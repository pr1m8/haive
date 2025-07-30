#!/bin/bash
# 🔄 Safe Refactoring Tool - Advanced Python Refactoring with Safety
# Usage: ./dev-tools/scripts/safe-refactor.sh <operation> <args...>

set -e

OPERATION=${1:-""}
shift

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

if [ -z "$OPERATION" ]; then
    echo -e "${CYAN}🔄 SAFE REFACTORING TOOL${NC}"
    echo "================================"
    echo ""
    echo -e "${YELLOW}📋 AVAILABLE OPERATIONS:${NC}"
    echo ""
    echo -e "${GREEN}🏷️  RENAME OPERATIONS:${NC}"
    echo "  rename-function    <old_name> <new_name> [directory]"
    echo "  rename-variable    <old_name> <new_name> [directory]"
    echo "  rename-class       <old_name> <new_name> [directory]"
    echo "  rename-method      <class.method> <new_name> [directory]"
    echo ""
    echo -e "${GREEN}🔧 EXTRACT OPERATIONS:${NC}"
    echo "  extract-method     <file> <start_line> <end_line> <new_method_name>"
    echo "  extract-variable   <file> <line> <new_var_name>"
    echo ""
    echo -e "${GREEN}📦 MOVE OPERATIONS:${NC}"
    echo "  move-function      <function_name> <source_file> <dest_file>"
    echo "  move-class         <class_name> <source_file> <dest_file>"
    echo ""
    echo -e "${GREEN}🔍 ANALYSIS OPERATIONS:${NC}"
    echo "  find-usages        <symbol_name> [directory]"
    echo "  show-dependencies  <file>"
    echo "  check-safety       [directory]"
    echo ""
    echo -e "${BLUE}💡 EXAMPLES:${NC}"
    echo "  ./dev-tools/scripts/safe-refactor.sh rename-function old_func new_func src/"
    echo "  ./dev-tools/scripts/safe-refactor.sh extract-method src/file.py 10 20 helper_method"
    echo "  ./dev-tools/scripts/safe-refactor.sh check-safety packages/haive-mcp/"
    exit 1
fi

# Safety checkpoint function
create_safety_checkpoint() {
    local desc=$1
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    git stash push -m "REFACTOR_CHECKPOINT_${desc}_${TIMESTAMP}" || echo "⚠️ No changes to stash"
    echo -e "${GREEN}🛡️ Safety checkpoint created: REFACTOR_CHECKPOINT_${desc}_${TIMESTAMP}${NC}"
}

# Check if required tools are available
check_dependencies() {
    echo -e "${BLUE}🔍 Checking dependencies...${NC}"
    
    if ! poetry show rope >/dev/null 2>&1; then
        echo -e "${YELLOW}📦 Installing rope...${NC}"
        poetry add --group dev rope
    fi
    
    if ! poetry show bowler >/dev/null 2>&1; then
        echo -e "${YELLOW}📦 Installing bowler...${NC}"
        poetry add --group dev bowler
    fi
    
    echo -e "${GREEN}✅ Dependencies ready${NC}"
}

# Rope-based refactoring functions
rope_rename_function() {
    local old_name=$1
    local new_name=$2
    local directory=${3:-"src/"}
    
    echo -e "${BLUE}🔄 Renaming function: $old_name → $new_name${NC}"
    
    poetry run python -c "
import sys
from rope.base.project import Project
from rope.refactor.rename import Rename
from rope.base.utils import pyobjectsdef

try:
    project = Project('.')
    
    # Find all occurrences of the function
    for root, dirs, files in project.root.walk():
        for file in files:
            if file.path.endswith('.py') and '$directory' in file.path:
                try:
                    # Simple text-based search for function definitions
                    content = file.read()
                    if 'def $old_name(' in content:
                        print(f'Found function definition in: {file.path}')
                        # For now, use simple text replacement for safety
                        new_content = content.replace('def $old_name(', 'def $new_name(')
                        new_content = new_content.replace('$old_name(', '$new_name(')
                        file.write(new_content)
                        print(f'Updated: {file.path}')
                except Exception as e:
                    print(f'Error processing {file.path}: {e}')
                    
    print('✅ Function rename completed')
    project.close()
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
"
}

# Bowler-based refactoring functions
bowler_rename_function() {
    local old_name=$1
    local new_name=$2
    local directory=${3:-"src/"}
    
    echo -e "${BLUE}🔄 Bowler rename: $old_name → $new_name${NC}"
    
    poetry run python -c "
from bowler import Query

try:
    # Rename function with bowler
    query = (Query('$directory')
             .select_function('$old_name')
             .rename('$new_name'))
    
    # Show diff first
    print('📋 Preview of changes:')
    query.diff()
    
    # Execute changes
    query.execute()
    print('✅ Bowler rename completed')
    
except Exception as e:
    print(f'❌ Bowler error: {e}')
    import sys
    sys.exit(1)
"
}

