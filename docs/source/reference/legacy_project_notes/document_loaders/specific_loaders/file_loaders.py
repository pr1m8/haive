"""File-based Document Loaders for Haive Framework.

This module implements various file-based document loaders including Jupyter notebooks,
Python files, subtitles, bibtex files, and other specialized formats.
"""

from pathlib import Path
from typing import Any

from pydantic import FilePath

from ..source_implementation import LocalSource, auto_source


@auto_source
class JupyterNotebookSource(LocalSource):
    """Jupyter notebook source."""

    file_path: FilePath
    include_outputs: bool = False
    include_code_only: bool = False
    remove_markdown: bool = False

    class Config:
        file_extensions = [".ipynb"]
        loader_strategies = {
            "basic": {
                "class": "NotebookLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["notebooks", "code_with_output"],
            }
        }

    def create_basic_loader(self):
        """Create a NotebookLoader."""
        try:
            from langchain_community.document_loaders import NotebookLoader

            return NotebookLoader(
                str(self.file_path),
                include_outputs=self.include_outputs,
                max_output_length=None,  # No limit by default
                include_code_only=self.include_code_only,
                remove_newline=False,
                remove_markdown=self.remove_markdown,
            )
        except ImportError:
            # Fallback to reading the file directly
            try:
                import json

                with open(self.file_path, encoding="utf-8") as f:
                    notebook_data = json.load(f)

                # Extract text content manually
                content = ""
                for cell in notebook_data.get("cells", []):
                    cell_type = cell.get("cell_type", "")

                    # Handle code cells
                    if cell_type == "code":
                        if not self.remove_markdown:
                            source = "".join(cell.get("source", []))
                            content += f"```python\n{source}\n```\n\n"

                        # Include outputs if specified
                        if self.include_outputs:
                            for output in cell.get("outputs", []):
                                if "text" in output:
                                    output_text = "".join(output["text"])
                                    content += f"Output:\n{output_text}\n\n"
                                elif (
                                    "data" in output and "text/plain" in output["data"]
                                ):
                                    output_text = "".join(output["data"]["text/plain"])
                                    content += f"Output:\n{output_text}\n\n"

                    # Handle markdown cells
                    elif cell_type == "markdown" and not self.remove_markdown:
                        source = "".join(cell.get("source", []))
                        content += f"{source}\n\n"

                # Create document
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content=content,
                        metadata={
                            "source": str(self.file_path),
                            "filename": self.file_path.name,
                        },
                    )
                ]
            except Exception:
                # Last resort fallback - read as plain text
                with open(self.file_path, encoding="utf-8") as f:
                    text = f.read()
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content=text, metadata={"source": str(self.file_path)}
                    )
                ]


