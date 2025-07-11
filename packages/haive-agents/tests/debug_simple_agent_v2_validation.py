#!/usr/bin/env python3

"""
COMPREHENSIVE DEBUG TEST for SimpleAgent V2 Validation Error

This test traces EVERY step of the validation process to find exactly
where the engine/context fields get marked as required when they shouldn't be.
"""

import traceback
from pprint import pprint
from typing import Any, Dict, List

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Import the exact components from the notebook
from haive.agents.simple.agent_v2 import SimpleAgentV2


class QueryRefinementSuggestion(BaseModel):
    """Individual query refinement suggestion."""

    refined_query: str = Field(description="The refined/improved query")
    improvement_type: str = Field(description="Type of improvement made")
    rationale: str = Field(description="Why this refinement improves the query")
    expected_benefit: str = Field(description="Expected improvement in retrieval")


class QueryRefinementResponse(BaseModel):
    """Query refinement analysis and suggestions."""

    original_query: str = Field(description="The original user query")
    query_analysis: str = Field(description="Analysis of the original query")
    query_type: str = Field(description="Classification of query type")
    complexity_level: str = Field(description="simple, moderate, or complex")
    refinement_suggestions: List[QueryRefinementSuggestion] = Field(
        description="List of suggested query improvements"
    )
    best_refined_query: str = Field(description="The recommended best refined query")
    search_strategy_recommendations: List[str] = Field(
        description="Recommendations for search strategy"
    )


# Create the exact prompt from the notebook
RAG_QUERY_REFINEMENT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert query optimization specialist for RAG systems. Your role is to analyze user queries and suggest improvements that will lead to better document retrieval and more accurate answers.

**Query Analysis Dimensions:**
1. **Clarity**: Is the query clear and unambiguous?
2. **Specificity**: Is the query specific enough to retrieve relevant documents?
3. **Scope**: Is the query scope appropriate (not too broad or narrow)?
4. **Terminology**: Does the query use appropriate domain-specific terms?
5. **Intent**: Is the user's intent clearly expressed?
6. **Context**: Is sufficient context provided for understanding?

**Refinement Strategies:**
- **Add Specificity**: Include specific terms, entities, timeframes, or constraints
- **Clarify Intent**: Make the desired outcome or answer type explicit
- **Expand Context**: Add background information that helps with retrieval
- **Use Better Terminology**: Replace colloquial terms with domain-specific language
- **Break Down Complex Queries**: Split multi-part questions into focused sub-queries
- **Add Constraints**: Include relevant filters or limitations

**Query Types to Consider:**
- Factual (seeking specific facts)
- Analytical (requiring analysis or comparison)
- Procedural (asking for step-by-step guidance)
- Conceptual (understanding abstract ideas)
- Temporal (time-based information)
- Causal (cause-and-effect relationships)

Provide multiple refinement suggestions with clear rationales.""",
        ),
        (
            "human",
            """Analyze and refine the following user query to improve retrieval and answer quality.

**Original Query:** {query}

**Context (if provided):** {context}

**Analysis Required:**
1. Analyze the current query's strengths and weaknesses
2. Classify the query type and complexity
3. Provide multiple refinement suggestions
4. Recommend the best refined query
5. Suggest optimal search strategies

