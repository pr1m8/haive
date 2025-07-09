# LTM Branching Logic & Conditional Flow

## Overview

This document details the branching logic, conditional flows, and decision points in the LTM agent workflow. The branching system ensures flexible, configuration-driven processing while maintaining robustness.

## Branching Categories

### 1. Configuration-Driven Branching

Routes based on agent configuration settings

### 2. Content-Driven Branching

Routes based on conversation content and context

### 3. Quality-Driven Branching

Routes based on processing quality and confidence scores

### 4. User-Driven Branching

Routes based on user interactions and tool requests

### 5. Error-Driven Branching

Routes for error handling and recovery

## Detailed Branching Logic

### 1. Main Processing Flow Branches

#### Primary Flow Decision Tree

```python
def determine_next_processing_step(state: LTMState) -> str:
    """Determine the next processing step based on current state and configuration."""

    # Check if memory extraction was successful
    if not state.extracted_memories:
        if state.processing_errors:
            return "handle_extraction_failure"
        else:
            return "end"  # No memories to process

    # Process based on enabled features
    if state.enable_kg_processing and not state.knowledge_graph:
        return "process_kg"
    elif state.enable_categorization and not state.categories:
        return "categorize_memories"
    elif state.enable_consolidation and should_consolidate(state):
        return "consolidate_memories"
    else:
        return "store_memories"

def should_consolidate(state: LTMState) -> bool:
    """Determine if consolidation should be performed."""
    memories = state.extracted_memories
    threshold = getattr(state, 'consolidation_threshold', 5)

    # Check memory count threshold
    if len(memories) < threshold:
        return False

    # Check for similar memories
    if has_similar_memories(memories):
        return True

    # Check categories for consolidation opportunities
    if state.categories and has_overcrowded_categories(state.categories, memories):
        return True

    return False

def has_similar_memories(memories: list[dict]) -> bool:
    """Check if memories have high similarity for consolidation."""
    if len(memories) < 2:
        return False

    # Calculate semantic similarity between memories
    similarities = calculate_memory_similarities(memories)
    high_similarity_threshold = 0.8

    return any(sim > high_similarity_threshold for sim in similarities)

def has_overcrowded_categories(categories: list[str], memories: list[dict]) -> bool:
    """Check if any category has too many memories."""
    category_counts = {}
    for memory in memories:
        for category in memory.get('categories', []):
            category_counts[category] = category_counts.get(category, 0) + 1

    max_memories_per_category = 20
    return any(count > max_memories_per_category for count in category_counts.values())
```

#### KG Processing Branch

```python
def should_process_kg(state: LTMState) -> str:
    """Determine KG processing path."""

    # Check if KG processing is enabled
    if not getattr(state, 'enable_kg_processing', True):
        return determine_next_after_kg(state)

    # Check if we have content suitable for KG
    memories = state.extracted_memories
    if not memories:
        return determine_next_after_kg(state)

    # Check if memories contain entities worth extracting
    if not contains_extractable_entities(memories):
        return determine_next_after_kg(state)

    # Check resource constraints
    if should_skip_kg_for_resources(state):
        return determine_next_after_kg(state)

    return "process_kg"

def contains_extractable_entities(memories: list[dict]) -> bool:
    """Check if memories contain content suitable for entity extraction."""
    entity_indicators = [
        'person', 'people', 'organization', 'company', 'place', 'location',
        'event', 'date', 'time', 'product', 'technology', 'concept'
    ]

    for memory in memories:
        content = memory.get('content', '').lower()
        if any(indicator in content for indicator in entity_indicators):
            return True

    return False

def should_skip_kg_for_resources(state: LTMState) -> bool:
    """Check if KG processing should be skipped due to resource constraints."""
    # Skip for very large memory sets to avoid timeout
    if len(state.extracted_memories) > 50:
        return True

    # Skip if previous KG processing failed recently
    if has_recent_kg_failures(state):
        return True

    return False

def determine_next_after_kg(state: LTMState) -> str:
    """Determine next step after KG processing decision."""
    if getattr(state, 'enable_categorization', True):
        return "categorize_memories"
    elif getattr(state, 'enable_consolidation', True) and should_consolidate(state):
        return "consolidate_memories"
    else:
        return "store_memories"
```

