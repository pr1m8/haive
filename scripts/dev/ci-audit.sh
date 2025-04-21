#!/bin/bash

OUTPUT_FILE="ci-audit.txt"
echo "🔍 CI + Poetry Coverage & Security Audit"" > $OUTPUT_F"ILE
echo "======================================" >> "$OUTPUT_FILE"

echo -e "\n📦 Checking pyproject.toml for coverage/security tools..." ">> $OUTPUT_F"ILE
grep -iE 'pytest-cov|safety|mypy' pyproject.toml >> "$OUTPUT_FILE" || echo "❌ None found in pyproject.toml" >"> $OUTPUT_FI"LE

echo -e "\n🧪 Checking if coverage tools are locked in poetry.lock..." ">> $OUTPUT_F"ILE
grep -iE 'pytest-cov|safety' poetry.lock >> "$OUTPUT_FILE" || echo "❌ None found in poetry.lock" >"> $OUTPUT_FI"LE

echo -e "\n⚙️  Checking GitHub workflows for coverage/security hooks..."" >> $OUTPUT_"FILE
grep -iE 'pytest|cov|coverage|safety|codeql' .github/workflows/*.yml >> "$OUTPUT_FILE" || echo "❌ No relevant actions in workflows" >"> $OUTPUT_FI"LE

echo -e "\n📁 Checking noxfile.py for pytest --cov usage..." ">> $OUTPUT_F"ILE
if [[ -f "noxfile.py" ]]; then
  grep -i 'cov' noxfile.py >> "$OUTPUT_FILE" || echo "❌ No coverage usage in noxfile.py" >"> $OUTPUT_FI"LE
else
  echo "⚠️ noxfile.py not found"" >> $OUTPUT_"FILE
fi

echo -e "\n✅ Audit complete. Se${ $OUTPUT_FI}LE"
