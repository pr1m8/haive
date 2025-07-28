#!/usr/bin/env python3
"""Focused Issues Analyzer - Fast, targeted analysis of remaining issues.

This script analyzes only the specific categories of issues we need to fix:
- Complex syntax errors (146 files)
- Circular imports
- Schema field shadowing warnings

It's optimized for speed and focuses on known problematic files.
"""

import ast
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FocusedIssuesAnalyzer:
    """Fast, targeted analyzer for remaining critical issues."""
    
    def __init__(self, root_path: str = "/home/will/Projects/haive/backend/haive"):
        self.root_path = Path(root_path)
        self.issues = {
            "complex_syntax_errors": [],
            "circular_imports": [],
            "schema_warnings": []
        }
    
    def analyze_issues(self) -> dict[str, Any]:
        """Analyze only the critical remaining issues."""
        logger.info("🔍 Fast analysis of critical remaining issues...")
        
        # First get the files that actually have syntax errors
        syntax_error_files = self._get_syntax_error_files()
        logger.info(f"📋 Found {len(syntax_error_files)} files with syntax errors")
        
        # Analyze only these problematic files
        self._analyze_syntax_errors_in_files(syntax_error_files)
        
        # Quick circular import check
        self._quick_circular_import_check()
        
        # Schema warnings in BaseModel files only
        self._analyze_schema_warnings_quick()
        
        return self.issues
    
    def _get_syntax_error_files(self) -> list[Path]:
        """Get list of files that actually have syntax errors."""
        syntax_error_files = []
        
        # Use our existing quick scan to get the problematic files
        try:
            result = subprocess.run([
                sys.executable, "scripts/quick_syntax_scan.py"
            ], cwd=self.root_path, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Extract file paths from the output (looking for "Error in ...")
                for line in result.stdout.split('\n'):
                    if "Error in" in line and ".py:" in line:
                        # Extract file path
                        match = re.search(r'Error in ([^:]+\.py)', line)
                        if match:
                            file_path = Path(match.group(1))
                            if file_path.exists():
                                syntax_error_files.append(file_path)
        except:
            # Fallback: manually check files
            logger.warning("Quick scan failed, using manual check...")
            python_files = list(self.root_path.rglob("*.py"))
            for py_file in python_files[:100]:  # Limit to first 100 for speed
                if self._has_syntax_error(py_file):
                    syntax_error_files.append(py_file)
        
        return syntax_error_files
    
    def _has_syntax_error(self, file_path: Path) -> bool:
        """Quick check if file has syntax error."""
        try:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
            ast.parse(content)
            return False
        except SyntaxError:
            return True
        except:
            return False
    
    def _analyze_syntax_errors_in_files(self, files: list[Path]):
        """Analyze syntax errors in specific files only."""
        logger.info(f"📋 Analyzing {len(files)} files with syntax errors...")
        
        for py_file in files:
            try:
                with open(py_file, encoding='utf-8') as f:
                    content = f.read()
                
                try:
                    ast.parse(content)
                except SyntaxError as e:
                    error_info = self._categorize_syntax_error(py_file, content, e)
                    if error_info:
                        self.issues["complex_syntax_errors"].append(error_info)
                        
            except Exception as e:
                logger.debug(f"Could not read {py_file}: {e}")
    
    def _categorize_syntax_error(self, file_path: Path, content: str, error: SyntaxError) -> dict[str, Any]:
        """Categorize and suggest fix for syntax error."""
        lines = content.splitlines()
        error_line_idx = (error.lineno - 1) if error.lineno else 0
        
        if error_line_idx >= len(lines):
            error_line_idx = len(lines) - 1
            
        problem_line = lines[error_line_idx] if error_line_idx >= 0 else ""
        error_msg = str(error).lower()
        
        # Get context
        start = max(0, error_line_idx - 1)
        end = min(len(lines), error_line_idx + 2)
        context = lines[start:end]
        
        # Categorize error type
        if "unterminated string" in error_msg:
            error_type = "unterminated_string"
            auto_fixable = True
            confidence = 0.8
            fix_suggestion = "Add missing closing quote"
        elif "unexpected character after line continuation" in error_msg:
            error_type = "line_continuation"
            auto_fixable = True
            confidence = 0.9
            fix_suggestion = "Remove invalid line continuation character"
        elif "invalid syntax" in error_msg and ('"' in problem_line or "'" in problem_line):
            error_type = "quote_issues"
            auto_fixable = True
            confidence = 0.7
            fix_suggestion = "Fix quote mismatches"
        elif "expected ':'" in error_msg:
            error_type = "missing_colon"
            auto_fixable = True
            confidence = 0.8
            fix_suggestion = "Add missing colon after if/for/def/class statement"
        elif "unindent does not match" in error_msg:
            error_type = "indentation_error"
            auto_fixable = False
            confidence = 0.2
            fix_suggestion = "Fix indentation manually"
        else:
            error_type = "other_syntax_error"
            auto_fixable = False
            confidence = 0.1
            fix_suggestion = "Manual review required"
        
        return {
            "file": str(file_path),
            "line": error.lineno,
            "column": error.offset,
            "error_type": error_type,
            "error_message": str(error),
            "problem_line": problem_line,
            "context": context,
            "auto_fixable": auto_fixable,
            "fix_confidence": confidence,
            "fix_suggestion": fix_suggestion
        }
    
    def _quick_circular_import_check(self):
        """Quick check for circular imports using import analysis."""
        logger.info("🔄 Quick circular import analysis...")
        
        # Look for common circular import patterns
        suspicious_patterns = [
            ("haive.core", "haive.agents"),
            ("haive.agents", "haive.core"),
            ("haive.core.engine", "haive.core.schema"),
            ("haive.core.schema", "haive.core.engine")
        ]
        
        python_files = list(self.root_path.rglob("*.py"))[:200]  # Limit for speed
        
        for py_file in python_files:
            try:
                with open(py_file, encoding='utf-8') as f:
                    content = f.read()
                
                imports = self._extract_import_names(content)
                
                # Check for suspicious patterns
                for pattern1, pattern2 in suspicious_patterns:
                    if pattern1 in imports and any(pattern2 in imp for imp in imports):
                        self.issues["circular_imports"].append({
                            "file": str(py_file),
                            "pattern": f"{pattern1} <-> {pattern2}",
                            "imports": imports,
                            "severity": "medium",
                            "fix_suggestion": "Move imports to function level or use TYPE_CHECKING"
                        })
                        
            except:
                continue
    
    def _extract_import_names(self, content: str) -> list[str]:
        """Extract import module names from content."""
        imports = []
        
        # Simple regex-based extraction for speed
        import_patterns = [
            r'^\s*import\s+([a-zA-Z0-9_.]+)',
            r'^\s*from\s+([a-zA-Z0-9_.]+)\s+import'
        ]
        
        for line in content.split('\n'):
            for pattern in import_patterns:
                match = re.match(pattern, line)
                if match:
                    imports.append(match.group(1))
        
        return imports
    
    def _analyze_schema_warnings_quick(self):
        """Quick analysis of schema field shadowing warnings."""
        logger.info("⚠️ Quick schema warnings analysis...")
        
        # Look only in files that contain "BaseModel"
        schema_files = []
        for py_file in self.root_path.rglob("*.py"):
            try:
                with open(py_file, encoding='utf-8') as f:
                    content = f.read()
                if "BaseModel" in content:
                    schema_files.append(py_file)
            except:
                continue
        
        logger.info(f"📊 Found {len(schema_files)} files with BaseModel")
        
        # Common shadowed fields
        shadowed_fields = ["schema", "schema_json", "max_tokens", "max_output_tokens", "model"]
        
        for py_file in schema_files:
            try:
                with open(py_file, encoding='utf-8') as f:
                    content = f.read()
                
                # Look for field definitions that might shadow
                for field in shadowed_fields:
                    pattern = rf'^\s*{field}\s*:\s*'
                    matches = re.finditer(pattern, content, re.MULTILINE)
                    
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        self.issues["schema_warnings"].append({
                            "file": str(py_file),
                            "line": line_num,
                            "field": field,
                            "issue_type": "field_shadowing",
                            "severity": "warning",
                            "fix_suggestion": f"Rename field to {field}_value or use alias",
                            "auto_fixable": True,
                            "fix_confidence": 0.7
                        })
                        
            except:
                continue
    
    def generate_fix_summary(self) -> str:
        """Generate a summary with fix recommendations."""
        syntax_errors = self.issues["complex_syntax_errors"]
        circular_imports = self.issues["circular_imports"]
        schema_warnings = self.issues["schema_warnings"]
        
        auto_fixable_syntax = len([e for e in syntax_errors if e.get("auto_fixable", False)])
        auto_fixable_schema = len([w for w in schema_warnings if w.get("auto_fixable", False)])
        
        summary = []
        summary.append("# 🔧 Focused Issues Analysis Summary")
        summary.append("")
        summary.append(f"## 📋 Complex Syntax Errors: {len(syntax_errors)}")
        summary.append(f"- **Auto-fixable**: {auto_fixable_syntax}")
        summary.append(f"- **Manual fixes needed**: {len(syntax_errors) - auto_fixable_syntax}")
        summary.append("")
        
        if syntax_errors:
            summary.append("### Top Syntax Error Types:")
            error_types = {}
            for error in syntax_errors:
                error_type = error.get("error_type", "unknown")
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
                summary.append(f"- **{error_type}**: {count} files")
        
        summary.append("")
        summary.append(f"## 🔄 Circular Imports: {len(circular_imports)}")
        summary.append("")
        summary.append(f"## ⚠️ Schema Warnings: {len(schema_warnings)}")
        summary.append(f"- **Auto-fixable**: {auto_fixable_schema}")
        summary.append("")
        
        total_auto_fixable = auto_fixable_syntax + auto_fixable_schema
        summary.append(f"## 🎯 **Total Auto-fixable Issues: {total_auto_fixable}**")
        summary.append("")
        summary.append("Ready to generate fix scripts!")
        
        return "\n".join(summary)


def main():
    """Main analysis function."""
    analyzer = FocusedIssuesAnalyzer()
    
    print("🔍 Starting focused analysis of remaining issues...")
    issues = analyzer.analyze_issues()
    
    # Save detailed results
    output_file = "/home/will/Projects/haive/backend/haive/focused_issues_analysis.json"
    with open(output_file, "w") as f:
        json.dump(issues, f, indent=2, default=str)
    
    # Generate summary
    summary = analyzer.generate_fix_summary()
    summary_file = "/home/will/Projects/haive/backend/haive/FOCUSED_ISSUES_SUMMARY.md"
    with open(summary_file, "w") as f:
        f.write(summary)
    
    print("✅ Focused analysis complete!")
    print(f"📋 Found {len(issues['complex_syntax_errors'])} complex syntax errors")
    print(f"🔄 Found {len(issues['circular_imports'])} circular import issues")
    print(f"⚠️ Found {len(issues['schema_warnings'])} schema warnings")
    print("")
    print("📄 Results saved to:")
    print(f"  - {output_file}")
    print(f"  - {summary_file}")


if __name__ == "__main__":
    main()