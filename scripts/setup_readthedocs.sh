#!/usr/bin/env bash
# Import all haive packages into ReadTheDocs via API.
#
# Usage:
#   export RTD_TOKEN=your-rtd-api-token  # Get from https://readthedocs.org/accounts/tokens/
#   bash scripts/setup_readthedocs.sh
#
# Or manually import via web UI (each repo takes ~30s):
#   https://readthedocs.org/dashboard/import/?query=pr1m8
#
# After import, RTD auto-detects .readthedocs.yaml and starts building.

set -e

if [ -z "$RTD_TOKEN" ]; then
    echo "RTD_TOKEN not set. Manual import links:"
    for repo in haive-core haive-agents haive-games haive-tools haive-hap haive-dataflow haive-mcp; do
        echo "  https://readthedocs.org/dashboard/import/manual/?name=$repo&repo=https://github.com/pr1m8/$repo"
    done
    echo ""
    echo "Or set RTD_TOKEN and re-run this script."
    exit 0
fi

for repo in haive-core haive-agents haive-games haive-tools haive-hap haive-dataflow haive-mcp; do
    echo "=== Importing $repo ==="
    curl -s -X POST "https://readthedocs.org/api/v3/projects/" \
        -H "Authorization: Token $RTD_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"$repo\",
            \"repository\": {
                \"url\": \"https://github.com/pr1m8/$repo\",
                \"type\": \"git\"
            },
            \"homepage\": \"https://pypi.org/project/$repo/\",
            \"programming_language\": \"py\",
            \"language\": \"en\"
        }" | jq -r '.name // .detail // "Failed"' 2>/dev/null || echo "import attempted"
done

echo ""
echo "Done! Check https://readthedocs.org/dashboard/ for build status."
