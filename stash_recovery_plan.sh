#!/bin/bash
# SAFE STASH RECOVERY PLAN
# Generated: $(date)
# Preserves git timeline while recovering critical work

set -e

RECOVERY_DIR="recovery_catalog/20250729_205144/stashes"
BACKUP_BRANCH="backup/before_stash_recovery_$(date +%Y%m%d_%H%M%S)"

echo "🔄 SAFE STASH RECOVERY PLAN"
echo "Current branch: $(git branch --show-current)"
echo "Current commit: $(git rev-parse HEAD)"

# Create safety backup
echo "📦 Creating safety backup branch..."
git branch "$BACKUP_BRANCH"
echo "✅ Created backup: $BACKUP_BRANCH"

# Function to safely apply a stash with conflict detection
apply_stash_safely() {
    local stash_num=$1
    local description=$2
    
    echo ""
    echo "🔍 Analyzing stash_$stash_num: $description"
    
    # Check if stash exists
    if [[ ! -f "$RECOVERY_DIR/stash_$stash_num.patch" ]]; then
        echo "❌ Stash file not found: stash_$stash_num.patch"
        return 1
    fi
    
    # Show affected files
    echo "📁 Files in this stash:"
    if [[ -f "$RECOVERY_DIR/stash_${stash_num}_files.txt" ]]; then
        tail -n +8 "$RECOVERY_DIR/stash_${stash_num}_files.txt" | head -10
        local total_files=$(tail -n +8 "$RECOVERY_DIR/stash_${stash_num}_files.txt" | wc -l)
        if [[ $total_files -gt 10 ]]; then
            echo "   ... and $((total_files - 10)) more files"
        fi
    fi
    
    # Get file size
    local size=$(du -h "$RECOVERY_DIR/stash_$stash_num.patch" | cut -f1)
    echo "📊 Patch size: $size"
    
    # Ask for confirmation
    echo ""
    read -p "Apply this stash? [y/N/s(skip)/q(quit)]: " choice
    case $choice in
        [Yy]* )
            echo "🔄 Applying stash_$stash_num..."
            
            # Try to apply with 3-way merge
            if git apply --3way --index "$RECOVERY_DIR/stash_$stash_num.patch" 2>/dev/null; then
                echo "✅ Applied cleanly!"
                git add -A
                git commit -m "Recover stash_$stash_num: $description

Original stash from: $(head -4 "$RECOVERY_DIR/stash_${stash_num}_files.txt" | tail -1)
Recovery source: $RECOVERY_DIR/stash_$stash_num.patch"
            else
                echo "⚠️  Conflicts detected. Attempting manual resolution..."
                
                # Try without index first
                if git apply "$RECOVERY_DIR/stash_$stash_num.patch" 2>/dev/null; then
                    echo "✅ Applied to working tree. Please review and commit manually."
                    echo "📝 To commit: git add -A && git commit -m 'Recover stash_$stash_num: $description'"
                    read -p "Press Enter when ready to continue..."
                else
                    echo "❌ Cannot apply automatically. Conflicts need manual resolution."
                    echo "📁 Patch saved at: $RECOVERY_DIR/stash_$stash_num.patch"
                    echo "🛠️  Manual steps:"
                    echo "   1. git apply --reject $RECOVERY_DIR/stash_$stash_num.patch"
                    echo "   2. Resolve conflicts in *.rej files"
                    echo "   3. git add -A && git commit"
                    read -p "Continue with next stash? [y/N]: " continue_choice
                    [[ $continue_choice =~ ^[Yy]$ ]] || return 1
                fi
            fi
            ;;
        [Ss]* )
            echo "⏭️  Skipped stash_$stash_num"
            ;;
        [Qq]* )
            echo "🛑 Stopping recovery process"
            exit 0
            ;;
        * )
            echo "⏭️  Skipped stash_$stash_num (default)"
            ;;
    esac
}

echo ""
echo "🗂️  RECOVERY PLAN - RECOMMENDED ORDER:"
echo ""

# PHASE 1: Recent critical work (work backwards from most recent)
echo "📅 PHASE 1: Recent Critical Work (July 29, 2025)"
echo "   Priority: HIGH - These are your most recent commits"

apply_stash_safely "0" "emergency-checkpoint-before-direct-fixes-20250729_193759"
apply_stash_safely "1" "error-analyzer-checkpoint-20250729_193609" 
apply_stash_safely "2" "error-analyzer-checkpoint-20250729_191934"

echo ""
echo "📅 PHASE 2: Import Management & Syntax Fixes (July 29)"
echo "   Priority: HIGH - Core functionality improvements"

apply_stash_safely "10" "IMPORT_MANAGER_CHECKPOINT_20250729_174147 (8.7MB - MAJOR CHANGES)"
apply_stash_safely "7" "SYSTEMATIC_FIXER_MASTER_20250729_182340"
apply_stash_safely "8" "INDENTATION_FIX_autopep8_20250729_181355"

echo ""
echo "📅 PHASE 3: Large Documentation & Code Changes"
echo "   Priority: MEDIUM - Review carefully for conflicts"

apply_stash_safely "14" "WIP: Before testing unterminated string fixes (61MB - MASSIVE)"
apply_stash_safely "17" "Accidental changes - reverting to docs branch (319KB)"

echo ""
echo "✅ RECOVERY COMPLETE!"
echo ""
echo "🔍 SUMMARY:"
echo "   • Backup branch created: $BACKUP_BRANCH"
echo "   • Current branch: $(git branch --show-current)"
echo "   • Commits added: $(git rev-list --count $BACKUP_BRANCH..HEAD 2>/dev/null || echo '0')"
echo ""
echo "🛟 ROLLBACK INSTRUCTIONS (if needed):"
echo "   git reset --hard $BACKUP_BRANCH"
echo "   git branch -D $BACKUP_BRANCH"
echo ""
echo "🔧 NEXT STEPS:"
echo "   1. Test your recovered changes"
echo "   2. Run your pyright configuration (should be much cleaner now!)"
echo "   3. Consider applying remaining stashes manually if needed"
echo ""

# Show remaining stashes
echo "📋 REMAINING STASHES (apply manually if needed):"
for i in {3..30}; do
    if [[ -f "$RECOVERY_DIR/stash_${i}.patch" && ! "$i" =~ ^(7|8|10|14|17)$ ]]; then
        size=$(du -h "$RECOVERY_DIR/stash_$i.patch" | cut -f1)
        desc=$(sed -n '6p' "$RECOVERY_DIR/stash_${i}_files.txt" 2>/dev/null | sed 's/^[[:space:]]*//' || echo "No description")
        echo "   stash_$i ($size): $desc"
    fi
done

echo ""
echo "🎯 All done! Your git timeline is preserved and enhanced."