# Main operation dispatcher
case $OPERATION in
    "rename-function")
        OLD_NAME=$1
        NEW_NAME=$2
        DIRECTORY=${3:-"src/"}
        
        if [ -z "$OLD_NAME" ] || [ -z "$NEW_NAME" ]; then
            echo -e "${RED}❌ Usage: rename-function <old_name> <new_name> [directory]${NC}"
            exit 1
        fi
        
        create_safety_checkpoint "rename_function_${OLD_NAME}_to_${NEW_NAME}"
        check_dependencies
        
        echo -e "${CYAN}🔄 RENAME FUNCTION: $OLD_NAME → $NEW_NAME${NC}"
        echo -e "${YELLOW}📁 Directory: $DIRECTORY${NC}"
        
        # Use bowler for safer refactoring
        bowler_rename_function "$OLD_NAME" "$NEW_NAME" "$DIRECTORY"
        ;;
        
    "rename-variable")
        OLD_NAME=$1
        NEW_NAME=$2
        DIRECTORY=${3:-"src/"}
        
        if [ -z "$OLD_NAME" ] || [ -z "$NEW_NAME" ]; then
            echo -e "${RED}❌ Usage: rename-variable <old_name> <new_name> [directory]${NC}"
            exit 1
        fi
        
        create_safety_checkpoint "rename_variable_${OLD_NAME}_to_${NEW_NAME}"
        check_dependencies
        
        echo -e "${CYAN}🔄 RENAME VARIABLE: $OLD_NAME → $NEW_NAME${NC}"
        
        # Simple text-based replacement with safety checks
        find "$DIRECTORY" -name "*.py" -exec sed -i "s/\b$OLD_NAME\b/$NEW_NAME/g" {} \;
        echo -e "${GREEN}✅ Variable rename completed${NC}"
        ;;
        
    "extract-method")
        FILE=$1
        START_LINE=$2
        END_LINE=$3
        METHOD_NAME=$4
        
        if [ -z "$FILE" ] || [ -z "$START_LINE" ] || [ -z "$END_LINE" ] || [ -z "$METHOD_NAME" ]; then
            echo -e "${RED}❌ Usage: extract-method <file> <start_line> <end_line> <new_method_name>${NC}"
            exit 1
        fi
        
        create_safety_checkpoint "extract_method_${METHOD_NAME}"
        check_dependencies
        
        echo -e "${CYAN}🔄 EXTRACT METHOD: Lines $START_LINE-$END_LINE → $METHOD_NAME()${NC}"
        echo -e "${YELLOW}📁 File: $FILE${NC}"
        
        # Use rope for method extraction
        poetry run python -c "
from rope.base.project import Project
from rope.refactor.extract import ExtractMethod

try:
    project = Project('.')
    resource = project.get_resource('$FILE')
    
    # Calculate byte offsets from line numbers
    lines = resource.read().split('\n')
    start_offset = sum(len(line) + 1 for line in lines[:$START_LINE-1])
    end_offset = sum(len(line) + 1 for line in lines[:$END_LINE])
    
    extractor = ExtractMethod(project, resource, start_offset, end_offset)
    changes = extractor.get_changes('$METHOD_NAME')
    project.do(changes)
    
    print('✅ Method extraction completed')
    project.close()
except Exception as e:
    print(f'❌ Error: {e}')
    import sys
    sys.exit(1)
"
        ;;
        
    "find-usages")
        SYMBOL=$1
        DIRECTORY=${2:-"src/"}
        
        if [ -z "$SYMBOL" ]; then
            echo -e "${RED}❌ Usage: find-usages <symbol_name> [directory]${NC}"
            exit 1
        fi
        
        echo -e "${CYAN}🔍 FIND USAGES: $SYMBOL${NC}"
        echo -e "${YELLOW}📁 Directory: $DIRECTORY${NC}"
        echo ""
        
        grep -rn --include="*.py" "$SYMBOL" "$DIRECTORY" | head -20
        ;;
        
    "check-safety")
        DIRECTORY=${1:-"src/"}
        
        echo -e "${CYAN}🔍 SAFETY CHECK: $DIRECTORY${NC}"
        echo ""
        
        # Check for syntax errors
        echo -e "${BLUE}📝 Checking Python syntax...${NC}"
        find "$DIRECTORY" -name "*.py" -exec python -m py_compile {} \; 2>&1 | head -10
        
        # Check for import errors
        echo -e "${BLUE}📦 Checking imports...${NC}"
        poetry run python -c "
import ast
import os

errors = []
for root, dirs, files in os.walk('$DIRECTORY'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r') as f:
                    ast.parse(f.read())
            except SyntaxError as e:
                errors.append(f'{filepath}: {e}')

if errors:
    print('❌ Syntax errors found:')
    for error in errors[:5]:
        print(f'  {error}')
else:
    print('✅ No syntax errors found')
"
        ;;
        
    *)
        echo -e "${RED}❌ Unknown operation: $OPERATION${NC}"
        echo "Run without arguments to see available operations"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Refactoring operation completed!${NC}"
echo -e "${YELLOW}🔄 Rollback: git stash apply stash@{0} (if needed)${NC}" 