from agents.coding.self_healing_code.state import SelfHealingCodeState
from langgraph.graph import END


def error_router(state: SelfHealingCodeState):
    if state.error:
        return "bug_report_node"
    return END


def memory_filter_router(state: SelfHealingCodeState):
    if state.memory_search_results:
        return "memory_filter_node"
    return "memory_generation_node"


def memory_generation_router(state: SelfHealingCodeState):
    if state.memory_ids_to_update:
        return "memory_modification_node"
    return "memory_generation_node"


def memory_update_router(state: SelfHealingCodeState):
    if state.memory_ids_to_update:
        return "memory_modification_node"
    return "code_update_node"
