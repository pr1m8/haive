#!/usr/bin/env python3
"""Full diagnostic of AutoAPI issues."""

import os
import sys
from pathlib import Path
from fnmatch import fnmatch

# Setup paths like conf.py
docs_dir = Path(__file__).parent
project_root = docs_dir.parent.parent
packages_dir = project_root / "packages"

# Current ignore patterns from conf.py
autoapi_ignore = [
    "**/examples/**/*.py",
    "**/example*.py", 
    "**/*example*.py",
    "**/demos/**/*.py",
    "**/demo*.py",
    "**/test*.py",
    "**/tests/**/*.py",
    "**/*.py.backup*",
    "**/*.backup", 
    "**/*.disabled",
    "**/auto_examples/**",
    "**/app.py",
    "**/app/**/*.py",
    "**/archive/**",
    "**/archives/**",
]

def analyze_ignore_impact():
    """Analyze what the ignore patterns exclude."""
    print("🔍 Analyzing ignore pattern impact...")
    
    all_files = []
    for pkg_path in packages_dir.glob("haive-*/src"):
        pkg_files = list(pkg_path.rglob("*.py"))
        all_files.extend([(f, pkg_path.name) for f in pkg_files])
    
    excluded_files = []
    important_excluded = []
    
    for file_path, pkg_name in all_files:
        rel_path = file_path.relative_to(packages_dir)
        
        is_excluded = False
        for pattern in autoapi_ignore:
            if (fnmatch(str(file_path), pattern) or 
                fnmatch(str(rel_path), pattern) or
                fnmatch(file_path.name, pattern)):
                is_excluded = True
                break
        
        if is_excluded:
            excluded_files.append(str(rel_path))
            # Check if it's an important file being excluded
            if (file_path.name == "app.py" or 
                "agent" in str(file_path).lower() or
                "config" in str(file_path).lower()):
                important_excluded.append(str(rel_path))
    
    total_files = len(all_files)
    excluded_count = len(excluded_files)
    included_count = total_files - excluded_count
    
    print(f"📊 File Analysis Results:")
    print(f"   Total Python files: {total_files}")
    print(f"   Excluded by patterns: {excluded_count} ({excluded_count/total_files*100:.1f}%)")
    print(f"   Included for documentation: {included_count}")
    
    if important_excluded:
        print(f"\n🚨 Important files being excluded:")
        for f in important_excluded[:10]:
            print(f"   - {f}")
        if len(important_excluded) > 10:
            print(f"   ... and {len(important_excluded) - 10} more")
    
    return {
        "total": total_files,
        "excluded": excluded_count,
        "included": included_count,
        "important_excluded": important_excluded
    }

def test_core_imports():
    """Test if core modules can be imported."""
    print("\n🧪 Testing core module imports...")
    
    sys.path.insert(0, str(packages_dir))
    for pkg_dir in packages_dir.glob("haive-*/src"):
        sys.path.insert(0, str(pkg_dir))
    
    test_modules = [
        "haive.core",
        "haive.core.config",
        "haive.core.engine",
        "haive.agents",
        "haive.tools", 
        "haive.games",
    ]
    
    results = {}
    for module in test_modules:
        try:
            imported = __import__(module)
            results[module] = "✅ SUCCESS"
        except ImportError as e:
            results[module] = f"❌ IMPORT ERROR: {str(e)[:100]}"
        except Exception as e:
            results[module] = f"⚠️  OTHER ERROR: {str(e)[:100]}"
    
    for module, result in results.items():
        print(f"   {module}: {result}")
    
    return results

def check_mock_impact():
    """Check which mocked modules exist in the codebase."""
    print("\n🎭 Analyzing mock imports impact...")
    
    # Key mocks from conf.py that might be problematic
    problematic_mocks = [
        "haive.agents.base.agent",
        "haive.agents.base", 
        "haive.agents",
        "haive.core.schema.prebuilt.messages_state",
    ]
    
    existing_mocks = []
    for mock in problematic_mocks:
        mock_path = mock.replace(".", "/") + ".py"
        for pkg_dir in packages_dir.glob("haive-*/src"):
            potential_file = pkg_dir / mock_path
            if potential_file.exists():
                existing_mocks.append((mock, potential_file))
    
    print(f"🚨 Critical mocked modules that exist:")
    for mock, path in existing_mocks:
        print(f"   {mock} -> {path.relative_to(packages_dir)}")
    
    return existing_mocks

if __name__ == "__main__":
    print("🔬 Full AutoAPI Diagnostic")
    print("=" * 60)
    
    # Test 1: Ignore patterns
    ignore_results = analyze_ignore_impact()
    
    # Test 2: Import capabilities  
    import_results = test_core_imports()
    
    # Test 3: Mock analysis
    mock_results = check_mock_impact()
    
    # Summary
    print(f"\n📋 DIAGNOSTIC SUMMARY")
    print(f"=" * 60)
    print(f"• Files available for documentation: {ignore_results['included']}")
    print(f"• Important files excluded: {len(ignore_results['important_excluded'])}")
    print(f"• Core modules importable: {sum(1 for r in import_results.values() if '✅' in r)}/{len(import_results)}")
    print(f"• Critical mocked modules: {len(mock_results)}")
    
    if ignore_results['important_excluded'] or mock_results:
        print(f"\n🚨 LIKELY ROOT CAUSES:")
        if ignore_results['important_excluded']:
            print(f"   1. Ignore patterns excluding important files")
        if mock_results:
            print(f"   2. Core modules being mocked, preventing AutoAPI processing")