#!/usr/bin/env python3
"""
Convert README.md files to proper Python __init__.py docstrings.

This script identifies all legitimate README files in the codebase and converts
them to Google-style docstrings in their corresponding __init__.py files.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ReadmeToDocstringConverter:
    """Convert README files to proper Python docstrings using Google style."""
    
    def __init__(self, packages_dir: Path):
        self.packages_dir = packages_dir
        self.readme_to_init_map: Dict[Path, Path] = {}
        self.conversion_report: List[Dict] = []
        
    def scan_readmes(self) -> None:
        """Scan for legitimate README files and map to __init__.py locations."""
        # Exclude unwanted paths
        exclude_patterns = [
            "/.venv/", "/venv/", "/site-packages/", "/.pytest_cache/",
            "/resources/embeddings_cache/", "/temp_refactor/"
        ]
        
        readme_files = []
        for readme_path in self.packages_dir.rglob("README*.md"):
            # Skip if in excluded paths
            if any(pattern in str(readme_path) for pattern in exclude_patterns):
                continue
            readme_files.append(readme_path)
        
        print(f"Found {len(readme_files)} legitimate README files")
        
        # Map each README to its corresponding __init__.py
        for readme_path in readme_files:
            init_path = self._find_corresponding_init(readme_path)
            if init_path:
                self.readme_to_init_map[readme_path] = init_path
            else:
                print(f"Warning: No __init__.py found for {readme_path}")
    
    def _find_corresponding_init(self, readme_path: Path) -> Optional[Path]:
        """Find the corresponding __init__.py for a README file."""
        readme_dir = readme_path.parent
        init_path = readme_dir / "__init__.py"
        
        # If __init__.py exists, use it
        if init_path.exists():
            return init_path
        
        # If no __init__.py, create one
        return init_path
    
    def analyze_readme_content(self, readme_path: Path) -> Dict:
        """Analyze README content and extract key information."""
        try:
            content = readme_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {readme_path}: {e}")
            return {}
        
        # Extract title (first # heading)
        title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        title = title_match.group(1) if title_match else readme_path.parent.name
        
        # Extract description (content after title, before next heading)
        desc_pattern = r'^#\s+.+?\n\n(.*?)(?=\n#{1,6}\s|\Z)'
        desc_match = re.search(desc_pattern, content, re.MULTILINE | re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else ""
        
        # Clean up description (remove extra whitespace, markdown)
        description = re.sub(r'\n+', ' ', description)
        description = re.sub(r'\s+', ' ', description)
        description = description[:500] + "..." if len(description) > 500 else description
        
        # Extract examples
        examples = self._extract_examples(content)
        
        # Determine module type
        module_type = self._determine_module_type(readme_path, content)
        
        return {
            'title': title,
            'description': description,
            'examples': examples,
            'module_type': module_type,
            'readme_path': readme_path,
            'content_length': len(content)
        }
    
    def _extract_examples(self, content: str) -> List[str]:
        """Extract code examples from README content."""
        # Find code blocks
        code_blocks = re.findall(r'```(?:python)?\n(.*?)\n```', content, re.DOTALL)
        
        # Clean and filter examples
        examples = []
        for block in code_blocks:
            block = block.strip()
            if len(block) > 10 and ('import' in block or 'from' in block):
                examples.append(block)
        
        return examples[:2]  # Limit to 2 examples
    
    def _determine_module_type(self, readme_path: Path, content: str) -> str:
        """Determine what type of module this is based on path and content."""
        path_str = str(readme_path).lower()
        content_lower = content.lower()
        
        if 'agent' in path_str:
            if 'base' in path_str:
                return 'base_module'
            elif any(x in path_str for x in ['rag', 'react', 'planning', 'reasoning']):
                return 'agent_implementation'
            else:
                return 'agent_module'
        elif 'engine' in path_str or 'core' in path_str:
            return 'core_module'
        elif 'tool' in path_str:
            return 'tool_module'
        elif 'game' in path_str:
            return 'game_module'
        elif 'util' in path_str or 'common' in path_str:
            return 'utility_module'
        else:
            return 'general_module'
    
    def generate_docstring(self, readme_info: Dict) -> str:
        """Generate Google-style docstring from README information."""
        title = readme_info['title']
        description = readme_info['description']
        examples = readme_info['examples']
        module_type = readme_info['module_type']
        
        # Start with title and description
        docstring_parts = [f'"""{title}']
        
        if description:
            docstring_parts.append('')
            docstring_parts.append(description)
        
        # Add module-specific information
        if module_type == 'agent_implementation':
            docstring_parts.extend([
                '',
                'This module provides agent implementations using advanced AI patterns.',
                'Agents are designed to work with the Haive framework for complex reasoning tasks.'
            ])
        elif module_type == 'core_module':
            docstring_parts.extend([
                '',
                'Core functionality for the Haive framework.',
                'Provides essential building blocks for agent and workflow construction.'
            ])
        elif module_type == 'tool_module':
            docstring_parts.extend([
                '',
                'Tools and utilities for agent interactions.',
                'Compatible with the Haive agent framework and external integrations.'
            ])
        
        # Add examples if available
        if examples:
            docstring_parts.extend(['', 'Examples:'])
            for i, example in enumerate(examples):
                if i == 0:
                    docstring_parts.append('    Basic usage::')
                else:
                    docstring_parts.append('    Advanced usage::')
                docstring_parts.append('')
                for line in example.split('\n'):
                    docstring_parts.append(f'        {line}')
                docstring_parts.append('')
        
        # Add attributes section for modules
        docstring_parts.extend([
            'Note:',
            '    This module is part of the Haive AI agent framework.',
            '    For detailed documentation, see the official Haive docs.'
        ])
        
        docstring_parts.append('"""')
        return '\n'.join(docstring_parts)
    
    def create_conversion_plan(self) -> None:
        """Create a plan for converting READMEs to docstrings."""
        print("\n=== README to Docstring Conversion Plan ===")
        
        for readme_path, init_path in self.readme_to_init_map.items():
            readme_info = self.analyze_readme_content(readme_path)
            
            # Determine relative path from packages root
            try:
                rel_readme = readme_path.relative_to(self.packages_dir)
                rel_init = init_path.relative_to(self.packages_dir)
            except ValueError:
                rel_readme = str(readme_path)
                rel_init = str(init_path)
            
            conversion_info = {
                'readme_path': str(rel_readme),
                'init_path': str(rel_init),
                'title': readme_info.get('title', 'Unknown'),
                'module_type': readme_info.get('module_type', 'unknown'),
                'has_examples': len(readme_info.get('examples', [])) > 0,
                'init_exists': init_path.exists(),
                'content_length': readme_info.get('content_length', 0)
            }
            
            self.conversion_report.append(conversion_info)
        
        # Sort by module type and path for better organization
        self.conversion_report.sort(key=lambda x: (x['module_type'], x['readme_path']))
        
        # Print summary
        print(f"\nTotal conversions planned: {len(self.conversion_report)}")
        
        # Group by module type
        type_counts = {}
        for item in self.conversion_report:
            module_type = item['module_type']
            type_counts[module_type] = type_counts.get(module_type, 0) + 1
        
        print("\nBy module type:")
        for module_type, count in sorted(type_counts.items()):
            print(f"  {module_type}: {count}")
        
        # Show examples of each type
        print("\nExample conversions:")
        shown_types = set()
        for item in self.conversion_report:
            module_type = item['module_type']
            if module_type not in shown_types and len(shown_types) < 5:
                print(f"  {module_type}: {item['readme_path']} → {item['init_path']}")
                shown_types.add(module_type)
    
    def save_conversion_report(self, output_file: Path) -> None:
        """Save detailed conversion report to a file."""
        report_content = [
            "# README to Docstring Conversion Report",
            f"**Generated**: {Path.cwd()}",
            f"**Total Conversions**: {len(self.conversion_report)}",
            "",
            "## Conversion Mapping",
            "",
            "| Module Type | README Path | Init Path | Has Examples | Status |",
            "|-------------|-------------|-----------|--------------|--------|"
        ]
        
        for item in self.conversion_report:
            status = "✅ Ready" if item['init_exists'] else "🆕 Create"
            examples_flag = "✅" if item['has_examples'] else "❌"
            
            report_content.append(
                f"| {item['module_type']} | `{item['readme_path']}` | `{item['init_path']}` | {examples_flag} | {status} |"
            )
        
        output_file.write_text('\n'.join(report_content))
        print(f"\nDetailed report saved to: {output_file}")


def main():
    """Main execution function."""
    packages_dir = Path(__file__).parent.parent / "packages"
    
    if not packages_dir.exists():
        print(f"Error: Packages directory not found at {packages_dir}")
        return
    
    print(f"Scanning packages directory: {packages_dir}")
    
    converter = ReadmeToDocstringConverter(packages_dir)
    
    # Step 1: Scan for READMEs
    converter.scan_readmes()
    
    # Step 2: Create conversion plan
    converter.create_conversion_plan()
    
    # Step 3: Save detailed report
    report_file = Path(__file__).parent.parent / "project_docs" / "readme_conversion_plan.md"
    report_file.parent.mkdir(exist_ok=True)
    converter.save_conversion_report(report_file)
    
    print(f"\n✅ Analysis complete!")
    print(f"📊 Found {len(converter.readme_to_init_map)} README files to convert")
    print(f"📄 Report saved to: {report_file}")
    print("\nNext steps:")
    print("1. Review the conversion plan")
    print("2. Run the actual conversion (implement convert_all method)")
    print("3. Update conf.py to exclude discovered_readmes")
    print("4. Apply showcase UI to new navigation")


if __name__ == "__main__":
    main()