@auto_source
class PythonSource(LocalSource):
    """Python source code file."""

    file_path: FilePath
    include_comments: bool = True
    include_docstrings: bool = True
    include_imports: bool = True

    class Config:
        file_extensions = [".py"]
        loader_strategies = {
            "basic": {
                "class": "PythonLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["code", "python_files"],
            },
            "text": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_code"],
            },
        }

    def create_basic_loader(self):
        """Create a PythonLoader."""
        try:
            from langchain_community.document_loaders import PythonLoader

            return PythonLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly with AST parsing
            try:
                import ast

                with open(self.file_path, encoding="utf-8") as f:
                    source_code = f.read()

                # Parse Python code
                tree = ast.parse(source_code)

                # Initialize document content
                content = source_code if self.include_comments else ""

                # Extract docstrings if needed
                if self.include_docstrings and not self.include_comments:
                    docstrings = []

                    # Function to extract docstrings from AST node
                    def extract_docstring(node):
                        if isinstance(
                            node, ast.Module | ast.ClassDef | ast.FunctionDef
                        ) and (
                            len(node.body) > 0
                            and isinstance(node.body[0], ast.Expr)
                            and isinstance(node.body[0].value, ast.Constant)
                            and isinstance(node.body[0].value.value, str)
                        ):
                            if isinstance(node, ast.Module):
                                docstrings.append(
                                    f"Module docstring: {node.body[0].value.value}"
                                )
                            elif isinstance(node, ast.ClassDef):
                                docstrings.append(
                                    f"Class {node.name} docstring: {node.body[0].value.value}"
                                )
                            elif isinstance(node, ast.FunctionDef):
                                docstrings.append(
                                    f"Function {node.name} docstring: {node.body[0].value.value}"
                                )

                    # Visit all nodes to extract docstrings
                    for node in ast.walk(tree):
                        extract_docstring(node)

                    content = "\n\n".join(docstrings)

                # Create document
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content=content,
                        metadata={
                            "source": str(self.file_path),
                            "filename": self.file_path.name,
                            "language": "python",
                        },
                    )
                ]
            except Exception:
                # Fallback to text loader
                return self.create_text_loader()

    def create_text_loader(self):
        """Create a basic TextLoader for Python files."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(
                    page_content=text,
                    metadata={"source": str(self.file_path), "language": "python"},
                )
            ]


@auto_source
class SubtitleSource(LocalSource):
    """Subtitle file source (SRT, VTT, etc.)."""

    file_path: FilePath
    include_timestamps: bool = False

    class Config:
        file_extensions = [".srt", ".vtt", ".ass", ".ssa"]
        loader_strategies = {
            "basic": {
                "class": "SRTLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["subtitles", "transcripts"],
            },
            "text": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_subtitles"],
            },
        }

    def create_basic_loader(self):
        """Create an SRTLoader."""
        try:
            from langchain_community.document_loaders import SRTLoader

            return SRTLoader(str(self.file_path))
        except ImportError:
            # Parse SRT file manually
            try:
                import re

                with open(self.file_path, encoding="utf-8", errors="replace") as f:
                    content = f.read()

                # Simple SRT parsing
                # Format: index, timestamp, text, blank line
                blocks = re.split(r"\n\s*\n", content)
                texts = []

                for block in blocks:
                    lines = block.strip().split("\n")
                    if len(lines) >= 3:
                        try:
                            # First line should be index number
                            int(lines[0])
                            # Second line is the timestamp
                            timestamp = lines[1]
                            # Rest is the text
                            text = "\n".join(lines[2:])

                            if self.include_timestamps:
                                texts.append(f"[{timestamp}] {text}")
                            else:
                                texts.append(text)
                        except (ValueError, IndexError):
                            # Skip invalid blocks
                            continue

                # Join all text
                full_text = " ".join(texts)

                # Create document
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content=full_text,
                        metadata={
                            "source": str(self.file_path),
                            "format": self.file_path.suffix[
                                1:
                            ],  # Remove dot from extension
                        },
                    )
                ]
            except Exception:
                # Fallback to text loader
                return self.create_text_loader()

    def create_text_loader(self):
        """Create a basic TextLoader for subtitle files."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8", errors="replace") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]


