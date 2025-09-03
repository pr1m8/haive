#!/usr/bin/env python3
"""Docstring analyzer to detect non-compliant docstrings in Python files.

This script detects:
1. Docstrings containing ```python code blocks (markdown style)
2. Non-Google style docstrings
3. Missing docstrings
"""

import ast
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class DocstringIssue:
    """Represents a docstring issue found in a file."""
    file_path: str
    line_number: int
    issue_type: str
    description: str
    node_name: str
    node_type: str
    docstring_preview: Optional[str] = None


@dataclass 
class FileAnalysis:
    """Results of analyzing a single file."""
    file_path: str
    issues: List[DocstringIssue] = field(default_factory=list)
    total_functions: int = 0
    total_classes: int = 0
    total_methods: int = 0
    has_markdown_code_blocks: bool = False
    

class DocstringAnalyzer(ast.NodeVisitor):
    """AST visitor to analyze docstrings in Python files."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues: List[DocstringIssue] = []
        self.total_functions = 0
        self.total_classes = 0
        self.total_methods = 0
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit function definitions."""
        self.total_functions += 1
        self._check_docstring(node, "function")
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Visit async function definitions."""
        self.total_functions += 1
        self._check_docstring(node, "async_function")
        self.generic_visit(node)
        
    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definitions."""
        self.total_classes += 1
        self._check_docstring(node, "class")
        
        # Visit methods
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.total_methods += 1
                self._check_docstring(item, "method")
        
        self.generic_visit(node)
        
    def visit_Module(self, node: ast.Module):
        """Visit module (file-level docstring)."""
        self._check_docstring(node, "module")
        self.generic_visit(node)
        
    def _check_docstring(self, node, node_type: str):
        """Check a node's docstring for issues."""
        docstring = ast.get_docstring(node)
        node_name = getattr(node, 'name', 'module')
        
        if docstring is None:
            # Skip __init__ methods and private functions for missing docstring check
            if node_name not in ['__init__', '__str__', '__repr__'] and not node_name.startswith('_'):
                self.issues.append(DocstringIssue(
                    file_path=self.file_path,
                    line_number=node.lineno if hasattr(node, 'lineno') else 1,
                    issue_type="missing_docstring",
                    description=f"Missing docstring for {node_type}",
                    node_name=node_name,
                    node_type=node_type
                ))
            return
            
        # Check for markdown code blocks
        if '```' in docstring:
            preview = docstring[:200] + '...' if len(docstring) > 200 else docstring
            self.issues.append(DocstringIssue(
                file_path=self.file_path,
                line_number=node.lineno if hasattr(node, 'lineno') else 1,
                issue_type="markdown_code_block",
                description=f"Docstring contains markdown-style code blocks (```)",
                node_name=node_name,
                node_type=node_type,
                docstring_preview=preview
            ))
            
        # Check for Google-style compliance
        if not self._is_google_style(docstring, node_type):
            self.issues.append(DocstringIssue(
                file_path=self.file_path,
                line_number=node.lineno if hasattr(node, 'lineno') else 1,
                issue_type="non_google_style",
                description=f"Docstring does not follow Google style guide",
                node_name=node_name,
                node_type=node_type,
                docstring_preview=docstring[:100] + '...' if len(docstring) > 100 else docstring
            ))
            
    def _is_google_style(self, docstring: str, node_type: str) -> bool:
        """Check if docstring follows Google style.
        
        Google style has:
        - Summary line
        - Blank line after summary (if multi-line)
        - Sections like Args:, Returns:, Raises:, Note:, Example:
        """
        lines = docstring.strip().split('\n')
        
        # Module docstrings can be more free-form
        if node_type == "module":
            return True
            
        # Check for common Google-style sections
        google_sections = ['Args:', 'Arguments:', 'Returns:', 'Return:', 'Yields:', 
                          'Raises:', 'Note:', 'Notes:', 'Example:', 'Examples:',
                          'Attributes:', 'See Also:', 'Todo:', 'Warning:', 'Warnings:']
        
        # For functions/methods, check if it has proper sections when needed
        if node_type in ["function", "method", "async_function"]:
            # Single line docstrings are acceptable for simple functions
            if len(lines) == 1 and len(lines[0]) < 80:
                return True
                
            # Multi-line should have sections if complex
            has_sections = any(
                any(section in line for section in google_sections) 
                for line in lines
            )
            
            # If multi-line and no sections, might not be Google style
            if len(lines) > 3 and not has_sections:
                return False
                
        return True
        

def analyze_file(file_path: Path) -> FileAnalysis:
    """Analyze a single Python file for docstring issues."""
    analysis = FileAnalysis(file_path=str(file_path))
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse AST
        tree = ast.parse(content, filename=str(file_path))
        
        # Visit nodes
        analyzer = DocstringAnalyzer(str(file_path))
        analyzer.visit(tree)
        
        # Collect results
        analysis.issues = analyzer.issues
        analysis.total_functions = analyzer.total_functions
        analysis.total_classes = analyzer.total_classes
        analysis.total_methods = analyzer.total_methods
        analysis.has_markdown_code_blocks = any(
            issue.issue_type == "markdown_code_block" 
            for issue in analyzer.issues
        )
        
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        
    return analysis


def print_analysis(analysis: FileAnalysis):
    """Print analysis results for a file."""
    print(f"\n{'='*80}")
    print(f"File: {analysis.file_path}")
    print(f"{'='*80}")
    
    print(f"\nStatistics:")
    print(f"  - Classes: {analysis.total_classes}")
    print(f"  - Functions: {analysis.total_functions}")
    print(f"  - Methods: {analysis.total_methods}")
    print(f"  - Total issues: {len(analysis.issues)}")
    print(f"  - Has markdown code blocks: {analysis.has_markdown_code_blocks}")
    
    if analysis.issues:
        print(f"\nIssues found:")
        
        # Group by issue type
        issues_by_type = {}
        for issue in analysis.issues:
            if issue.issue_type not in issues_by_type:
                issues_by_type[issue.issue_type] = []
            issues_by_type[issue.issue_type].append(issue)
            
        for issue_type, issues in issues_by_type.items():
            print(f"\n  {issue_type.replace('_', ' ').title()} ({len(issues)} found):")
            for issue in issues[:5]:  # Show first 5 of each type
                print(f"    - Line {issue.line_number}: {issue.node_type} '{issue.node_name}'")
                if issue.docstring_preview:
                    preview = issue.docstring_preview.replace('\n', ' ')[:60]
                    print(f"      Preview: {preview}...")
            if len(issues) > 5:
                print(f"    ... and {len(issues) - 5} more")
    else:
        print("\n✅ No issues found!")


def main():
    """Main entry point for the docstring analyzer."""
    if len(sys.argv) < 2:
        print("Usage: python detect_docstring_issues.py <file_path>")
        sys.exit(1)
        
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist")
        sys.exit(1)
        
    if not file_path.suffix == '.py':
        print(f"Error: File {file_path} is not a Python file")
        sys.exit(1)
        
    # Analyze the file
    analysis = analyze_file(file_path)
    
    # Print results
    print_analysis(analysis)
    
    # Return exit code based on issues
    if analysis.has_markdown_code_blocks:
        sys.exit(1)  # Exit with error if markdown blocks found
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()