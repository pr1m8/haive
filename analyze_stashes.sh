#!/bin/bash
# STASH ANALYSIS TOOL - READ ONLY
# Shows what's in each stash without applying anything

RECOVERY_DIR="recovery_catalog/20250729_205144/stashes"

echo "🔍 STASH ANALYSIS REPORT"
echo "Date: $(date)"
echo "Total stashes found: $(ls -1 $RECOVERY_DIR/stash_*.patch | wc -l)"
echo ""

# Function to analyze a single stash
analyze_stash() {
    local stash_num=$1
    
    if [[ ! -f "$RECOVERY_DIR/stash_$stash_num.patch" ]]; then
        return
    fi
    
    local size=$(du -h "$RECOVERY_DIR/stash_$stash_num.patch" | cut -f1)
    local date_line=$(sed -n '4p' "$RECOVERY_DIR/stash_${stash_num}_files.txt" 2>/dev/null)
    local desc_line=$(sed -n '6p' "$RECOVERY_DIR/stash_${stash_num}_files.txt" 2>/dev/null | sed 's/^[[:space:]]*//')
    
    # Count files in this stash
    local file_count=0
    if [[ -f "$RECOVERY_DIR/stash_${stash_num}_files.txt" ]]; then
        file_count=$(tail -n +8 "$RECOVERY_DIR/stash_${stash_num}_files.txt" 2>/dev/null | wc -l)
    fi
    
    echo "📦 STASH_$stash_num ($size, $file_count files)"
    echo "   📅 $date_line"
    echo "   📝 $desc_line"
    
    # Show key files if available
    if [[ -f "$RECOVERY_DIR/stash_${stash_num}_files.txt" && $file_count -gt 0 ]]; then
        echo "   📁 Key files:"
        tail -n +8 "$RECOVERY_DIR/stash_${stash_num}_files.txt" 2>/dev/null | head -3 | sed 's/^/      /'
        if [[ $file_count -gt 3 ]]; then
            echo "      ... and $((file_count - 3)) more files"
        fi
    fi
    echo ""
}

echo "🎯 PRIORITY STASHES (Recommended order):"
echo ""

echo "🔥 PHASE 1: Recent Emergency Checkpoints"
analyze_stash "0"
analyze_stash "1" 
analyze_stash "2"

echo "🔧 PHASE 2: Major System Changes"
analyze_stash "10"
analyze_stash "14"
analyze_stash "17"

echo "⚙️  PHASE 3: Systematic Fixes"
analyze_stash "7"
analyze_stash "8"
analyze_stash "5"

echo "📚 PHASE 4: Documentation & Config"
analyze_stash "3"
analyze_stash "4"
analyze_stash "6"

echo ""
echo "📊 ALL STASHES BY SIZE:"
echo ""

# Show all stashes sorted by size
for patch_file in $(ls -S $RECOVERY_DIR/stash_*.patch); do
    stash_num=$(basename "$patch_file" .patch | sed 's/stash_//')
    size=$(du -h "$patch_file" | cut -f1)
    desc=$(sed -n '6p' "$RECOVERY_DIR/stash_${stash_num}_files.txt" 2>/dev/null | sed 's/^[[:space:]]*//' | cut -c1-60)
    echo "   stash_$stash_num ($size): $desc"
done

echo ""
echo "🎯 RECOMMENDATIONS:"
echo ""
echo "1. 🚨 CRITICAL: Start with stash_0, stash_1, stash_2 (most recent emergency saves)"
echo "2. 🔧 MAJOR: Apply stash_10 (8.7MB import manager) and stash_14 (61MB fixes)"
echo "3. ⚠️  CAREFUL: stash_17 mentions 'accidental changes' - review before applying"
echo "4. 🧹 CLEANUP: Remaining stashes are smaller incremental changes"
echo ""
echo "⚡ TO PROCEED:"
echo "   Review this analysis, then run: ./stash_recovery_plan.sh"
echo ""
echo "🛟 SAFETY:"
echo "   The recovery script creates backup branches before any changes"
echo "   Your current git timeline will be preserved"