@auto_source
class BibtexSource(LocalSource):
    """BibTeX bibliography source."""

    file_path: FilePath
    include_abstract: bool = True
    include_notes: bool = True

    class Config:
        file_extensions = [".bib", ".bibtex"]
        loader_strategies = {
            "basic": {
                "class": "BibtexLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["bibliography", "references"],
            },
            "text": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_bibtex"],
            },
        }

    def create_basic_loader(self):
        """Create a BibtexLoader."""
        try:
            from langchain_community.document_loaders import BibtexLoader

            return BibtexLoader(
                str(self.file_path),
                include_abstract=self.include_abstract,
                include_notes=self.include_notes,
            )
        except ImportError:
            # Parse BibTeX manually
            try:
                import re

                with open(self.file_path, encoding="utf-8") as f:
                    content = f.read()

                # Extract entries
                entry_pattern = r"@(\w+)\s*\{([^,]*),(.*?)\}"
                entries = re.findall(entry_pattern, content, re.DOTALL)

                documents = []
                from langchain_core.documents import Document

                for entry_type, cite_key, fields_text in entries:
                    # Parse fields
                    field_pattern = r"(\w+)\s*=\s*\{(.*?)\}"
                    fields = dict(re.findall(field_pattern, fields_text, re.DOTALL))

                    # Build text representation
                    text_parts = [f"Type: {entry_type}", f"Citation Key: {cite_key}"]

                    # Add author, title, year if available
                    for field in ["author", "title", "year", "journal", "booktitle"]:
                        if field in fields:
                            text_parts.append(f"{field.capitalize()}: {fields[field]}")

                    # Add abstract if requested and available
                    if self.include_abstract and "abstract" in fields:
                        text_parts.append(f"Abstract: {fields['abstract']}")

                    # Add notes if requested and available
                    if self.include_notes and "note" in fields:
                        text_parts.append(f"Notes: {fields['note']}")

                    # Create document
                    documents.append(
                        Document(
                            page_content="\n".join(text_parts),
                            metadata={
                                "source": str(self.file_path),
                                "cite_key": cite_key,
                                "entry_type": entry_type,
                                **{
                                    k: v
                                    for k, v in fields.items()
                                    if k in ["author", "title", "year"]
                                },
                            },
                        )
                    )

                return documents
            except Exception:
                # Fallback to text loader
                return self.create_text_loader()

    def create_text_loader(self):
        """Create a basic TextLoader for BibTeX files."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]


@auto_source
class ReStructuredTextSource(LocalSource):
    """ReStructuredText (RST) document source."""

    file_path: FilePath

    class Config:
        file_extensions = [".rst"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredRSTLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["documentation", "rst_files"],
            },
            "text": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_rst"],
            },
        }

    def create_unstructured_loader(self):
        """Create an UnstructuredRSTLoader."""
        try:
            from langchain_community.document_loaders import UnstructuredRSTLoader

            return UnstructuredRSTLoader(str(self.file_path), mode="elements")
        except ImportError:
            # Fallback to text loader
            return self.create_text_loader()

    def create_text_loader(self):
        """Create a basic TextLoader for RST files."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]


@auto_source
class TSVSource(LocalSource):
    """Tab-separated values file source."""

    file_path: FilePath
    has_header: bool = True

    class Config:
        file_extensions = [".tsv"]
        loader_strategies = {
            "basic": {
                "class": "UnstructuredTSVLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["tabular_data"],
            },
            "csv": {
                "class": "CSVLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_tsv"],
            },
        }

    def create_basic_loader(self):
        """Create an UnstructuredTSVLoader."""
        try:
            from langchain_community.document_loaders import UnstructuredTSVLoader

            return UnstructuredTSVLoader(str(self.file_path))
        except ImportError:
            # Fallback to CSV loader
            return self.create_csv_loader()

    def create_csv_loader(self):
        """Create a CSVLoader with tab delimiter."""
        try:
            from langchain_community.document_loaders import CSVLoader

            return CSVLoader(
                file_path=str(self.file_path),
                csv_args={
                    "delimiter": "\t",
                    "fieldnames": None if self.has_header else [],
                },
            )
        except ImportError:
            # Fallback to pandas if available
            try:
                from langchain_community.document_loaders import DataFrameLoader
                import pandas as pd

                # Read TSV into pandas DataFrame
                df = pd.read_csv(
                    self.file_path,
                    delimiter="\t",
                    header=0 if self.has_header else None,
                )

                # Use first column as index if it makes sense
                page_content_column = df.columns[0] if len(df.columns) > 0 else None

                return DataFrameLoader(
                    data_frame=df, page_content_column=page_content_column
                )
            except ImportError:
                # Last resort: read as text
                with open(self.file_path, encoding="utf-8") as f:
                    text = f.read()
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content=text, metadata={"source": str(self.file_path)}
                    )
                ]