#### Categorization Branch

```python
def should_categorize(state: LTMState) -> str:
    """Determine categorization path."""

    # Check if categorization is enabled
    if not getattr(state, 'enable_categorization', True):
        return determine_next_after_categorization(state)

    # Check if we have enough memories for meaningful categorization
    memories = state.extracted_memories
    min_memories_for_categorization = 3
    if len(memories) < min_memories_for_categorization:
        return determine_next_after_categorization(state)

    # Check if memories are diverse enough for categorization
    if not has_diverse_content(memories):
        return determine_next_after_categorization(state)

    return "categorize_memories"

def has_diverse_content(memories: list[dict]) -> bool:
    """Check if memories have diverse content worth categorizing."""
    if len(memories) < 3:
        return False

    # Simple diversity check based on content keywords
    keywords_per_memory = []
    for memory in memories:
        content = memory.get('content', '').lower()
        keywords = extract_keywords(content)
        keywords_per_memory.append(set(keywords))

    # Calculate diversity as average unique keywords per memory
    all_keywords = set()
    for keywords in keywords_per_memory:
        all_keywords.update(keywords)

    avg_unique_ratio = len(all_keywords) / len(memories)
    return avg_unique_ratio > 2  # At least 2 unique keywords per memory on average

def determine_next_after_categorization(state: LTMState) -> str:
    """Determine next step after categorization decision."""
    if getattr(state, 'enable_consolidation', True) and should_consolidate(state):
        return "consolidate_memories"
    else:
        return "store_memories"
```

### 2. Tool Interaction Branches

#### Tool Activation Logic

```python
def should_activate_tools(state: LTMState) -> str:
    """Determine if memory tools should be activated."""

    # Check if tools are enabled
    if not getattr(state, 'create_memory_tools', True):
        return "end"

    # Check for explicit tool requests in conversation
    if has_explicit_tool_request(state):
        return "memory_tools"

    # Check for implicit memory operations
    if has_implicit_memory_request(state):
        return "memory_tools"

    # Check if user is asking questions that could benefit from memory search
    if has_memory_search_intent(state):
        return "memory_tools"

    return "end"

def has_explicit_tool_request(state: LTMState) -> bool:
    """Check for explicit tool usage requests."""
    if not state.messages:
        return False

    last_message = state.messages[-1].content.lower()

    explicit_requests = [
        'search my memories', 'find in memory', 'look up',
        'remember when', 'recall', 'what do you know about',
        'delete memory', 'update memory', 'forget',
        'show me memories', 'browse memories', 'memory search'
    ]

    return any(request in last_message for request in explicit_requests)

def has_implicit_memory_request(state: LTMState) -> bool:
    """Check for implicit memory operation requests."""
    if not state.messages:
        return False

    last_message = state.messages[-1].content.lower()

    implicit_patterns = [
        'do you remember', 'you mentioned before', 'we talked about',
        'last time we discussed', 'you know i like', 'my preference',
        'as i told you', 'i previously said'
    ]

    return any(pattern in last_message for pattern in implicit_patterns)

def has_memory_search_intent(state: LTMState) -> bool:
    """Check if user is asking questions that could benefit from memory search."""
    if not state.messages:
        return False

    last_message = state.messages[-1].content.lower()

    # Questions that might be answered by searching memories
    search_intent_patterns = [
        'what is my', 'what are my', 'tell me about my',
        'how do i', 'what should i', 'recommend',
        'based on my', 'considering my', 'given my'
    ]

    return any(pattern in last_message for pattern in search_intent_patterns)
```

#### Tool Flow Control