Focus on improvements that will lead to better document retrieval and more comprehensive answers.""",
        ),
    ]
)


def debug_step(step_name: str, data: Any, file_location: str = "") -> None:
    """Debug helper to print step information."""
    print(f"\n{'='*20} {step_name} {'='*20}")
    if file_location:
        print(f"📁 File Location: {file_location}")
    print(f"📊 Data Type: {type(data)}")

    if hasattr(data, "__dict__"):
        print(f"📋 Attributes: {list(data.__dict__.keys())}")

    if isinstance(data, dict):
        print(f"📋 Dict Keys: {list(data.keys())}")

    print(f"📄 Data:")
    try:
        pprint(data, width=100, depth=3)
    except Exception as e:
        print(f"❌ Error printing data: {e}")
        print(f"📄 String representation: {str(data)[:500]}...")


def inspect_pydantic_model(model_class: type, name: str) -> None:
    """Inspect a Pydantic model's fields and requirements."""
    print(f"\n🔍 INSPECTING PYDANTIC MODEL: {name}")
    print(f"📁 Model Class: {model_class}")

    if hasattr(model_class, "model_fields"):
        fields = model_class.model_fields
        print(f"📋 Fields ({len(fields)}):")

        for field_name, field_info in fields.items():
            # Check if field is required
            is_required = (
                field_info.is_required()
                if hasattr(field_info, "is_required")
                else (field_info.default is ...)
            )
            default_val = getattr(field_info, "default", "NO_DEFAULT")

            print(f"  🔸 {field_name}:")
            print(f"    - Required: {is_required}")
            print(f"    - Default: {default_val}")
            print(f"    - Type: {field_info.annotation}")

            if field_name in ["context", "engine"]:
                print(f"    ⚠️  CRITICAL FIELD DETECTED: {field_name}")