@auto_source
class OrgModeSource(LocalSource):
    """Org Mode document source."""

    file_path: FilePath

    class Config:
        file_extensions = [".org"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredOrgModeLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["org_mode", "emacs"],
            },
            "text": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_org"],
            },
        }

    def create_unstructured_loader(self):
        """Create an UnstructuredOrgModeLoader."""
        try:
            from langchain_community.document_loaders import UnstructuredOrgModeLoader

            return UnstructuredOrgModeLoader(str(self.file_path), mode="elements")
        except ImportError:
            # Fallback to text loader
            return self.create_text_loader()

    def create_text_loader(self):
        """Create a basic TextLoader for Org Mode files."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]


@auto_source
class CHMSource(LocalSource):
    """Windows Help file (CHM) source."""

    file_path: FilePath

    class Config:
        file_extensions = [".chm"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredCHMLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["help_files", "documentation"],
            }
        }

    def create_unstructured_loader(self):
        """Create an UnstructuredCHMLoader."""
        try:
            from langchain_community.document_loaders import UnstructuredCHMLoader

            return UnstructuredCHMLoader(str(self.file_path), mode="elements")
        except ImportError:
            # Fallback to a custom CHM parser
            try:
                # Try using pychm or other libraries if available
                import subprocess
                import tempfile

                # Extract CHM to temporary directory using external tool
                with tempfile.TemporaryDirectory() as temp_dir:
                    try:
                        # Try using extract_chmLib if available
                        subprocess.run(
                            ["extract_chmLib", str(self.file_path), temp_dir],
                            check=True,
                            capture_output=True,
                        )

                        # Read extracted HTML files
                        import glob
                        import os

                        html_files = glob.glob(
                            os.path.join(temp_dir, "**", "*.html"), recursive=True
                        )
                        html_files += glob.glob(
                            os.path.join(temp_dir, "**", "*.htm"), recursive=True
                        )

                        # Process HTML files
                        all_content = []
                        for html_file in html_files:
                            try:
                                with open(
                                    html_file, encoding="utf-8", errors="replace"
                                ) as f:
                                    html_content = f.read()

                                # Use Beautiful Soup to extract text if available
                                try:
                                    from bs4 import BeautifulSoup

                                    soup = BeautifulSoup(html_content, "html.parser")
                                    all_content.append(soup.get_text())
                                except ImportError:
                                    # Simple HTML tag removal
                                    import re

                                    text = re.sub(r"<[^>]+>", " ", html_content)
                                    all_content.append(text)
                            except Exception:
                                continue

                        # Create document
                        from langchain_core.documents import Document

                        return [
                            Document(
                                page_content="\n\n".join(all_content),
                                metadata={"source": str(self.file_path)},
                            )
                        ]
                    except Exception:
                        # If extraction fails, return empty document
                        from langchain_core.documents import Document

                        return [
                            Document(
                                page_content="[CHM file could not be extracted]",
                                metadata={"source": str(self.file_path)},
                            )
                        ]
            except Exception:
                # If all else fails, return an empty document
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content="[CHM file could not be processed]",
                        metadata={"source": str(self.file_path)},
                    )
                ]


@auto_source
class MHTMLSource(LocalSource):
    """MHTML web archive source."""

    file_path: FilePath

    class Config:
        file_extensions = [".mhtml", ".mht"]
        loader_strategies = {
            "basic": {
                "class": "MHTMLLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["web_archives", "saved_pages"],
            },
            "text": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "low",
                "best_for": ["simple_mhtml"],
            },
        }

    def create_basic_loader(self):
        """Create an MHTMLLoader."""
        try:
            from langchain_community.document_loaders import MHTMLLoader

            return MHTMLLoader(str(self.file_path))
        except ImportError:
            # Try to parse MHTML manually
            try:
                import email
                import re

                with open(self.file_path, encoding="utf-8", errors="replace") as f:
                    content = f.read()

                # Parse MHTML as email multipart
                message = email.message_from_string(content)

                # Extract HTML part
                html_content = ""
                for part in message.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/html":
                        html_content = part.get_payload(decode=True).decode(
                            "utf-8", errors="replace"
                        )
                        break

                # Extract text from HTML
                try:
                    from bs4 import BeautifulSoup

                    soup = BeautifulSoup(html_content, "html.parser")
                    text = soup.get_text()
                except ImportError:
                    # Simple HTML tag removal
                    text = re.sub(r"<[^>]+>", " ", html_content)

                # Create document
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content=text,
                        metadata={
                            "source": str(self.file_path),
                            "title": message.get("Subject", ""),
                        },
                    )
                ]
            except Exception:
                # Fallback to text loader
                return self.create_text_loader()

    def create_text_loader(self):
        """Create a basic TextLoader for MHTML files."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8", errors="replace") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]


