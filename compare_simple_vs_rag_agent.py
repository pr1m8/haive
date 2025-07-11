#!/usr/bin/env python3

"""Compare SimpleAgentV2 vs BaseRAGAgent to find validation difference."""

print("=== COMPARISON: SimpleAgentV2 vs BaseRAGAgent ===")

try:
    print("\n1. Testing BaseRAGAgent...")
    from haive.agents.rag.base.agent import BaseRAGAgent
    from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig
    from langchain_core.documents import Document

    # Create BaseRAGAgent (should work without validation errors)
    docs = [Document(page_content="Test document")]
    vs_config = VectorStoreConfig(name="test_vs", documents=docs)

    rag_agent = BaseRAGAgent(name="test_rag", engine=vs_config)

    print("✅ BaseRAGAgent created successfully")
    print(f"   State schema: {rag_agent.state_schema}")

    # Check what fields are in the state schema
    if hasattr(rag_agent.state_schema, "model_fields"):
        fields = rag_agent.state_schema.model_fields
        print(f"   State fields: {list(fields.keys())}")

        # Check if context/engine fields exist and their properties
        for field_name in ["context", "engine"]:
            if field_name in fields:
                field_info = fields[field_name]
                required = (
                    field_info.is_required()
                    if hasattr(field_info, "is_required")
                    else (field_info.default is ...)
                )
                print(
                    f"   {field_name}: required={required}, default={getattr(field_info, 'default', 'NO_DEFAULT')}"
                )
            else:
                print(f"   {field_name}: NOT PRESENT in state schema")

    print(f"\n2. Checking BaseRAGAgent _app and input_model...")
    if hasattr(rag_agent, "_app") and rag_agent._app:
        app = rag_agent._app
        print(f"   _app type: {type(app)}")

        if hasattr(app, "input_model") and app.input_model:
            input_model = app.input_model
            print(f"   input_model: {input_model}")

            if hasattr(input_model, "model_fields"):
                input_fields = input_model.model_fields
                print(f"   input_model fields: {list(input_fields.keys())}")

                for field_name in ["context", "engine"]:
                    if field_name in input_fields:
                        field_info = input_fields[field_name]
                        required = (
                            field_info.is_required()
                            if hasattr(field_info, "is_required")
                            else (field_info.default is ...)
                        )
                        print(f"   input_model {field_name}: required={required}")
                    else:
                        print(f"   input_model {field_name}: NOT PRESENT")
        else:
            print("   No input_model found")
    else:
        print("   No _app found")

except Exception as e:
    print(f"❌ BaseRAGAgent error: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 60)

try:
    print("\n3. Testing SimpleAgentV2...")
    from haive.agents.simple.agent_v2 import SimpleAgentV2
    from haive.core.engine.aug_llm import AugLLMConfig
    from langchain_core.prompts import ChatPromptTemplate

    # Create same template as in notebook but with partial
    template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human", "Query: {query}\nContext: {context}"),
        ]
    ).partial(
        context=""
    )  # This should make context optional

    config = AugLLMConfig(prompt_template=template)

    simple_agent = SimpleAgentV2(engine=config)
    print("✅ SimpleAgentV2 created successfully")
    print(f"   State schema: {simple_agent.state_schema}")

    # Check what fields are in the state schema
    if hasattr(simple_agent.state_schema, "model_fields"):
        fields = simple_agent.state_schema.model_fields
        print(f"   State fields: {list(fields.keys())}")

        # Check if context/engine fields exist and their properties
        for field_name in ["context", "engine"]:
            if field_name in fields:
                field_info = fields[field_name]
                required = (
                    field_info.is_required()
                    if hasattr(field_info, "is_required")
                    else (field_info.default is ...)
                )
                print(
                    f"   {field_name}: required={required}, default={getattr(field_info, 'default', 'NO_DEFAULT')}"
                )
            else:
                print(f"   {field_name}: NOT PRESENT in state schema")

    print(f"\n4. Checking SimpleAgentV2 _app and input_model...")
    if hasattr(simple_agent, "_app") and simple_agent._app:
        app = simple_agent._app
        print(f"   _app type: {type(app)}")

        if hasattr(app, "input_model") and app.input_model:
            input_model = app.input_model
            print(f"   input_model: {input_model}")

            if hasattr(input_model, "model_fields"):
                input_fields = input_model.model_fields
                print(f"   input_model fields: {list(input_fields.keys())}")

                for field_name in ["context", "engine"]:
                    if field_name in input_fields:
                        field_info = input_fields[field_name]
                        required = (
                            field_info.is_required()
                            if hasattr(field_info, "is_required")
                            else (field_info.default is ...)
                        )
                        print(f"   input_model {field_name}: required={required}")
                    else:
                        print(f"   input_model {field_name}: NOT PRESENT")
        else:
            print("   No input_model found")
    else:
        print("   No _app found")

except Exception as e:
    print(f"❌ SimpleAgentV2 error: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 60)
print("\n5. SUMMARY:")
print("The key difference should be in the input_model validation.")
print(
    "BaseRAGAgent likely doesn't have context/engine marked as required in its input_model,"
)
print("while SimpleAgentV2 does.")
