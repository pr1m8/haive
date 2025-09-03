#!/usr/bin/env python3
"""Import Issue Tracker for Haive Documentation.

This script systematically tests imports of all modules and submodules,
tracks failures, and generates reports to help fix documentation issues.
"""
from __future__ import annotations

import ast
import importlib
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path

import yaml

# Setup paths
workspace_root = Path(__file__).resolve().parents[2]
packages_dir = workspace_root / 'packages'
for package_name in [
    'haive-core',
    'haive-agents',
    'haive-tools',
    'haive-games',
    'haive-dataflow',
    'haive-prebuilt',
    'haive-mcp',
]:
    package_path = packages_dir / package_name / 'src'
    if package_path.exists():
        sys.path.insert(0, str(package_path))


class ImportIssueTracker:
    """Track and analyze import issues across the Haive codebase."""

    def __init__(self, output_dir: Path | None = None):
        if output_dir is None:
            output_dir = workspace_root / 'docs' / 'import_analysis'
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Data structures
        self.successful_imports: set[str] = set()
        self.failed_imports: dict[str, dict] = {}
        self.partial_imports: dict[str, dict] = {}
        self.module_structure: dict[str, list[str]] = {}
        self.dependency_graph: dict[str, set[str]] = {}

        # Categories of issues
        self.import_categories = {
            'missing_dependencies': [],
            'circular_imports': [],
            'syntax_errors': [],
            'attribute_errors': [],
            'type_errors': [],
            'pydantic_issues': [],
            'langchain_issues': [],
            'other_errors': [],
        }

    def discover_modules(self) -> list[str]:
        """Discover all Python modules in the haive packages."""
        modules = []

        for package_name in [
            'haive-core',
            'haive-agents',
            'haive-tools',
            'haive-games',
            'haive-dataflow',
            'haive-prebuilt',
            'haive-mcp',
        ]:
            package_path = packages_dir / package_name / 'src'
            if not package_path.exists():
                continue

            # Find all Python files
            for py_file in package_path.rglob('*.py'):
                if py_file.name == '__init__.py':
                    continue
                if any(
                    skip in str(py_file)
                    for skip in ['test', 'example', 'demo', '__pycache__']
                ):
                    continue

                # Convert path to module name
                relative_path = py_file.relative_to(package_path)
                module_parts = list(relative_path.with_suffix('').parts)
                module_name = '.'.join(module_parts)
                modules.append(module_name)

        return sorted(modules)

    def test_import(
        self,
        module_name: str,
    ) -> tuple[bool, str | None, Exception | None]:
        """Test importing a specific module."""
        try:
            importlib.import_module(module_name)
            return True, None, None
        except Exception as e:
            error_type = type(e).__name__
            str(e)
            return False, error_type, e

    def analyze_import_error(
        self,
        module_name: str,
        error_type: str,
        error: Exception,
    ) -> dict:
        """Analyze an import error and categorize it."""
        error_info = {
            'module': module_name,
            'error_type': error_type,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'category': 'other_errors',
            'suggestions': [],
        }

        error_msg = str(error).lower()

        # Categorize errors
        if 'no module named' in error_msg:
            error_info['category'] = 'missing_dependencies'
            # Extract missing module
            if "'" in error_msg:
                missing_module = error_msg.split("'")[1]
                error_info['missing_module'] = missing_module
                error_info['suggestions'].append(
                    f"Add '{missing_module}' to autodoc_mock_imports",
                )

        elif 'circular import' in error_msg or 'cannot import name' in error_msg:
            error_info['category'] = 'circular_imports'
            error_info['suggestions'].append(
                'Refactor imports to avoid circular dependencies',
            )

        elif 'invalid syntax' in error_msg:
            error_info['category'] = 'syntax_errors'
            error_info['suggestions'].append('Fix syntax errors in the module')

        elif 'attributeerror' in error_type.lower():
            error_info['category'] = 'attribute_errors'
            error_info['suggestions'].append(
                'Check for missing attributes or incorrect imports',
            )

        elif 'typeerror' in error_type.lower():
            error_info['category'] = 'type_errors'
            if 'pydantic' in error_msg or 'basemodel' in error_msg:
                error_info['category'] = 'pydantic_issues'
                error_info['suggestions'].append(
                    'Check Pydantic model definitions and generics',
                )

        elif 'langchain' in error_msg or 'langgraph' in error_msg:
            error_info['category'] = 'langchain_issues'
            error_info['suggestions'].append(
                'Mock LangChain dependencies or check versions',
            )

        return error_info

    def analyze_module_structure(self, module_name: str) -> dict:
        """Analyze the structure of a module using AST."""
        try:
            # Find the module file
            module_path = None
            for package_name in [
                'haive-core',
                'haive-agents',
                'haive-tools',
                'haive-games',
                'haive-dataflow',
                'haive-prebuilt',
                'haive-mcp',
            ]:
                package_path = packages_dir / package_name / 'src'
                if not package_path.exists():
                    continue

                # Convert module name to file path
                parts = module_name.split('.')
                potential_path = package_path / '/'.join(parts[1:]) / '__init__.py'
                if not potential_path.exists():
                    potential_path = package_path / f"{'/'.join(parts[1:])}.py"

                if potential_path.exists():
                    module_path = potential_path
                    break

            if not module_path:
                return {'error': 'Module file not found'}

            # Parse with AST
            with open(module_path, encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            structure = {
                'imports': [],
                'classes': [],
                'functions': [],
                'constants': [],
                'has_all': False,
                'all_items': [],
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        structure['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            structure['imports'].append(f"{node.module}.{alias.name}")
                elif isinstance(node, ast.ClassDef):
                    structure['classes'].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    structure['functions'].append(node.name)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if target.id == '__all__':
                                structure['has_all'] = True
                                if isinstance(node.value, ast.List):
                                    structure['all_items'] = [
                                        elt.s
                                        for elt in node.value.elts
                                        if isinstance(elt, ast.Str)
                                    ]
                            elif target.id.isupper():
                                structure['constants'].append(target.id)

            return structure

        except Exception as e:
            return {'error': f"AST analysis failed: {e}"}

    def run_comprehensive_analysis(self) -> None:
        """Run comprehensive import analysis."""
        modules = self.discover_modules()

        for _i, module_name in enumerate(modules, 1):
            success, error_type, error = self.test_import(module_name)

            if success:
                self.successful_imports.add(module_name)
            else:
                error_info = self.analyze_import_error(module_name, error_type, error)
                self.failed_imports[module_name] = error_info

                # Add to category
                category = error_info['category']
                if category in self.import_categories:
                    self.import_categories[category].append(module_name)

            # Analyze structure regardless of import success
            structure = self.analyze_module_structure(module_name)
            self.module_structure[module_name] = structure

    def generate_reports(self) -> None:
        """Generate comprehensive reports."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 1. Summary report
        summary_report = {
            'timestamp': datetime.now().isoformat(),
            'total_modules': len(self.successful_imports) + len(self.failed_imports),
            'successful_imports': len(self.successful_imports),
            'failed_imports': len(self.failed_imports),
            'success_rate': len(self.successful_imports)
            / (len(self.successful_imports) + len(self.failed_imports))
            * 100,
            'error_categories': {
                cat: len(modules) for cat, modules in self.import_categories.items()
            },
            'top_error_types': self._get_top_error_types(),
            'recommendations': self._generate_recommendations(),
        }

        # 2. Detailed failure report
        failures_report = {
            'timestamp': datetime.now().isoformat(),
            'failed_imports': self.failed_imports,
            'categorized_failures': self.import_categories,
            'missing_dependencies': self._extract_missing_dependencies(),
            'suggested_mocks': self._generate_mock_suggestions(),
        }

        # 3. Module structure report
        structure_report = {
            'timestamp': datetime.now().isoformat(),
            'module_structures': self.module_structure,
            'modules_with_all': [
                m for m, s in self.module_structure.items() if s.get('has_all', False)
            ],
            'modules_without_all': [
                m
                for m, s in self.module_structure.items()
                if not s.get('has_all', False)
            ],
        }

        # 4. Sphinx configuration suggestions
        sphinx_suggestions = self._generate_sphinx_config_suggestions()

        # Save reports
        reports = {
            f"import_analysis_summary_{timestamp}.json": summary_report,
            f"import_failures_detailed_{timestamp}.json": failures_report,
            f"module_structures_{timestamp}.json": structure_report,
            f"sphinx_config_suggestions_{timestamp}.yaml": sphinx_suggestions,
        }

        for filename, content in reports.items():
            filepath = self.output_dir / filename
            if filename.endswith('.yaml'):
                with open(filepath, 'w') as f:
                    yaml.dump(content, f, default_flow_style=False)
            else:
                with open(filepath, 'w') as f:
                    json.dump(content, f, indent=2)

        # 5. Generate markdown summary
        self._generate_markdown_summary(timestamp)

    def _get_top_error_types(self) -> dict[str, int]:
        """Get the most common error types."""
        error_counts = {}
        for failure in self.failed_imports.values():
            error_type = failure['error_type']
            error_counts[error_type] = error_counts.get(error_type, 0) + 1

        return dict(sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:10])

    def _extract_missing_dependencies(self) -> set[str]:
        """Extract all missing dependencies."""
        missing = set()
        for failure in self.failed_imports.values():
            if (
                failure['category'] == 'missing_dependencies'
                and 'missing_module' in failure
            ):
                missing.add(failure['missing_module'])
        return sorted(missing)

    def _generate_mock_suggestions(self) -> list[str]:
        """Generate mock import suggestions for sphinx conf.py."""
        missing_deps = self._extract_missing_dependencies()
        current_mocks = {
            'langchain',
            'langchain_core',
            'langchain_community',
            'langchain_openai',
            'langgraph',
            'langsmith',
            'neo4j',
            'sqlalchemy',
            'psycopg2',
            'chromadb',
            'faiss',
            'pinecone',
            'weaviate',
            'qdrant_client',
            'elasticsearch',
            'supabase',
            # ... (existing mocks from conf.py)
        }

        new_mocks = []
        for dep in missing_deps:
            if dep not in current_mocks:
                new_mocks.append(dep)

        return sorted(new_mocks)

    def _generate_recommendations(self) -> list[str]:
        """Generate actionable recommendations."""
        recs = []

        if self.import_categories['missing_dependencies']:
            recs.append(
                f"Add {len(self.import_categories['missing_dependencies'])} missing dependencies to autodoc_mock_imports",
            )

        if self.import_categories['pydantic_issues']:
            recs.append(
                f"Fix {len(self.import_categories['pydantic_issues'])} Pydantic model issues (generics, inheritance)",
            )

        if self.import_categories['circular_imports']:
            recs.append(
                f"Resolve {len(self.import_categories['circular_imports'])} circular import issues",
            )

        if self.import_categories['syntax_errors']:
            recs.append(
                f"Fix {len(self.import_categories['syntax_errors'])} syntax errors",
            )

        success_rate = (
            len(self.successful_imports)
            / (len(self.successful_imports) + len(self.failed_imports))
            * 100
        )
        if success_rate < 80:
            recs.append(
                'Consider disabling autosummary for problematic modules until issues are resolved',
            )

        return recs

    def _generate_sphinx_config_suggestions(self) -> dict:
        """Generate Sphinx configuration suggestions."""
        return {
            'autodoc_mock_imports_additions': self._generate_mock_suggestions(),
            'exclude_patterns_additions': [
                f"**/{module.replace('.', '/')}*"
                for module in list(self.failed_imports.keys())[:20]  # Top 20 failures
            ],
            'autosummary_skip_modules': list(self.failed_imports.keys()),
            'recommended_settings': {
                'autodoc_default_options': {
                    'members': True,
                    'undoc-members': False,  # Disable for problematic modules
                    'show-inheritance': True,
                    'ignore-module-all': True,
                },
                'autosummary_generate': False,  # Disable until issues resolved
                'suppress_warnings': [
                    'autodoc.import_object',
                    'autosummary.import_cycle',
                ],
            },
        }

    def _generate_markdown_summary(self, timestamp: str) -> None:
        """Generate a readable markdown summary."""
        content = f"""# Import Analysis Report - {timestamp}

## Summary
- **Total modules analyzed**: {len(self.successful_imports) + len(self.failed_imports)}
- **Successful imports**: {len(self.successful_imports)} ({len(self.successful_imports) / (len(self.successful_imports) + len(self.failed_imports)) * 100:.1f}%)
- **Failed imports**: {len(self.failed_imports)} ({len(self.failed_imports) / (len(self.successful_imports) + len(self.failed_imports)) * 100:.1f}%)

## Error Categories
"""

        for category, modules in self.import_categories.items():
            if modules:
                content += f"\n### {category.replace('_', ' ').title()} ({len(modules)} modules)\n"
                for module in modules[:10]:  # Show first 10
                    error_info = self.failed_imports.get(module, {})
                    content += f"- `{module}`: {error_info.get('error_message', 'Unknown error')}\n"
                if len(modules) > 10:
                    content += f"- ... and {len(modules) - 10} more\n"

        content += """
## Top Recommendations
"""
        for rec in self._generate_recommendations():
            content += f"- {rec}\n"

        content += """
## Missing Dependencies to Mock
```python
autodoc_mock_imports = [
    # Existing mocks...
"""
        for dep in self._generate_mock_suggestions()[:20]:
            content += f'    "{dep}",\n'
        content += ']\n```\n'

        # Save markdown
        md_path = self.output_dir / f"import_analysis_report_{timestamp}.md"
        with open(md_path, 'w') as f:
            f.write(content)


def main():
    """Run the import issue tracker."""
    tracker = ImportIssueTracker()
    tracker.run_comprehensive_analysis()
    tracker.generate_reports()


if __name__ == '__main__':
    main()
