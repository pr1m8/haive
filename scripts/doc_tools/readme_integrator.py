#!/usr/bin/env python3
"""README Integration Tool for Haive Documentation.

This script discovers README files throughout the codebase and
integrates them into the Sphinx documentation.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import yaml


class ReadmeIntegrator:
    """Integrates README files into Sphinx documentation."""

    def __init__(self, workspace_root: Path, docs_source: Path):
        self.workspace_root = workspace_root
        self.docs_source = docs_source
        self.packages_dir = workspace_root / 'packages'
        self.output_dir = docs_source / 'discovered_readmes'

    def discover_readmes(self) -> list[tuple[Path, Path]]:
        """Discover all README files in the workspace."""
        readme_files = []

        # Patterns to exclude
        exclude_patterns = [
            'node_modules',
            'build',
            'dist',
            '__pycache__',
            '.git',
            '.tox',
            '.pytest_cache',
            'egg-info',
            '.venv',
            'venv',
            '.nox',
            'site-packages',
            '.cache',
            'resources/embeddings_cache',
        ]

        # Find READMEs in packages directory only
        for package_dir in self.packages_dir.glob('haive-*'):
            # Look for README in package root
            for name in ['README.md', 'readme.md', 'README.rst']:
                readme = package_dir / name
                if readme.exists():
                    relative_path = readme.relative_to(self.workspace_root)
                    readme_files.append((readme, relative_path))
                    break

            # Look for READMEs in src subdirectories
            src_dir = package_dir / 'src'
            if src_dir.exists():
                for readme in src_dir.rglob('README.md'):
                    # Skip excluded paths
                    if any(pattern in str(readme) for pattern in exclude_patterns):
                        continue

                    relative_path = readme.relative_to(self.workspace_root)
                    readme_files.append((readme, relative_path))

        # Add main README if exists
        main_readme = self.workspace_root / 'README.md'
        if main_readme.exists():
            readme_files.insert(0, (main_readme, Path('README.md')))

        # Add project docs READMEs
        project_docs = self.workspace_root / 'project_docs'
        if project_docs.exists():
            for readme in project_docs.rglob('README.md'):
                if any(pattern in str(readme) for pattern in exclude_patterns):
                    continue
                relative_path = readme.relative_to(self.workspace_root)
                readme_files.append((readme, relative_path))

        return sorted(readme_files, key=lambda x: x[1])

    def extract_readme_metadata(self, readme_path: Path) -> dict[str, str]:
        """Extract metadata from README file."""
        content = readme_path.read_text()
        lines = content.split('\n')

        metadata = {
            'title': '',
            'description': '',
            'category': 'general',
        }

        # Extract title (first heading)
        for line in lines:
            if line.startswith('# '):
                metadata['title'] = line[2:].strip()
                break

        # Extract description (first paragraph)
        in_paragraph = False
        description_lines = []
        for line in lines:
            line = line.strip()
            if not line and in_paragraph:
                break
            if line and not line.startswith('#') and not line.startswith('```'):
                in_paragraph = True
                description_lines.append(line)

        metadata['description'] = ' '.join(description_lines)[:200]

        # Determine category based on path
        relative_path = str(readme_path.relative_to(self.workspace_root))
        if 'haive-agents' in relative_path:
            metadata['category'] = 'agents'
        elif 'haive-tools' in relative_path:
            metadata['category'] = 'tools'
        elif 'haive-games' in relative_path:
            metadata['category'] = 'games'
        elif 'haive-core' in relative_path:
            metadata['category'] = 'core'
        elif 'haive-dataflow' in relative_path:
            metadata['category'] = 'dataflow'
        elif 'haive-prebuilt' in relative_path:
            metadata['category'] = 'prebuilt'
        elif 'haive-mcp' in relative_path:
            metadata['category'] = 'mcp'

        return metadata

    def convert_markdown_links(
        self,
        content: str,
        source_path: Path,
        dest_path: Path,
    ) -> str:
        """Convert relative markdown links to work in new location."""
        # Pattern for markdown links: [text](url)
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        def replace_link(match):
            text = match.group(1)
            url = match.group(2)

            # Skip external links
            if url.startswith(('http://', 'https://', '#')):
                return match.group(0)

            # Convert relative path
            if not url.startswith('/'):
                # Make path absolute relative to source README
                abs_path = (source_path.parent / url).resolve()

                # Check if it's within workspace
                try:
                    rel_to_workspace = abs_path.relative_to(self.workspace_root)
                    # Convert to path relative to destination
                    new_url = f"../../{rel_to_workspace}"
                    return f"[{text}]({new_url})"
                except ValueError:
                    # Path is outside workspace, keep as is
                    pass

            return match.group(0)

        return link_pattern.sub(replace_link, content)

    def process_readme(self, readme_path: Path, relative_path: Path) -> Path:
        """Process a README file for documentation."""
        # Create output path
        output_path = self.output_dir / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Read content
        content = readme_path.read_text()

        # Extract metadata
        metadata = self.extract_readme_metadata(readme_path)

        # Convert links
        content = self.convert_markdown_links(content, readme_path, output_path)

        # Add metadata header
        header = f"""
