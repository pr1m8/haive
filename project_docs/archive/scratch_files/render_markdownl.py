import logging
import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import markdown
from pydantic import BaseModel, Field, validator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("markdown_converter")


# Define supported output formats
class OutputFormat(str, Enum):
    HTML = "html"
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    EPUB = "epub"
    MARKDOWN = "md"  # For copying without conversion


# Pydantic model for configuration
class MarkdownConverterConfig(BaseModel):
    input_path: Path = Field(
        ..., description="Directory containing markdown files or a single markdown file"
    )
    output_dir: Path | None = Field(
        default=None,
        description="Directory where converted files will be saved (defaults to 'rendered' folder in input directory)",
    )
    formats: list[OutputFormat] = Field(
        default=[OutputFormat.HTML], description="Output formats to generate"
    )
    recursive: bool = Field(
        default=False, description="Whether to process directories recursively"
    )
    preserve_structure: bool = Field(
        default=True, description="Whether to preserve directory structure in output"
    )
    markdown_extensions: list[str] = Field(
        default=["extra", "codehilite"], description="Markdown extensions to use"
    )
    parallel: bool = Field(
        default=True, description="Whether to process files in parallel"
    )
    max_workers: int = Field(
        default=4, description="Maximum number of parallel workers"
    )
    pandoc_path: str | None = Field(
        default=None, description="Path to pandoc executable"
    )

    @validator("input_path", "output_dir", pre=True)
    def validate_paths(self, v):
        if isinstance(v, str):
            return Path(v)
        return v

    @validator("input_path")
    def validate_input_path_exists(self, v):
        if not v.exists():
            raise ValueError(f"Input path does not exist: {v}")
        return v

    @validator("output_dir", always=True)
    def set_default_output_dir(self, v, values):
        if v is None and "input_path" in values:
            # If output_dir is not provided, create a "rendered" folder in the input directory
            if values["input_path"].is_file():
                return values["input_path"].parent / "rendered"
            return values["input_path"] / "rendered"
        return v

    class Config:
        arbitrary_types_allowed = True


# Model representing a markdown file
class MarkdownFile(BaseModel):
    path: Path
    relative_path: Path | None = None
    content: str | None = None

    def load_content(self) -> str:
        """Load the content of the markdown file."""
        if self.content is None:
            try:
                self.content = self.path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # Try with different encodings if UTF-8 fails
                try:
                    self.content = self.path.read_text(encoding="latin-1")
                except Exception as e:
                    raise ValueError(f"Failed to read file {self.path}: {e}")
        return self.content

    class Config:
        arbitrary_types_allowed = True


# Exception classes
class ConverterException(Exception):
    """Base exception for converter errors."""


class PandocMissingError(ConverterException):
    """Raised when pandoc is required but not available."""


class FormatConversionError(ConverterException):
    """Raised when conversion to a specific format fails."""


