#!/usr/bin/env python3
"""Find all Pydantic validator issues by trying to import modules."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def find_python_modules(root_dir: Path) -> list[str]:
    """Find all Python modules that can be imported."""
    modules = []

    for py_file in root_dir.rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        if '/tests/' in str(py_file) or '/test_' in str(py_file):
            continue
        if py_file.name == '__init__.py':
            continue

        # Convert file path to module path
        try:
            relative_path = py_file.relative_to(
                root_dir.parent.parent,
            )  # relative to packages/
            module_parts = list(relative_path.parts)

            # Remove 'src' if present
            if 'src' in module_parts:
                src_idx = module_parts.index('src')
                module_parts = module_parts[src_idx + 1:]

            # Remove .py extension
            module_parts[-1] = module_parts[-1][:-3]

            module_name = '.'.join(module_parts)
            modules.append((module_name, py_file))
        except BaseException:
            pass

    return modules


def test_imports():
    """Test importing all modules to find validator issues."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    packages_dir = project_root / 'packages'

    all_errors = []
    tested_modules = set()

    # Test each package
    for package_dir in sorted(packages_dir.iterdir()):
        if not package_dir.is_dir() or package_dir.name.startswith('.'):
            continue

        print(f"\n{'=' * 60}")
        print(f"Testing package: {package_dir.name}")
        print(f"{'=' * 60}")

        src_dir = package_dir / 'src'
        if not src_dir.exists():
            continue

        modules = find_python_modules(src_dir)

        for module_name, file_path in sorted(modules):
            if module_name in tested_modules:
                continue
            tested_modules.add(module_name)

            # Try to import the module
            cmd = [sys.executable, '-c', f"import {module_name}"]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(project_root),
                check=False,
            )

            if result.returncode != 0:
                error_text = result.stderr

                # Check if it's a validator error
                if 'PydanticUserError' in error_text and 'validator' in error_text:
                    # Extract the specific error
                    lines = error_text.strip().split('\n')
                    for i, line in enumerate(lines):
                        if 'PydanticUserError:' in line:
                            error_msg = line.split('PydanticUserError:')[1].strip()

                            # Try to find the exact location
                            location = 'Unknown'
                            if i + 1 < len(lines):
                                next_line = lines[i + 1]
                                if 'For further information' not in next_line:
                                    location = next_line.strip()

                            # Extract method name from error
                            method_match = None
                            if 'for <bound method' in error_msg:
                                method_part = error_msg.split('for <bound method')[1]
                                method_match = method_part.split(' of ')[0].strip()

                            all_errors.append(
                                {
                                    'module': module_name,
                                    'file': str(file_path),
                                    'error': error_msg,
                                    'method': method_match,
                                    'location': location,
                                },
                            )

                            print(f"\n❌ Validator error in {module_name}")
                            print(f"   File: {file_path}")
                            print(f"   Error: {error_msg}")
                            if method_match:
                                print(f"   Method: {method_match}")
                            break

    # Summary
    print(f"\n{'=' * 60}")
    print('SUMMARY OF ALL VALIDATOR ISSUES')
    print(f"{'=' * 60}")
    print(f"Total validator errors found: {len(all_errors)}")

    # Group by error type
    error_types = {}
    for error in all_errors:
        error_type = (
            error['error'].split(':')[0] if ':' in error['error'] else error['error']
        )
        if error_type not in error_types:
            error_types[error_type] = []
        error_types[error_type].append(error)

    print('\nErrors by type:')
    for error_type, errors in error_types.items():
        print(f"\n{error_type}: {len(errors)} errors")
        for err in errors[:3]:  # Show first 3
            print(f"  - {err['file']}")
            if err['method']:
                print(f"    Method: {err['method']}")

    # Save detailed report
    report_file = script_dir / 'validator_issues_report.txt'
    with open(report_file, 'w') as f:
        f.write('PYDANTIC VALIDATOR ISSUES REPORT\n')
        f.write('================================\n\n')

        for error in all_errors:
            f.write(f"Module: {error['module']}\n")
            f.write(f"File: {error['file']}\n")
            f.write(f"Error: {error['error']}\n")
            if error['method']:
                f.write(f"Method: {error['method']}\n")
            f.write('-' * 80 + '\n\n')

    print(f"\nDetailed report saved to: {report_file}")


if __name__ == '__main__':
    test_imports()
