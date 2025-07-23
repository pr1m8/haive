#!/bin/bash

# Extract all remaining missing files from the recovered Git tree
TREE_HASH="99050ac33e9516651f8d02c3d92886d1b7be16f6"
BASE_DIR="src/haive/agents"

echo "🔄 Extracting remaining missing files from Git tr${e $TREE_H}ASH"

# Function to extract and create file
extract_file() {
	local blob_hash=$1
	local target_path=$2
	local display_path=$3

	# Create directory if it doesn't exist
	mkdir -p "$(dirname "${target_path}")"

	# Extract file
	if git show "${blob_hash}" >"${target_path}" 2>/dev/null; then
		echo "✅ Extracted${ $display_pa}th"
		return 0
	else
		echo "❌ Failed${ $display_pa}th"
		return 1
	fi
}

# Count files
total_files=0
extracted_files=0

echo "📁 EXTRACTING MULTI AGENT FILES:"

# Enhanced Multi Agent files
extract_file "27648728ac21e7a9d5c366b6e2f28cd98d10d4c4" "${BASE_DIR}/multi/enhanced_multi_agent_v3.py" "multi/enhanced_multi_agent_v3.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "1c7d2f79b0645847dea1c89e3de862aa22f85dd1" "${BASE_DIR}/multi/enhanced_parallel_agent.py" "multi/enhanced_parallel_agent.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "cbdcfd05787c70fb98429ffb3c811f7cc780af7f" "${BASE_DIR}/multi/enhanced_sequential_agent.py" "multi/enhanced_sequential_agent.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "3112873bcfb650b905e499c2846350578608bae5" "${BASE_DIR}/multi/enhanced_supervisor_agent.py" "multi/enhanced_supervisor_agent.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "df54d0109771abe3d8b27e4930c93a5bda65e679" "${BASE_DIR}/multi/enhanced_dynamic_supervisor.py" "multi/enhanced_dynamic_supervisor.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "68c5237423c515bf5c4df898f11796566182b96d" "${BASE_DIR}/multi/enhanced_clean_multi_agent.py" "multi/enhanced_clean_multi_agent.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "512b9074a46f86254593a7d0028e26d7b82cb4fc" "${BASE_DIR}/multi/clean.py" "multi/clean.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

# Multi Archive files
extract_file "b067d1001e2b42ccc9efa49a8821215d24ab48e9" "${BASE_DIR}/multi/archive/base.py" "multi/archive/base.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "4228e83c4f2f13395071eb6cf6e0dcb2eae0a16d" "${BASE_DIR}/multi/archive/example.py" "multi/archive/example.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "07ae04bce728701644371258a965ac602263514c" "${BASE_DIR}/multi/archive/configurable_base.py" "multi/archive/configurable_base.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "0e76c0ab3f974af1989666b0f9925ad5d2aa0b4e" "${BASE_DIR}/multi/archive/enhanced_base.py" "multi/archive/enhanced_base.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

echo ""
echo "📁 EXTRACTING PLANNING FILES:"

# Planning LLM Compiler (original)
extract_file "20931bd2a239560a2e81c86a17bc6a53ba6998fc" "${BASE_DIR}/planning/llm_compiler/agent.py" "planning/llm_compiler/agent.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "df2d955e39251dec33468600c77a8b3a42133833" "${BASE_DIR}/planning/llm_compiler/aug_llms.py" "planning/llm_compiler/aug_llms.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "31ce5272ec1b015bec809b0f1fdc41368fa41069" "${BASE_DIR}/planning/llm_compiler/config.py" "planning/llm_compiler/config.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "bdb73ae43fddb5536a13735c4605b5ebdb658d8b" "${BASE_DIR}/planning/llm_compiler/models.py" "planning/llm_compiler/models.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "e736b0cde0fffd692d94e73cddab292cd89106c0" "${BASE_DIR}/planning/llm_compiler/output_parser.py" "planning/llm_compiler/output_parser.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "92b21741b3c47b5fcf54f88e337d35678fe8cce4" "${BASE_DIR}/planning/llm_compiler/state.py" "planning/llm_compiler/state.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "2b4e58be348c722cd49195e156b645708f285c2f" "${BASE_DIR}/planning/llm_compiler/utils.py" "planning/llm_compiler/utils.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

# LLM Compiler tools
extract_file "aac17c8b7af3fab54f2e437536e040697a0998c0" "${BASE_DIR}/planning/llm_compiler/tools/math_tools.py" "planning/llm_compiler/tools/math_tools.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

# LLM Compiler V3 examples
extract_file "93550d770be49fc53e266b34d121131a0fa724c7" "${BASE_DIR}/planning/llm_compiler_v3/examples/basic_example.py" "planning/llm_compiler_v3/examples/basic_example.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

# Plan and Execute (p_and_e)
extract_file "137ec6536ed4671f6224304cbcbc036be48c2aa6" "${BASE_DIR}/planning/p_and_e/agent.py" "planning/p_and_e/agent.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "198601ae6a9934540a1d331035ce50d0a834fef0" "${BASE_DIR}/planning/p_and_e/engines.py" "planning/p_and_e/engines.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "1b9dbf6a88671e7a11034874018e2b2cdc404a21" "${BASE_DIR}/planning/p_and_e/example.py" "planning/p_and_e/example.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

# Additional planning files
extract_file "ebbbb88f21211faeca09aff334cb731c9449aef7" "${BASE_DIR}/planning/clean_plan_execute.py" "planning/clean_plan_execute.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "5729b012bcc2804c1356ad72c272433fb6e4a383" "${BASE_DIR}/planning/langgraph_plan_execute.py" "planning/langgraph_plan_execute.py"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

echo ""
echo "📁 EXTRACTING README AND DOCUMENTATION FILES:"

extract_file "48c4e45a8b94bb201a3a9cd7b5b2399a4287510e" "${BASE_DIR}/multi/MULTI_AGENT_GUIDE.md" "multi/MULTI_AGENT_GUIDE.md"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "068642f374aea781b47763c175c44063986c887e" "${BASE_DIR}/multi/README_COMPREHENSIVE.md" "multi/README_COMPREHENSIVE.md"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "398565f58be8af273b180975abdcad158163b92a" "${BASE_DIR}/multi/README_STRUCTURE.md" "multi/README_STRUCTURE.md"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "f308d942d143b4ff7dd726b00514d3122c5bae39" "${BASE_DIR}/planning/PLANNING_AGENT_MEMORY_GUIDE.md" "planning/PLANNING_AGENT_MEMORY_GUIDE.md"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "05abbe0165b0841f2782ab221185aeeb9ff6b1f7" "${BASE_DIR}/planning/llm_compiler/README.md" "planning/llm_compiler/README.md"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

extract_file "295805770be803555949bf2747e38996113d39b4" "${BASE_DIR}/planning/llm_compiler_v3/README.md" "planning/llm_compiler_v3/README.md"
total_files=$((total_files + 1))
if [[ $? -eq 0 ]]; then extracted_files=$((extracted_files + 1)); fi

echo ""
echo "📊 EXTRACTION SUMMARY:"
echo "✅ Extracted${ $extracted_fil}es files"
echo "❌ Failed: $((total_files - extracted_files)) files"
echo "📈 Success Rate: $((extracted_files * 100 / total_files))%"

if [[ "$extracted_files" -gt 0 ]]; then
	echo ""
	echo "🎯 NEXT STEPS:"
	echo "1. Check extracted files are properly formatted"
	echo "2. Run linting on new files"
	echo "3. Update __init__.py files as needed"
	echo "4. Test imports work correctly"
fi