# Renderer class
class MarkdownRenderer:
    def __init__(self, config: MarkdownConverterConfig):
        self.config = config
        self.md = markdown.Markdown(extensions=config.markdown_extensions)

        # Ensure output directory exists
        os.makedirs(self.config.output_dir, exist_ok=True)

        # Check for pandoc availability if needed formats are requested
        self.pandoc_required_formats = {
            OutputFormat.PDF,
            OutputFormat.DOCX,
            OutputFormat.EPUB,
        }

        self.needs_pandoc = any(
            fmt in self.pandoc_required_formats for fmt in config.formats
        )
        if self.needs_pandoc:
            self._check_pandoc()

    def _check_pandoc(self):
        """Check if pandoc is available."""
        pandoc_cmd = self.config.pandoc_path or "pandoc"
        try:
            result = subprocess.run(
                [pandoc_cmd, "--version"], capture_output=True, text=True, check=False
            )
            if result.returncode != 0:
                raise PandocMissingError(
                    "Pandoc is required for PDF, DOCX, and EPUB conversion but not found. "
                    "Please install pandoc or specify the path using pandoc_path."
                )
        except FileNotFoundError:
            raise PandocMissingError(
                "Pandoc is required for PDF, DOCX, and EPUB conversion but not found. "
                "Please install pandoc or specify the path using pandoc_path."
            )

        logger.info(
            f"Using pandoc: {result.stdout.splitlines()[0] if result.stdout else 'Unknown version'}"
        )

    def render_to_html(self, md_file: MarkdownFile) -> str:
        """Render markdown to HTML."""
        content = md_file.load_content()
        return self.md.convert(content)

    def _get_output_path(self, md_file: MarkdownFile, format: OutputFormat) -> Path:
        """Determine the output path for the converted file."""
        if md_file.relative_path and self.config.preserve_structure:
            output_subdir = self.config.output_dir / md_file.relative_path.parent
            os.makedirs(output_subdir, exist_ok=True)
            output_base = output_subdir / md_file.path.stem
        else:
            output_base = self.config.output_dir / md_file.path.stem

        return output_base.with_suffix(f".{format.value}")

    def save_as_html(self, md_file: MarkdownFile) -> Path:
        """Save markdown as HTML."""
        output_path = self._get_output_path(md_file, OutputFormat.HTML)
        html_content = self.render_to_html(md_file)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n')
            f.write(f"<title>{md_file.path.stem}</title>\n")
            f.write(
                "<style>body{font-family:system-ui,-apple-system,sans-serif;line-height:1.6;max-width:50em;margin:0 auto;padding:2em}</style>\n"
            )
            f.write("</head>\n<body>\n")
            f.write(html_content)
            f.write("\n</body>\n</html>")

        return output_path

    def save_as_text(self, md_file: MarkdownFile) -> Path:
        """Save markdown as plain text."""
        output_path = self._get_output_path(md_file, OutputFormat.TXT)
        content = md_file.load_content()

        # Simple markdown to text conversion
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    def save_as_markdown(self, md_file: MarkdownFile) -> Path:
        """Save as markdown (basically just copy)."""
        output_path = self._get_output_path(md_file, OutputFormat.MARKDOWN)
        content = md_file.load_content()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    def save_with_pandoc(self, md_file: MarkdownFile, format: OutputFormat) -> Path:
        """Save using pandoc for conversion."""
        if not self.needs_pandoc:
            self._check_pandoc()

        output_path = self._get_output_path(md_file, format)
        content = md_file.load_content()

        with tempfile.NamedTemporaryFile(
            suffix=".md", mode="w", encoding="utf-8", delete=False
        ) as temp:
            temp_path = temp.name
            temp.write(content)

        try:
            pandoc_cmd = self.config.pandoc_path or "pandoc"
            args = [
                pandoc_cmd,
                temp_path,
                "-o",
                str(output_path),
                "-f",
                "markdown",
                "-t",
                format.value,
            ]

            # Add special args for PDF if needed
            if format == OutputFormat.PDF:
                args.extend(["--pdf-engine=xelatex", "-V", "geometry:margin=1in"])

            result = subprocess.run(args, capture_output=True, text=True, check=False)

            if result.returncode != 0:
                raise FormatConversionError(
                    f"Pandoc conversion failed: {result.stderr}"
                )

            return output_path
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass

    def save_as_format(self, md_file: MarkdownFile, format: OutputFormat) -> Path:
        """Save markdown file in the specified format."""
        try:
            if format == OutputFormat.HTML:
                return self.save_as_html(md_file)
            if format == OutputFormat.TXT:
                return self.save_as_text(md_file)
            elif format == OutputFormat.MARKDOWN:
                return self.save_as_markdown(md_file)
            elif format in self.pandoc_required_formats:
                return self.save_with_pandoc(md_file, format)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            if isinstance(e, ConverterException):
                raise
            raise FormatConversionError(f"Failed to convert to {format}: {e!s}")


# Main utility class
class MarkdownConverter:
    def __init__(self, config: MarkdownConverterConfig):
        self.config = config

        # Ensure output directory exists
        os.makedirs(self.config.output_dir, exist_ok=True)
        logger.info(f"Output directory set to: {self.config.output_dir}")

        self.renderer = MarkdownRenderer(config)

    def collect_markdown_files(self) -> list[MarkdownFile]:
        """Collect all markdown files to be processed."""
        md_files = []
        input_path = self.config.input_path

        if input_path.is_file() and input_path.suffix.lower() in [".md", ".markdown"]:
            # Single file
            md_files.append(MarkdownFile(path=input_path))
        elif input_path.is_dir():
            # Directory of files
            base_path = input_path
            glob_pattern = "**/*.md" if self.config.recursive else "*.md"

            for md_path in input_path.glob(glob_pattern):
                if md_path.is_file():
                    relative_path = md_path.relative_to(base_path)
                    md_files.append(
                        MarkdownFile(path=md_path, relative_path=relative_path)
                    )

            # Also look for .markdown extension
            markdown_glob = "**/*.markdown" if self.config.recursive else "*.markdown"
            for md_path in input_path.glob(markdown_glob):
                if md_path.is_file():
                    relative_path = md_path.relative_to(base_path)
                    md_files.append(
                        MarkdownFile(path=md_path, relative_path=relative_path)
                    )
        else:
            raise ValueError(
                f"Input path '{input_path}' is not a valid markdown file or directory"
            )

        if not md_files:
            logger.warning(f"No markdown files found in {input_path}")

        return md_files

    def _convert_file(self, md_file: MarkdownFile) -> list[Path]:
        """Convert a single markdown file to all specified formats."""
        output_paths = []
        for format in self.config.formats:
            try:
                output_path = self.renderer.save_as_format(md_file, format)
                output_paths.append(output_path)
                logger.info(f"Converted {md_file.path} to {output_path}")
            except Exception as e:
                logger.exception(f"Error converting {md_file.path} to {format}: {e}")
                if isinstance(e, PandocMissingError):
                    # If pandoc is missing, skip all pandoc-required formats
                    logger.exception(
                        "Skipping all pandoc-required formats due to missing pandoc"
                    )
                    break
        return output_paths

    def convert(self) -> list[Path]:
        """Convert all markdown files to specified formats."""
        md_files = self.collect_markdown_files()
        all_output_paths = []

        if not md_files:
            return []

        if self.config.parallel and len(md_files) > 1:
            # Process files in parallel
            with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
                results = list(executor.map(self._convert_file, md_files))
                for result in results:
                    all_output_paths.extend(result)
        else:
            # Process files sequentially
            for md_file in md_files:
                output_paths = self._convert_file(md_file)
                all_output_paths.extend(output_paths)

        return all_output_paths


