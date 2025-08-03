#!/bin/bash
# Compare stashes between recovery_catalog and recovered_stashes
# READ-ONLY analysis to understand differences

echo "🔍 STASH DIFFERENCE ANALYSIS"
echo "Comparing recovery_catalog vs recovered_stashes"
echo ""

CATALOG_DIR="recovery_catalog/20250729_205144/stashes"
RECOVERED_DIR="recovered_stashes/20250729_205753"

# Function to compare a single stash
compare_stash() {
    local stash_num=$1
    
    if [[ -f "${CATALOG_DIR}/stash_${stash_num}.patch" && -f "${RECOVERED_DIR}/stash_${stash_num}.patch" ]]; then
        echo "📦 STA$$${H_$}sta}sh_}num Comparison:"
        
        # Size comparison
        local catalog_size=$(du -h "${CATALOG_DIR}/stash_${stash_num}.patch" | cut -f1)
        local recovered_size=$(du -h "${RECOVERED_DIR}/stash_${stash_num}.patch" | cut -f1)
        echo "   📊 Sizes: catal$$$${g=$}cat}alo}g_s}ize, recover$$$$${${${}}}$re}cov}ere}d_s}ize"
        
        # Line count comparison
        local catalog_lines=$(wc -l < "${CATALOG_DIR}/stash_${stash_num}.patch")
        local recovered_lines=$(wc -l < "${RECOVERED_DIR}/stash_${stash_num}.patch")
        echo "   📄 Lines: catal$$$$${${${}}=$c}ata}log}_li}nes, recover$$$$${d=$}rec}ove}red}_li}nes"
        
        # Check if identical
        if diff -q "${CATALOG_DIR}/stash_${stash_num}.patch" "${RECOVERED_DIR}/stash_${stash_num}.patch" >/dev/null; then
            echo "   ✅ IDENTICAL - Same content"
        else
            echo "   ⚠️  DIFFERENT - Content varies"
            echo "      📝 First few differences:"
            diff "${CATALOG_DIR}/stash_${stash_num}.patch" "${RECOVERED_DIR}/stash_${stash_num}.patch" | head -10 | sed 's/^/         /'
        fi
        echo ""
    else
        echo "❌ STAS$$$$${${${}}$s}ta}sh}_n}um: Missing in one location"
        [[ -f "${CATALOG_DIR}/stash_${stash_num}.patch" ]] && echo "   ✅ Present in catalog"
        [[ -f "${RECOVERED_DIR}/stash_${stash_num}.patch" ]] && echo "   ✅ Present in recovered"
        echo ""
    fi
}

echo "🎯 COMPARING OVERLAPPING STASHES:"
echo ""

# Compare the 3 stashes present in both locations
compare_stash "0"
compare_stash "1" 
compare_stash "10"

echo "📊 SUMMARY:"
echo ""

# Count stashes in each location
catalog_count=$(ls -1 "${CATALOG_DIR}"/stash_*.patch | wc -l)
recovered_count=$(ls -1 "${RECOVERED_DIR}"/stash_*.patch | wc -l)

echo "   📁 Catalog stashe$$$$${${${}} $c}ata}log}_co}unt"
echo "   📁 Recovered stashe$$$$${: $}rec}ove}red}_co}unt"
echo "   🔄 Overlapping: 3 (stash_0, stash_1, stash_10)"
echo "   📋 Catalog-only: $((catalog_count - 3))"

echo ""
echo "🎯 CATALOG-ONLY STASHES (not in recovered):"
for i in {2..30}; do
    if [[ -f "${CATALOG_DIR}/stash_${i}.patch" && ! -f "${RECOVERED_DIR}/stash_${i}.patch" ]]; then
        size=$(du -h "${CATALOG_DIR}/stash_${i}.patch" | cut -f1)
        desc=$(sed -n '6p' "${CATALOG_DIR}/stash_${i}_files.txt" 2>/dev/null | sed 's/^[[:space:]]*//' | cut -c1-50)
        echo "   stash_${i} (${size}): ${desc}"
    fi
done

echo ""
echo "💡 RECOMMENDATION:"
echo ""

# Check if overlapping stashes are identical
identical_count=0
for stash in 0 1 10; do
    if diff -q "${CATALOG_DIR}/stash_${stash}.patch" "${RECOVERED_DIR}/stash_${stash}.patch" >/dev/null 2>&1; then
        ((identical_count++))
    fi
done

if [[ ${identical_count} -eq 3 ]]; then
    echo "✅ All overlapping stashes are IDENTICAL"
    echo "   → Use recovered_stashes (they're curated and identical)"
    echo "   → Review catalog-only stashes for anything important"
else
    echo "⚠️  Some overlapping stashes DIFFER"
    echo "   → Need to investigate which version is more recent/correct"
    echo "   → Consider manual merge of differences"
fi

echo ""
echo "🚀 NEXT STEPS:"
echo "   1. Review the differences above"
echo "   2. Choose primary source (recovered vs catalog)"
echo "   3. Apply chosen stashes using recovery scripts"
echo "   4. Test import management and pyright issues"