```{{note}}
**Original Location:** `{relative_path}`

**Category:** {metadata["category"]}
```

"""

        # Write processed content
        output_path.write_text(header + content)

        return output_path

    def create_index_files(
        self,
        processed_files: list[tuple[Path, dict[str, str]]],
    ) -> None:
        """Create index files for discovered READMEs."""
        # Group by category
        by_category = {}
        for output_path, metadata in processed_files:
            category = metadata['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append((output_path, metadata))

        # Create main index
        main_index = self.output_dir / 'index.rst'
        main_content = """
Discovered Documentation
========================

This section contains README files and other documentation discovered throughout
the Haive codebase, organized by category.

.. toctree::
   :maxdepth: 2
   :caption: Categories

"""

        # Add category indices
        for category in sorted(by_category.keys()):
            main_content += f"   {category}/index\n"

            # Create category index
            category_dir = self.output_dir / category
            category_dir.mkdir(exist_ok=True)

            category_index = category_dir / 'index.rst'
            category_content = f"""
{category.title()} Documentation
{"=" * (len(category) + 14)}

.. toctree::
   :maxdepth: 2
   :caption: {category.title()} READMEs

"""

            # Add files to category index
            for output_path, metadata in sorted(
                by_category[category],
                key=lambda x: x[0],
            ):
                # Get relative path from output directory
                rel_path_from_output = output_path.relative_to(self.output_dir)

                # Add to toctree with proper relative path
                # We need to go up one level from category/index.rst to find the file
                category_content += f"   ../{rel_path_from_output.with_suffix('')}\n"

            category_index.write_text(category_content)

        main_index.write_text(main_content)

    def integrate_readmes(self) -> None:
        """Main integration process."""
        readme_files = self.discover_readmes()

        # Clean output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)

        # Process each README
        processed_files = []
        for readme_path, relative_path in readme_files:
            try:
                output_path = self.process_readme(readme_path, relative_path)
                metadata = self.extract_readme_metadata(readme_path)
                processed_files.append((output_path, metadata))
            except Exception:
                pass

        # Create index files
        self.create_index_files(processed_files)

        # Create summary file
        summary_path = self.output_dir / 'summary.yaml'
        summary_data = {
            'total_files': len(processed_files),
            'categories': {},
            'files': [],
        }

        for output_path, metadata in processed_files:
            category = metadata['category']
            if category not in summary_data['categories']:
                summary_data['categories'][category] = 0
            summary_data['categories'][category] += 1

            summary_data['files'].append(
                {
                    'path': str(output_path.relative_to(self.output_dir)),
                    'title': metadata['title'],
                    'category': category,
                    'description': metadata['description'],
                },
            )

        with open(summary_path, 'w') as f:
            yaml.dump(summary_data, f, default_flow_style=False)


def main():
    """Run the README integration."""
    # Get paths
    script_path = Path(__file__).resolve()
    workspace_root = script_path.parents[2]
    docs_source = workspace_root / 'docs' / 'source'

    # Run integration
    integrator = ReadmeIntegrator(workspace_root, docs_source)
    integrator.integrate_readmes()


if __name__ == '__main__':
    main()