@auto_source
class VisioSource(LocalSource):
    """Microsoft Visio document source."""

    file_path: FilePath

    class Config:
        file_extensions = [".vsdx", ".vsd"]
        loader_strategies = {
            "basic": {
                "class": "VsdxLoader",
                "speed": "medium",
                "quality": "medium",
                "best_for": ["diagrams", "visio"],
            }
        }

    def create_basic_loader(self):
        """Create a VsdxLoader."""
        try:
            from langchain_community.document_loaders import VsdxLoader

            return VsdxLoader(str(self.file_path))
        except ImportError:
            # Try to parse VSDX manually as it's basically a ZIP file with XML content
            try:
                import re
                import xml.etree.ElementTree as ET
                import zipfile

                # Extract text from Visio XML content
                all_text = []

                with zipfile.ZipFile(self.file_path) as vsdx:
                    # Look for document.xml and page XMLs
                    for file_info in vsdx.infolist():
                        if (
                            file_info.filename.endswith(".xml")
                            and "/page" in file_info.filename.lower()
                        ):
                            with vsdx.open(file_info) as xml_file:
                                try:
                                    tree = ET.parse(xml_file)
                                    root = tree.getroot()

                                    # Extract text elements - specific implementation depends on Visio XML schema
                                    # This is a simplified version
                                    for elem in root.iter():
                                        if "Text" in elem.tag and elem.text:
                                            all_text.append(elem.text)
                                except Exception:
                                    continue

                # If nothing found, try a different approach for shapes
                if not all_text:
                    with zipfile.ZipFile(self.file_path) as vsdx:
                        for file_info in vsdx.infolist():
                            if (
                                "page" in file_info.filename.lower()
                                and file_info.filename.endswith(".xml")
                            ):
                                try:
                                    content = vsdx.read(file_info).decode("utf-8")
                                    # Simple regex for shape text
                                    texts = re.findall(
                                        r"<Text>(.*?)</Text>", content, re.DOTALL
                                    )
                                    all_text.extend(texts)
                                except Exception:
                                    continue

                # Create document
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content="\n".join(all_text),
                        metadata={"source": str(self.file_path)},
                    )
                ]
            except Exception:
                # Return empty document if all parsing fails
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content="[Visio file could not be parsed]",
                        metadata={"source": str(self.file_path)},
                    )
                ]


@auto_source
class NotionSource(LocalSource):
    """Notion export source."""

    directory_path: Path
    include_media: bool = False
    include_databases: bool = True

    class Config:
        loader_strategies = {
            "directory": {
                "class": "NotionDirectoryLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["notion_export", "documentation"],
            }
        }

    def create_directory_loader(self):
        """Create a NotionDirectoryLoader."""
        try:
            from langchain_community.document_loaders import NotionDirectoryLoader

            return NotionDirectoryLoader(
                str(self.directory_path), include_hidden=False, recursive=True
            )
        except ImportError:
            # Fallback to processing Notion Markdown files manually
            try:
                import glob
                import os

                # Find all Markdown files in the directory
                md_files = glob.glob(
                    os.path.join(str(self.directory_path), "**/*.md"), recursive=True
                )

                documents = []
                from langchain_core.documents import Document

                for md_file in md_files:
                    try:
                        with open(md_file, encoding="utf-8") as f:
                            content = f.read()

                        # Extract title from filename
                        title = os.path.basename(md_file).replace(".md", "")

                        # Create document for each Markdown file
                        documents.append(
                            Document(
                                page_content=content,
                                metadata={
                                    "source": md_file,
                                    "title": title,
                                    "type": "notion_page",
                                },
                            )
                        )
                    except Exception:
                        continue

                # Process CSV files if they exist and databases are included
                if self.include_databases:
                    csv_files = glob.glob(
                        os.path.join(str(self.directory_path), "**/*.csv"),
                        recursive=True,
                    )

                    for csv_file in csv_files:
                        try:
                            with open(csv_file, encoding="utf-8") as f:
                                content = f.read()

                            # Extract database name from filename
                            db_name = os.path.basename(csv_file).replace(".csv", "")

                            # Create document for each CSV file
                            documents.append(
                                Document(
                                    page_content=content,
                                    metadata={
                                        "source": csv_file,
                                        "title": db_name,
                                        "type": "notion_database",
                                    },
                                )
                            )
                        except Exception:
                            continue

                return documents
            except Exception:
                # Return empty document if all parsing fails
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content="[Notion directory could not be processed]",
                        metadata={"source": str(self.directory_path)},
                    )
                ]