def convert_markdown(
    input_path: str | Path,
    output_dir: Union[str, Path] | None = None,
    formats: list[str] = ["html"],
    recursive: bool = False,
    preserve_structure: bool = True,
    markdown_extensions: list[str] = ["extra", "codehilite"],
    parallel: bool = True,
    max_workers: int = 4,
    pandoc_path: str | None = None,
) -> list[Path]:
    """Convert markdown files to various formats.

    Args:
        input_path: Path to a markdown file or directory containing markdown files
        output_dir: Directory where converted files will be saved.
                   If not provided, creates a "rendered" folder in the input directory
        formats: List of output formats (html, pdf, docx, txt, epub, md)
        recursive: Whether to process directories recursively
        preserve_structure: Whether to preserve directory structure in output
        markdown_extensions: Markdown extensions to use
        parallel: Whether to process files in parallel
        max_workers: Maximum number of parallel workers
        pandoc_path: Path to pandoc executable (optional)

    Returns:
        List of paths to the generated files

    Raises:
        ValueError: If input path doesn't exist or formats are invalid
        PandocMissingError: If pandoc is required but not available
        FormatConversionError: If conversion to a specific format fails
    """
    # Validate formats
    if formats is None:
        formats = ["html"]
    validated_formats = []
    for fmt in formats:
        try:
            validated_formats.append(OutputFormat(fmt.lower()))
        except ValueError:
            logger.warning(f"Unsupported format '{fmt}', skipping")

    if not validated_formats:
        validated_formats = [OutputFormat.HTML]
        logger.info("No valid formats specified, defaulting to HTML")

    # Create config
    config_kwargs = {
        "input_path": input_path,
        "formats": validated_formats,
        "recursive": recursive,
        "preserve_structure": preserve_structure,
        "markdown_extensions": markdown_extensions,
        "parallel": parallel,
        "max_workers": max_workers,
        "pandoc_path": pandoc_path,
    }

    if output_dir is not None:
        config_kwargs["output_dir"] = output_dir

    config = MarkdownConverterConfig(**config_kwargs)

    # Run conversion
    converter = MarkdownConverter(config)
    return converter.convert()


# Example usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert markdown files to various formats"
    )
    parser.add_argument(
        "input_path",
        help="Directory containing markdown files or a single markdown file",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        help="Directory where converted files will be saved (defaults to 'rendered' folder in input directory)",
    )
    parser.add_argument(
        "-f",
        "--formats",
        nargs="+",
        default=["html"],
        help="Output formats (html, pdf, docx, txt, epub, md)",
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Process directories recursively"
    )
    parser.add_argument(
        "--no-preserve-structure",
        action="store_false",
        dest="preserve_structure",
        help="Don't preserve directory structure in output",
    )
    parser.add_argument(
        "-e",
        "--extensions",
        nargs="+",
        default=["extra", "codehilite"],
        help="Markdown extensions to use",
    )
    parser.add_argument(
        "--no-parallel",
        action="store_false",
        dest="parallel",
        help="Disable parallel processing",
    )
    parser.add_argument(
        "--max-workers", type=int, default=4, help="Maximum number of parallel workers"
    )
    parser.add_argument("--pandoc-path", help="Path to pandoc executable")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger("markdown_converter").setLevel(logging.DEBUG)

    try:
        output_files = convert_markdown(
            input_path=args.input_path,
            output_dir=args.output_dir,
            formats=args.formats,
            recursive=args.recursive,
            preserve_structure=args.preserve_structure,
            markdown_extensions=args.extensions,
            parallel=args.parallel,
            max_workers=args.max_workers,
            pandoc_path=args.pandoc_path,
        )

        logger.info(f"Successfully converted {len(output_files)} files")
    except Exception as e:
        logger.exception(f"Conversion failed: {e}")
        import sys

        sys.exit(1)