```python
def determine_tool_flow(state: LTMState) -> str:
    """Control tool interaction flow."""

    tool_results = getattr(state, 'tool_results', [])

    # First tool interaction
    if not tool_results:
        return classify_initial_tool_request(state)

    # Analyze last tool result for continuation
    last_result = tool_results[-1]

    # Check if user expressed satisfaction
    if indicates_satisfaction(state, last_result):
        return "end"

    # Check if user wants to refine/continue
    if indicates_continuation_intent(state, last_result):
        return classify_follow_up_request(state, last_result)

    # Check for new tool requests
    if has_new_tool_request(state):
        return classify_new_tool_request(state)

    # Default to ending if no clear continuation
    return "end"

def classify_initial_tool_request(state: LTMState) -> str:
    """Classify the type of initial tool request."""
    last_message = state.messages[-1].content.lower()

    if any(word in last_message for word in ['search', 'find', 'look', 'recall']):
        return "search_tool"
    elif any(word in last_message for word in ['remember', 'save', 'store']):
        return "manage_tool"
    elif any(word in last_message for word in ['browse', 'explore', 'show']):
        return "browse_tool"
    elif any(word in last_message for word in ['delete', 'forget', 'remove']):
        return "manage_tool"
    else:
        return "search_tool"  # Default to search

def indicates_satisfaction(state: LTMState, last_result: dict) -> bool:
    """Check if user indicates satisfaction with tool results."""
    if not state.messages:
        return False

    last_message = state.messages[-1].content.lower()

    satisfaction_indicators = [
        'thank you', 'thanks', 'perfect', 'exactly', 'that\'s right',
        'great', 'excellent', 'good', 'helpful', 'that works'
    ]

    return any(indicator in last_message for indicator in satisfaction_indicators)

def indicates_continuation_intent(state: LTMState, last_result: dict) -> bool:
    """Check if user wants to continue or refine the interaction."""
    if not state.messages:
        return False

    last_message = state.messages[-1].content.lower()

    continuation_indicators = [
        'but', 'however', 'actually', 'also', 'what about',
        'can you also', 'now', 'next', 'more', 'other'
    ]

    return any(indicator in last_message for indicator in continuation_indicators)
```

### 3. Error Recovery Branches

#### Error Classification and Recovery

```python
def handle_processing_error(state: LTMState, error_stage: str, error: Exception) -> str:
    """Handle errors during processing with appropriate recovery strategies."""

    error_type = classify_error(error)
    error_severity = assess_error_severity(error, error_stage)

    # Log error for monitoring
    log_processing_error(error_stage, error_type, error_severity, state)

    # Determine recovery strategy
    if error_severity == "critical":
        return handle_critical_error(state, error_stage, error)
    elif error_severity == "moderate":
        return handle_moderate_error(state, error_stage, error)
    else:
        return handle_minor_error(state, error_stage, error)

def classify_error(error: Exception) -> str:
    """Classify the type of error for appropriate handling."""
    error_type = type(error).__name__
    error_message = str(error).lower()

    if 'timeout' in error_message or 'time' in error_message:
        return "timeout"
    elif 'api' in error_message or 'rate limit' in error_message:
        return "api_error"
    elif 'memory' in error_message or 'out of memory' in error_message:
        return "resource_error"
    elif 'validation' in error_message or 'schema' in error_message:
        return "validation_error"
    elif 'connection' in error_message or 'network' in error_message:
        return "network_error"
    else:
        return "unknown_error"

def assess_error_severity(error: Exception, stage: str) -> str:
    """Assess the severity of an error in context."""
    error_type = classify_error(error)

    # Critical errors that stop the workflow
    if stage == "memory_extraction" and error_type in ["api_error", "timeout"]:
        return "critical"

    if stage == "store_memories" and error_type in ["network_error", "resource_error"]:
        return "critical"

    # Moderate errors that can be worked around
    if stage in ["process_kg", "categorize_memories"] and error_type == "timeout":
        return "moderate"

    if error_type == "validation_error":
        return "moderate"

    # Minor errors that don't significantly impact functionality
    return "minor"

def handle_critical_error(state: LTMState, stage: str, error: Exception) -> str:
    """Handle critical errors that require workflow termination or major fallback."""

    if stage == "memory_extraction":
        # Can't continue without memories
        return "end_with_error"

    elif stage == "store_memories":
        # Try alternative storage or partial save
        if should_retry_storage(error):
            return "retry_storage"
        else:
            return "partial_storage_fallback"

    else:
        # For other stages, skip to storage with partial results
        return "store_memories"

def handle_moderate_error(state: LTMState, stage: str, error: Exception) -> str:
    """Handle moderate errors with graceful degradation."""

    # Add error to state for user awareness
    state.processing_errors.append(f"{stage}: {str(error)}")
    state.partial_success = True

    if stage == "process_kg":
        # Skip KG processing, continue with categorization
        return determine_next_after_kg(state)

    elif stage == "categorize_memories":
        # Skip categorization, continue with consolidation or storage
        return determine_next_after_categorization(state)

    elif stage == "consolidate_memories":
        # Skip consolidation, go directly to storage
        return "store_memories"

    else:
        # Continue to next logical step
        return determine_next_processing_step(state)

def handle_minor_error(state: LTMState, stage: str, error: Exception) -> str:
    """Handle minor errors with minimal impact."""

    # Log error but continue processing
    state.processing_errors.append(f"{stage} (minor): {str(error)}")

    # Continue with normal flow
    return determine_next_processing_step(state)
```