@auto_source
class ObsidianSource(LocalSource):
    """Obsidian vault source."""

    directory_path: Path
    include_media: bool = False
    follow_links: bool = True

    class Config:
        loader_strategies = {
            "basic": {
                "class": "ObsidianLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["obsidian_vault", "linked_notes"],
            }
        }

    def create_basic_loader(self):
        """Create an ObsidianLoader."""
        try:
            from langchain_community.document_loaders import ObsidianLoader

            return ObsidianLoader(
                str(self.directory_path), encoding="utf-8", collect_metadata=True
            )
        except ImportError:
            # Fallback to processing Obsidian Markdown files manually
            try:
                import glob
                import os
                import re

                # Find all Markdown files in the directory
                md_files = glob.glob(
                    os.path.join(str(self.directory_path), "**/*.md"), recursive=True
                )

                # Regular expressions for Obsidian syntax
                wikilink_pattern = (
                    r"\[\[(.*?)(?:\|(.*?))?\]\]"  # [[Link]] or [[Link|Text]]
                )
                tag_pattern = r"#([A-Za-z0-9_-]+)"  # #tag

                documents = []
                from langchain_core.documents import Document

                # Process each Markdown file
                for md_file in md_files:
                    try:
                        with open(md_file, encoding="utf-8") as f:
                            content = f.read()

                        # Extract title from filename
                        title = os.path.basename(md_file).replace(".md", "")

                        # Extract links and tags
                        wikilinks = re.findall(wikilink_pattern, content)
                        tags = re.findall(tag_pattern, content)

                        # Process links if enabled
                        if self.follow_links:
                            # Replace wiki links with plain text
                            for link in wikilinks:
                                if len(link) >= 2:
                                    link_target, link_text = link
                                    display_text = (
                                        link_text if link_text else link_target
                                    )
                                    content = content.replace(
                                        f"[[{link_target}|{link_text}]]", display_text
                                    )
                                elif len(link) >= 1:
                                    link_target = link[0]
                                    content = content.replace(
                                        f"[[{link_target}]]", link_target
                                    )

                        # Create document for each Markdown file
                        documents.append(
                            Document(
                                page_content=content,
                                metadata={
                                    "source": md_file,
                                    "title": title,
                                    "tags": tags,
                                    "links": [link[0] for link in wikilinks],
                                },
                            )
                        )
                    except Exception:
                        continue

                return documents
            except Exception:
                # Return empty document if all parsing fails
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content="[Obsidian vault could not be processed]",
                        metadata={"source": str(self.directory_path)},
                    )
                ]


@auto_source
class ReadTheDocsSource(LocalSource):
    """ReadTheDocs documentation source."""

    directory_path: Path

    class Config:
        loader_strategies = {
            "basic": {
                "class": "ReadTheDocsLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["documentation", "sphinx"],
            }
        }

    def create_basic_loader(self):
        """Create a ReadTheDocsLoader."""
        try:
            from langchain_community.document_loaders import ReadTheDocsLoader

            return ReadTheDocsLoader(str(self.directory_path), features="html.parser")
        except ImportError:
            # Fallback to processing HTML files manually
            try:
                import glob
                import os

                # Find all HTML files in the directory
                html_files = glob.glob(
                    os.path.join(str(self.directory_path), "**/*.html"), recursive=True
                )

                documents = []
                from langchain_core.documents import Document

                for html_file in html_files:
                    try:
                        # Parse HTML
                        with open(html_file, encoding="utf-8") as f:
                            html_content = f.read()

                        # Extract text from HTML
                        try:
                            from bs4 import BeautifulSoup

                            soup = BeautifulSoup(html_content, "html.parser")

                            # Extract title
                            title_tag = soup.find("title")
                            title = (
                                title_tag.text
                                if title_tag
                                else os.path.basename(html_file)
                            )

                            # Extract main content - ReadTheDocs typically has a 'main' element
                            main_content = (
                                soup.find("div", {"role": "main"})
                                or soup.find("main")
                                or soup.find("div", {"class": "document"})
                            )

                            if main_content:
                                # Remove navigation, sidebars, etc.
                                for nav in main_content.find_all(["nav", "aside"]):
                                    nav.decompose()

                                text = main_content.get_text(separator="\n")
                            else:
                                # Fallback to body content
                                body = soup.find("body")
                                text = (
                                    body.get_text(separator="\n")
                                    if body
                                    else soup.get_text(separator="\n")
                                )

                            # Create document
                            documents.append(
                                Document(
                                    page_content=text,
                                    metadata={"source": html_file, "title": title},
                                )
                            )
                        except ImportError:
                            # Simple HTML tag removal if BeautifulSoup is not available
                            import re

                            text = re.sub(r"<[^>]+>", " ", html_content)
                            documents.append(
                                Document(
                                    page_content=text, metadata={"source": html_file}
                                )
                            )
                    except Exception:
                        continue

                return documents
            except Exception:
                # Return empty document if all parsing fails
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content="[ReadTheDocs documentation could not be processed]",
                        metadata={"source": str(self.directory_path)},
                    )
                ]


