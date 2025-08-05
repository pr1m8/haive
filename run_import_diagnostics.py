#!/usr/bin/env python3
"""Run import diagnostics for Haive packages."""

from __future__ import annotations

import json
import os
import sys
import warnings
from pathlib import Path

from import_diagnostics import save_import_diagnosis

# Suppress warnings
os.environ["HAIVE_QUIET"] = "1"

warnings.filterwarnings("ignore")

# Add conf_modules to path
sys.path.insert(0, "docs/source/conf_modules")


def main():
    base_dir = Path.cwd()
    autoapi_dirs = [
        str(base_dir / "packages" / "haive-core" / "src"),
        str(base_dir / "packages" / "haive-agents" / "src"),
        str(base_dir / "packages" / "haive-tools" / "src"),
        str(base_dir / "packages" / "haive-games" / "src"),
        str(base_dir / "packages" / "haive-dataflow" / "src"),
        str(base_dir / "packages" / "haive-mcp" / "src"),
        str(base_dir / "packages" / "haive-prebuilt" / "src"),
    ]

    # Save to file
    save_import_diagnosis(autoapi_dirs, str(base_dir))

    # Find the latest diagnosis file
    diagnosis_files = sorted(
        [f for f in (base_dir / "docs" / "logs").glob("import_diagnosis_*.json")],
    )
    if not diagnosis_files:
        print("No diagnosis file found!")
        return

    diagnosis_file = diagnosis_files[-1]

    with open(diagnosis_file) as f:
        data = json.load(f)

    print("\n" + "=" * 80)
    print("📊 IMPORT DIAGNOSTICS SUMMARY")
    print("=" * 80)
    print(f"Total modules scanned: {data['summary']['total_modules']}")
    print(f"Successful imports: {data['summary']['successful_imports']}")
    print(f"Failed imports: {data['summary']['failed_imports']}")

    print("\n🔴 ERROR BREAKDOWN:")
    for error_type, count in data["summary"]["error_types"].items():
        print(f"  {error_type}: {count}")

    print("\n❌ MISSING MODULES (top 20):")
    missing = data["summary"].get("missing_modules", {})
    sorted_missing = sorted(missing.items(), key=lambda x: x[1], reverse=True)
    for module, count in sorted_missing[:20]:
        print(f"  {module}: {count} times")

    print("\n⚠️  IMPORT ERRORS (unique types):")
    seen_errors = set()
    for err in data["failed_imports"][:100]:
        error_msg = err["error"][:80] if err["error"] else "No error message"
        error_key = (err["error_type"], error_msg)
        if error_key not in seen_errors:
            seen_errors.add(error_key)
            print(f"\n  Module: {err['module']}")
            print(f"  Type: {err['error_type']}")
            print(
                f"  Error: {err['error'][:200] if err['error'] else 'No error message'}...",
            )
            if len(seen_errors) >= 15:
                break

    print(f"\n📝 Total mock imports generated: {len(data['mock_imports'])}")
    print(f"📄 Full report saved to: {diagnosis_file.name}")

    # Also save a summary report
    summary_file = diagnosis_file.with_name(
        diagnosis_file.stem.replace("diagnosis", "diagnosis_summary") + ".md",
    )
    with open(summary_file, "w") as f:
        f.write("# Import Diagnosis Summary\n\n")
        f.write(f"Generated: {data['timestamp']}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- Total modules: {data['summary']['total_modules']}\n")
        f.write(f"- Successful: {data['summary']['successful_imports']}\n")
        f.write(f"- Failed: {data['summary']['failed_imports']}\n\n")
        f.write("## Error Types\n\n")
        for error_type, count in data["summary"]["error_types"].items():
            f.write(f"- {error_type}: {count}\n")
        f.write("\n## Missing Modules\n\n")
        for module, count in sorted_missing[:30]:
            f.write(f"- {module}: {count} times\n")

    print(f"📄 Summary report saved to: {summary_file.name}")


if __name__ == "__main__":
    main()