### 4. Quality-Driven Branches

#### Quality Assessment and Routing

```python
def assess_processing_quality(state: LTMState, stage: str) -> str:
    """Assess quality of processing results and route accordingly."""

    quality_score = calculate_quality_score(state, stage)
    quality_threshold = get_quality_threshold(stage)

    if quality_score < quality_threshold:
        return handle_low_quality(state, stage, quality_score)
    else:
        return continue_normal_flow(state, stage)

def calculate_quality_score(state: LTMState, stage: str) -> float:
    """Calculate quality score for processing stage results."""

    if stage == "memory_extraction":
        return assess_extraction_quality(state)
    elif stage == "process_kg":
        return assess_kg_quality(state)
    elif stage == "categorize_memories":
        return assess_categorization_quality(state)
    elif stage == "consolidate_memories":
        return assess_consolidation_quality(state)
    else:
        return 1.0  # Default high quality

def assess_extraction_quality(state: LTMState) -> float:
    """Assess quality of memory extraction."""
    memories = state.extracted_memories

    if not memories:
        return 0.0

    quality_factors = []

    # Check for content completeness
    content_completeness = sum(1 for m in memories if len(m.get('content', '')) > 10) / len(memories)
    quality_factors.append(content_completeness)

    # Check for proper structure
    structure_quality = sum(1 for m in memories if 'memory_id' in m and 'content' in m) / len(memories)
    quality_factors.append(structure_quality)

    # Check confidence scores if available
    if hasattr(state, 'extraction_metadata') and 'confidence_scores' in state.extraction_metadata:
        avg_confidence = sum(state.extraction_metadata['confidence_scores'].values()) / len(state.extraction_metadata['confidence_scores'])
        quality_factors.append(avg_confidence)

    return sum(quality_factors) / len(quality_factors)

def handle_low_quality(state: LTMState, stage: str, quality_score: float) -> str:
    """Handle low quality results with improvement strategies."""

    # Check if we can retry with different parameters
    retry_count = getattr(state, f'{stage}_retry_count', 0)
    max_retries = 2

    if retry_count < max_retries:
        return f"retry_{stage}"
    else:
        # Accept low quality and continue
        state.processing_errors.append(f"{stage}: Low quality results (score: {quality_score:.2f})")
        return continue_normal_flow(state, stage)
```

### 5. Content-Driven Branches

#### Content Analysis for Routing