@auto_source
class SlackSource(LocalSource):
    """Slack export source."""

    directory_path: Path
    include_users: bool = True
    include_channels: bool = True

    class Config:
        loader_strategies = {
            "directory": {
                "class": "SlackDirectoryLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["slack_export", "chat_history"],
            }
        }

    def create_directory_loader(self):
        """Create a SlackDirectoryLoader."""
        try:
            from langchain_community.document_loaders import SlackDirectoryLoader

            return SlackDirectoryLoader(str(self.directory_path))
        except ImportError:
            # Process Slack export JSON files manually
            try:
                import glob
                import json
                import os

                # Find all JSON files in the directory
                json_files = glob.glob(
                    os.path.join(str(self.directory_path), "**/*.json"), recursive=True
                )

                documents = []
                from langchain_core.documents import Document

                # Process channel files
                for json_file in json_files:
                    try:
                        with open(json_file, encoding="utf-8") as f:
                            data = json.load(f)

                        # Skip users.json file if not including users
                        if (
                            not self.include_users
                            and os.path.basename(json_file) == "users.json"
                        ):
                            continue

                        # Process user data
                        if (
                            os.path.basename(json_file) == "users.json"
                            and self.include_users
                        ):
                            user_info = []
                            for user in data:
                                if isinstance(user, dict):
                                    user_id = user.get("id", "")
                                    real_name = user.get("real_name", "")
                                    display_name = user.get("profile", {}).get(
                                        "display_name", ""
                                    )
                                    user_info.append(
                                        f"User: {real_name or display_name} (ID: {user_id})"
                                    )

                            # Create document for users
                            if user_info:
                                documents.append(
                                    Document(
                                        page_content="\n".join(user_info),
                                        metadata={
                                            "source": json_file,
                                            "type": "slack_users",
                                        },
                                    )
                                )
                            continue

                        # Process channel data
                        if self.include_channels and isinstance(data, list):
                            # Get channel name from directory
                            channel_dir = os.path.dirname(json_file)
                            channel_name = os.path.basename(channel_dir)

                            # Process messages
                            messages = []
                            for msg in data:
                                if (
                                    isinstance(msg, dict)
                                    and "user" in msg
                                    and "text" in msg
                                ):
                                    user = msg.get("user", "")
                                    text = msg.get("text", "")
                                    ts = msg.get("ts", "")

                                    # Basic timestamp formatting
                                    try:
                                        import datetime

                                        timestamp = float(ts)
                                        date = datetime.datetime.fromtimestamp(
                                            timestamp
                                        ).strftime("%Y-%m-%d %H:%M:%S")
                                    except (ValueError, TypeError):
                                        date = ts

                                    messages.append(f"[{date}] {user}: {text}")

                            # Create document for channel
                            if messages:
                                documents.append(
                                    Document(
                                        page_content="\n".join(messages),
                                        metadata={
                                            "source": json_file,
                                            "channel": channel_name,
                                            "type": "slack_channel",
                                        },
                                    )
                                )
                    except Exception:
                        continue

                return documents
            except Exception:
                # Return empty document if all parsing fails
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content="[Slack export could not be processed]",
                        metadata={"source": str(self.directory_path)},
                    )
                ]