def test_debug_simple_agent_v2_validation():
    """
    Comprehensive debug test to trace every step of SimpleAgentV2 validation.

    This will help us find exactly where the engine/context validation error occurs.
    Traces the ENTIRE schema creation and composition process.
    """

    print("🚀 STARTING COMPREHENSIVE SIMPLE AGENT V2 DEBUG TEST")
    print("🔍 TRACING ENTIRE SCHEMA CREATION AND COMPOSITION PROCESS")
    print("=" * 80)

    # STEP 1: Test the prompt template
    debug_step(
        "STEP 1: Prompt Template Analysis",
        RAG_QUERY_REFINEMENT,
        "langchain_core.prompts.ChatPromptTemplate",
    )

    print(f"\n🔍 Prompt Template Details:")
    print(f"📋 Input Variables: {RAG_QUERY_REFINEMENT.input_variables}")
    print(
        f"📋 Partial Variables: {getattr(RAG_QUERY_REFINEMENT, 'partial_variables', {})}"
    )

    # STEP 2: Create AugLLMConfig and inspect it
    print(f"\n{'='*20} STEP 2: AugLLMConfig Creation {'='*20}")

    config = AugLLMConfig(
        structured_output_model=QueryRefinementResponse,
        structured_output_version="v2",
        prompt_template=RAG_QUERY_REFINEMENT,
    )

    debug_step(
        "AugLLMConfig Created",
        config,
        "packages/haive-core/src/haive/core/engine/aug_llm/config.py",
    )

    # Test the _get_input_variables method
    print(f"\n🔍 Testing AugLLMConfig._get_input_variables():")
    try:
        input_vars = config._get_input_variables()
        print(f"✅ Input Variables: {input_vars}")
    except Exception as e:
        print(f"❌ Error getting input variables: {e}")
        traceback.print_exc()

    # Test the _compute_input_fields method
    print(f"\n🔍 Testing AugLLMConfig._compute_input_fields():")
    try:
        input_fields = config._compute_input_fields()
        print(f"✅ Input Fields:")
        for field_name, field_tuple in input_fields.items():
            print(f"  🔸 {field_name}: {field_tuple}")

            if field_name in ["context", "engine"]:
                print(f"    ⚠️  CRITICAL FIELD: {field_name} = {field_tuple}")
    except Exception as e:
        print(f"❌ Error computing input fields: {e}")
        traceback.print_exc()

    # STEP 3: Trace Schema Creation and Composition Process
    print(f"\n{'='*20} STEP 3: SCHEMA CREATION & COMPOSITION TRACING {'='*20}")

    # Before creating the agent, let's trace schema composition
    print(f"\n🔍 TRACING SCHEMA COMPOSITION PROCESS:")

    # Let's manually trace what happens during agent creation
    try:
        print(f"\n📊 A. Pre-Creation Analysis:")
        print(f"   🔸 Engine Type: {type(config)}")
        print(f"   🔸 Engine Name: {getattr(config, 'name', 'NO_NAME')}")

        # Check if we can access the schema composer
        try:
            from haive.core.schema.schema_composer import SchemaComposer

            print(f"   ✅ SchemaComposer imported successfully")

            # Let's trace what base schemas are available
            print(f"\n📊 B. Base Schemas Analysis:")

            # Check MessagesState and other base schemas
            try:
                from haive.core.schema.prebuilt.messages_state import MessagesState

                inspect_pydantic_model(MessagesState, "MessagesState (Base)")
            except Exception as e:
                print(f"   ❌ Error importing MessagesState: {e}")

            try:
                from haive.core.schema.prebuilt.meta_state import MetaStateSchema

                inspect_pydantic_model(MetaStateSchema, "MetaStateSchema (Base)")
            except Exception as e:
                print(f"   ❌ Error importing MetaStateSchema: {e}")

            try:
                from haive.core.schema.prebuilt.messages.messages_with_token_usage import (
                    MessagesStateWithTokenUsage,
                )

                inspect_pydantic_model(
                    MessagesStateWithTokenUsage, "MessagesStateWithTokenUsage (Base)"
                )
            except Exception as e:
                print(f"   ❌ Error importing MessagesStateWithTokenUsage: {e}")

        except Exception as e:
            print(f"   ❌ Error importing SchemaComposer: {e}")

        print(f"\n📊 C. Engine Schema Derivation:")

        # Check what input/output schemas the engine will contribute
        if hasattr(config, "derive_input_schema"):
            try:
                engine_input_schema = config.derive_input_schema()
                print(f"   ✅ Engine Input Schema Derived:")
                inspect_pydantic_model(engine_input_schema, "Engine Input Schema")
            except Exception as e:
                print(f"   ❌ Error deriving engine input schema: {e}")
                traceback.print_exc()

        if hasattr(config, "derive_output_schema"):
            try:
                engine_output_schema = config.derive_output_schema()
                print(f"   ✅ Engine Output Schema Derived:")
                inspect_pydantic_model(engine_output_schema, "Engine Output Schema")
            except Exception as e:
                print(f"   ❌ Error deriving engine output schema: {e}")
                traceback.print_exc()

        print(f"\n📊 D. Creating SimpleAgentV2 with Schema Tracing:")

        # Now create the agent and trace the schema composition
        agent = SimpleAgentV2(engine=config)
        debug_step(
            "SimpleAgentV2 Created",
            agent,
            "packages/haive-agents/src/haive/agents/simple/agent_v2.py",
        )

        # Trace the schema that was actually created
        print(f"\n📊 E. Post-Creation Schema Analysis:")
        if hasattr(agent, "state_schema"):
            print(f"   ✅ Agent has state_schema: {agent.state_schema}")

            # Check if we can access the schema composer instance
            if hasattr(agent, "_schema_composer"):
                composer = agent._schema_composer
                debug_step(
                    "Schema Composer Instance",
                    composer,
                    "packages/haive-core/src/haive/core/schema/schema_composer.py",
                )

                # Check the composer's base schema
                if hasattr(composer, "base_state_schema"):
                    print(f"   🔸 Composer Base Schema: {composer.base_state_schema}")
                    inspect_pydantic_model(
                        composer.base_state_schema, "Composer Base Schema"
                    )

                # Check the composer's engines
                if hasattr(composer, "engines"):
                    print(f"   🔸 Composer Engines: {composer.engines}")
                    for i, engine in enumerate(composer.engines):
                        print(f"      Engine {i}: {engine}")
                        if hasattr(engine, "derive_input_schema"):
                            try:
                                eng_input = engine.derive_input_schema()
                                inspect_pydantic_model(
                                    eng_input, f"Engine {i} Input Schema"
                                )
                            except Exception as e:
                                print(f"      ❌ Error deriving engine {i} input: {e}")

                # Check the composed schema fields
                if hasattr(composer, "composed_schema"):
                    print(f"   🔸 Final Composed Schema: {composer.composed_schema}")
                    inspect_pydantic_model(
                        composer.composed_schema, "Final Composed Schema"
                    )
            else:
                print(f"   ❌ No _schema_composer found on agent")
        else:
            print(f"   ❌ No state_schema found on agent")

    except Exception as e:
        print(f"❌ Error during schema creation tracing: {e}")
        traceback.print_exc()
        return

    # STEP 4: Inspect the agent's state schema
    print(f"\n{'='*20} STEP 4: State Schema Analysis {'='*20}")

    if hasattr(agent, "state_schema"):
        inspect_pydantic_model(agent.state_schema, "Agent State Schema")
    else:
        print("❌ No state_schema found on agent")

    # STEP 5: Trace Graph Building and Compilation Process
    print(f"\n{'='*20} STEP 5: GRAPH BUILDING & COMPILATION TRACING {'='*20}")

    # Let's trace the graph building process
    print(f"\n🔍 TRACING GRAPH BUILDING PROCESS:")

    # Check if agent has build_graph method
    if hasattr(agent, "build_graph"):
        print(f"\n📊 A. Agent Graph Building:")
        try:
            # Get the graph before compilation
            graph = agent.build_graph()
            debug_step("Built Graph", graph, "BaseGraph or StateGraph")

            # Check graph properties
            if hasattr(graph, "nodes"):
                print(
                    f"   🔸 Graph Nodes: {list(graph.nodes.keys()) if hasattr(graph.nodes, 'keys') else graph.nodes}"
                )

            if hasattr(graph, "edges"):
                print(f"   🔸 Graph Edges: {graph.edges}")

            # Check if graph has a schema or input model
            if hasattr(graph, "schema"):
                print(f"   🔸 Graph Schema: {graph.schema}")
                inspect_pydantic_model(graph.schema, "Graph Schema")

        except Exception as e:
            print(f"   ❌ Error building graph: {e}")
            traceback.print_exc()

    print(f"\n📊 B. LangGraph App Compilation:")

    # Check the compiled app
    if hasattr(agent, "_app") and agent._app:
        app = agent._app
        debug_step("LangGraph App", app, "langgraph.pregel")

        # Trace app creation properties
        print(f"\n🔍 App Properties:")
        if hasattr(app, "channels"):
            print(f"   🔸 App Channels: {app.channels}")

        if hasattr(app, "input_channels"):
            print(f"   🔸 App Input Channels: {app.input_channels}")

        if hasattr(app, "output_channels"):
            print(f"   🔸 App Output Channels: {app.output_channels}")

        # Check for input_model - THIS IS THE CRITICAL PART
        if hasattr(app, "input_model") and app.input_model:
            print(f"\n🔍 LangGraph Input Model Found!")
            inspect_pydantic_model(app.input_model, "LangGraph Input Model")

            # Trace where this input_model comes from
            print(f"\n🔍 Input Model Source Analysis:")
            print(f"   🔸 Input Model Class: {app.input_model}")
            print(
                f"   🔸 Input Model Module: {getattr(app.input_model, '__module__', 'UNKNOWN')}"
            )
            print(
                f"   🔸 Input Model Name: {getattr(app.input_model, '__name__', 'UNKNOWN')}"
            )

            # THIS IS LIKELY WHERE THE BUG IS
            print(f"\n⚠️  CRITICAL: Comparing State Schema vs Input Model")
            state_fields = (
                agent.state_schema.model_fields
                if hasattr(agent, "state_schema")
                else {}
            )
            input_fields = (
                app.input_model.model_fields
                if hasattr(app.input_model, "model_fields")
                else {}
            )

            for critical_field in ["context", "engine"]:
                print(f"\n🔸 Field: {critical_field}")

                if critical_field in state_fields:
                    state_field = state_fields[critical_field]
                    state_required = (
                        state_field.is_required()
                        if hasattr(state_field, "is_required")
                        else (state_field.default is ...)
                    )
                    print(
                        f"  📊 State Schema: required={state_required}, default={getattr(state_field, 'default', 'NO_DEFAULT')}"
                    )
                else:
                    print(f"  📊 State Schema: NOT PRESENT")

                if critical_field in input_fields:
                    input_field = input_fields[critical_field]
                    input_required = (
                        input_field.is_required()
                        if hasattr(input_field, "is_required")
                        else (input_field.default is ...)
                    )
                    print(
                        f"  📊 Input Model: required={input_required}, default={getattr(input_field, 'default', 'NO_DEFAULT')}"
                    )

                    if critical_field in state_fields:
                        state_field = state_fields[critical_field]
                        state_required = (
                            state_field.is_required()
                            if hasattr(state_field, "is_required")
                            else (state_field.default is ...)
                        )
                        if state_required != input_required:
                            print(
                                f"  🚨 MISMATCH DETECTED! State={state_required}, Input={input_required}"
                            )
                            print(
                                f"      This is likely the source of the validation error!"
                            )
                else:
                    print(f"  📊 Input Model: NOT PRESENT")

            # Check if we can trace the input model creation
            print(f"\n🔍 Tracing Input Model Creation:")
            print(f"   This input_model was likely created during graph.compile()")
            print(f"   Location: langgraph/pregel/__init__.py or BaseGraph.compile()")

        else:
            print("❌ No input_model found on LangGraph app")
    else:
        print("❌ No _app found on agent")

    # STEP 5.5: Trace Engine Registration and Field Mapping
    print(f"\n{'='*20} STEP 5.5: ENGINE REGISTRATION & FIELD MAPPING {'='*20}")

    try:
        from haive.core.engine.base import EngineRegistry

        registry = EngineRegistry.get_instance()

        print(f"\n🔍 Engine Registry Analysis:")
        print(f"   🔸 Registry Type: {type(registry)}")

        if hasattr(registry, "engines"):
            print(f"   🔸 Registered Engines: {list(registry.engines.keys())}")

            # Check our specific engine
            engine_name = getattr(config, "name", None)
            if engine_name and engine_name in registry.engines:
                engine_info = registry.engines[engine_name]
                debug_step(
                    f"Engine Registry Info: {engine_name}",
                    engine_info,
                    "packages/haive-core/src/haive/core/engine/base.py",
                )

        # Check field mappings if they exist
        if hasattr(registry, "input_mappings"):
            print(f"   🔸 Input Mappings: {registry.input_mappings}")

        if hasattr(registry, "output_mappings"):
            print(f"   🔸 Output Mappings: {registry.output_mappings}")

        # Check if the engine has field information
        print(f"\n🔍 Engine Field Analysis:")
        if hasattr(config, "input_fields"):
            print(f"   🔸 Engine Input Fields: {config.input_fields}")

        if hasattr(config, "output_fields"):
            print(f"   🔸 Engine Output Fields: {config.output_fields}")

        # Check if there are any field metadata or annotations
        if hasattr(config, "_field_metadata"):
            print(f"   🔸 Engine Field Metadata: {config._field_metadata}")

    except Exception as e:
        print(f"❌ Error analyzing engine registry: {e}")
        traceback.print_exc()

    # STEP 6: Try to run with debug and catch the exact error
    print(f"\n{'='*20} STEP 6: Execution Attempt {'='*20}")

    test_input = {"query": "what is the tallest building in france"}
    print(f"🔍 Test Input: {test_input}")

    try:
        print("🚀 Attempting to run agent...")
        result = agent.run(test_input, debug=True)
        print(f"✅ SUCCESS: {result}")
    except Exception as e:
        print(f"❌ VALIDATION ERROR CAUGHT:")
        print(f"📄 Error Type: {type(e)}")
        print(f"📄 Error Message: {str(e)}")

        # Get the full traceback
        print(f"\n📚 Full Traceback:")
        traceback.print_exc()

        # Analyze the validation error
        if "validation errors" in str(e):
            print(f"\n🔍 VALIDATION ERROR ANALYSIS:")
            print(
                f"This confirms the issue is in Pydantic validation during LangGraph execution."
            )
            print(
                f"The error occurs when LangGraph tries to validate the input using input_model."
            )

    print(f"\n{'='*80}")
    print("🏁 DEBUG TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_debug_simple_agent_v2_validation()