```python
def analyze_content_for_routing(state: LTMState) -> dict:
    """Analyze conversation content to inform routing decisions."""

    messages = state.messages
    if not messages:
        return {"content_type": "empty", "complexity": "low", "topics": []}

    combined_content = " ".join(msg.content for msg in messages if hasattr(msg, 'content'))

    return {
        "content_type": classify_content_type(combined_content),
        "complexity": assess_content_complexity(combined_content),
        "topics": extract_main_topics(combined_content),
        "length": len(combined_content),
        "language": detect_language(combined_content),
        "sentiment": analyze_sentiment(combined_content)
    }

def classify_content_type(content: str) -> str:
    """Classify the type of content for processing decisions."""
    content_lower = content.lower()

    if any(indicator in content_lower for indicator in ['fact', 'information', 'data', 'statistic']):
        return "factual"
    elif any(indicator in content_lower for indicator in ['feel', 'think', 'opinion', 'believe']):
        return "subjective"
    elif any(indicator in content_lower for indicator in ['do', 'action', 'task', 'goal']):
        return "procedural"
    elif any(indicator in content_lower for indicator in ['story', 'happened', 'experience']):
        return "narrative"
    else:
        return "general"

def should_use_advanced_processing(content_analysis: dict) -> bool:
    """Determine if content warrants advanced processing features."""

    # Use advanced processing for complex, lengthy, or factual content
    if content_analysis["complexity"] == "high":
        return True

    if content_analysis["length"] > 1000:
        return True

    if content_analysis["content_type"] in ["factual", "procedural"]:
        return True

    if len(content_analysis["topics"]) > 3:
        return True

    return False
```

## Branch Configuration

### Configuration-Based Branch Control

```python
class LTMBranchingConfig(BaseModel):
    """Configuration for LTM branching logic."""

    # Feature toggles
    enable_kg_processing: bool = True
    enable_categorization: bool = True
    enable_consolidation: bool = True
    enable_quality_checks: bool = True
    enable_error_recovery: bool = True

    # Thresholds
    consolidation_threshold: int = 5
    quality_threshold: float = 0.7
    max_retries: int = 2

    # Content-based routing
    min_memories_for_kg: int = 2
    min_memories_for_categorization: int = 3
    max_memories_for_single_batch: int = 50

    # Tool activation
    enable_implicit_tool_activation: bool = True
    tool_timeout: int = 30
    max_tool_iterations: int = 5

    # Error handling
    fail_fast: bool = False
    partial_results_acceptable: bool = True
    error_recovery_strategies: list[str] = ["retry", "skip", "fallback"]
```

## Branch Monitoring and Analytics

### Branch Decision Tracking

```python
def log_branch_decision(state: LTMState, from_node: str, to_node: str, reason: str):
    """Log branching decisions for analytics and debugging."""

    decision_log = {
        "timestamp": datetime.now().isoformat(),
        "from_node": from_node,
        "to_node": to_node,
        "reason": reason,
        "state_summary": summarize_state(state),
        "user_id": getattr(state, 'user_id', None),
        "session_id": getattr(state, 'session_id', None)
    }

    # Log to monitoring system
    logger.info(f"Branch decision: {from_node} → {to_node} ({reason})")

    # Store for analytics
    store_branch_analytics(decision_log)

def analyze_branch_patterns(time_window: str = "24h") -> dict:
    """Analyze branching patterns for optimization."""

    decisions = get_branch_decisions(time_window)

    return {
        "most_common_paths": calculate_common_paths(decisions),
        "error_rates_by_branch": calculate_error_rates(decisions),
        "processing_times_by_path": calculate_processing_times(decisions),
        "quality_scores_by_path": calculate_quality_scores(decisions),
        "user_satisfaction_by_path": calculate_satisfaction_scores(decisions)
    }
```

This branching logic provides a comprehensive, flexible, and robust system for routing LTM processing based on configuration, content, quality, errors, and user interactions. The system ensures optimal processing paths while maintaining resilience and user satisfaction.