@auto_source
class GutenbergSource(RemoteSource):
    """Project Gutenberg book source."""

    url: str | None = None
    book_id: int | None = None

    class Config:
        domain_patterns = ["gutenberg.org"]
        path_patterns = ["/files/*"]
        loader_strategies = {
            "basic": {
                "class": "GutenbergLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["books", "literature"],
            }
        }

    def create_basic_loader(self):
        """Create a GutenbergLoader."""
        try:
            from langchain_community.document_loaders import GutenbergLoader

            # Use book_id if provided, otherwise extract from URL
            if self.book_id:
                return GutenbergLoader(self.book_id)
            if self.url:
                # Extract book ID from URL
                import re

                match = re.search(r"/files/(\d+)", self.url)
                if match:
                    book_id = int(match.group(1))
                    return GutenbergLoader(book_id)

            # If no valid book_id found, fetch the URL directly
            from langchain_community.document_loaders import WebBaseLoader

            return WebBaseLoader(self.url)
        except ImportError:
            # Fallback to web scraping
            try:
                from bs4 import BeautifulSoup
                import requests

                # Determine URL
                url = self.url
                if not url and self.book_id:
                    url = f"https://www.gutenberg.org/files/{self.book_id}/{self.book_id}-h/{self.book_id}-h.htm"

                if not url:
                    raise ValueError("Either url or book_id must be provided")

                # Fetch content
                response = requests.get(url)
                response.raise_for_status()

                # Parse HTML
                soup = BeautifulSoup(response.text, "html.parser")

                # Extract title
                title_tag = soup.find("title")
                title = title_tag.text if title_tag else "Unknown Gutenberg Book"

                # Extract main content - typically in a div with class 'pgdbtextmain' or similar
                main_content = soup.find("div", {"class": "pgdbtextmain"}) or soup.find(
                    "body"
                )

                if main_content:
                    # Remove headers, footers, tables of contents
                    for elem in main_content.find_all(["header", "footer", "nav"]):
                        elem.decompose()

                    text = main_content.get_text(separator="\n")
                else:
                    text = soup.get_text(separator="\n")

                # Create document
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content=text,
                        metadata={
                            "source": url,
                            "title": title,
                            "book_id": self.book_id,
                        },
                    )
                ]
            except Exception as e:
                # Return document with error message
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content=f"[Error loading Gutenberg book: {e!s}]",
                        metadata={"source": self.url or f"gutenberg:{self.book_id}"},
                    )
                ]


# Additional convenience function for automatic loader creation


def create_file_loader(file_path: str | Path, **kwargs) -> Any:
    """Create the appropriate file-based loader for a given file path.

    Args:
        file_path: Path to the file
        **kwargs: Additional arguments for specific loaders

    Returns:
        A document loader instance
    """
    # Convert to Path object if string
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # Get file extension
    extension = file_path.suffix.lower()

    # Create appropriate source based on extension
    if extension == ".ipynb":
        source = JupyterNotebookSource(file_path=file_path, **kwargs)
    elif extension == ".py":
        source = PythonSource(file_path=file_path, **kwargs)
    elif extension in [".srt", ".vtt", ".ass", ".ssa"]:
        source = SubtitleSource(file_path=file_path, **kwargs)
    elif extension in [".bib", ".bibtex"]:
        source = BibtexSource(file_path=file_path, **kwargs)
    elif extension == ".rst":
        source = ReStructuredTextSource(file_path=file_path, **kwargs)
    elif extension == ".tsv":
        source = TSVSource(file_path=file_path, **kwargs)
    elif extension == ".org":
        source = OrgModeSource(file_path=file_path, **kwargs)
    elif extension == ".chm":
        source = CHMSource(file_path=file_path, **kwargs)
    elif extension in [".mhtml", ".mht"]:
        source = MHTMLSource(file_path=file_path, **kwargs)
    elif extension in [".vsdx", ".vsd"]:
        source = VisioSource(file_path=file_path, **kwargs)
    else:
        # Try to use a more general source from text_loaders.py
        from .text_loaders import create_text_loader

        return create_text_loader(file_path, **kwargs)

    # Get strategy if specified
    strategy = kwargs.get("strategy")

    # Create loader with specified or default strategy
    return source.create_loader(strategy)
