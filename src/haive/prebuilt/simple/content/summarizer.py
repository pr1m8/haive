

# Example usage
if __name__ == "__main__":
    # Configure logging
    #logging.basicConfig(level=logging.DEBUG)
    """
    # Create a simple agent
    agent = create_simple_agent(
        system_prompt="You are a helpful assistant.",
        name="simple_agent"
    )
    
    # Print schema info
    print(f"config.state_schema: {agent.config.state_schema}")
    
    # Run the agent
    result = agent.run("How old are you")
    print(f"DEBUG: Result: {result}")
    # Print the messages for debugging
    #print("\nFinal Messages:")
    for msg in result["messages"]:
        if hasattr(msg, "content"):
            print(f"{msg.type.upper()}: {msg.content}")
        elif isinstance(msg, tuple):
            print(f"{msg[0].upper()}: {msg[1]}")
    """
    from langchain_core.output_parsers import StrOutputParser
    map_prompt = ChatPromptTemplate.from_messages([('human',"Write a concise summary of the following:\\n\\n{contex}")])
    #map_prompt_template_config = PromptTemplateConfig(chat_prompt_template=map_prompt)
    map_aug_llm_config = AugLLMConfig(
        name='summarizer_map',
        prompt_template=map_prompt,
        output_parser = StrOutputParser()
    )
    #nagent = create_simple_agent(
    #    engine=map_aug_llm_config,
    ##    name="simple_agent_summarizer",
     ##   visualize=True,
        #struc
        #structured_output_model=SimpleAgentSchema
    #)
    #nagent2 = create_simple_agent(
    #    engine= planner_aug_llm_config,
    #    name="simple_planner",
    #    visualize=True,
    #    #struc
    #    #structured_output_model=SimpleAgentSchema
    #)
    #from src.haive.agents.summarizer.iterative_refinement.aug_llms import initial_summary_aug_llm, refine_summary_aug_llm
    #nagent3 = create_simple_agent(
    #    engine=refine_summary_aug_llm,
    #    name="iterative_refinement_summarizer",
    #    visualize=True,
    #    #output_mapping={"summary":"answer"},
    #    #structured_output_model=SimpleAgentSchema
    #)
    #print(f"DEBUG: nagent: {nagent}")
    #print(f"DEBUG: nagent.config: {nagent.config}")
    #print(f"DEBUG: nagent.config.state_schema: {nagent.config.state_schema}")
    #a=nagent.run(['Hello, how are you?','I am fine, thank you.','What is the weather in Tokyo?','The weather in Tokyo is sunny.','do you know the weather in Tokyo?','I like dogs', 'you like cats'])
    #a=nagent3.run("What is the age of the oldest person who is still alive who was born in the 1900s?")
    #print(f"DEBUG: Result: {a}")
    # Print the messages for debugging
    #print("\nFinal Messages:")
    #for msg in a["messages"]:
    #    if hasattr(msg, "content"):
    #        print(f"{msg.type.upper()}: {msg.content}")
    #    elif isinstance(msg, tuple):
    #        print(f"{msg[0].upper()}: {msg[1]}")
    
    # Define QA Model
    class QA(BaseModel):
        question: str = Field(description="The question that was asked.")
        answer: str = Field(description="The answer to the question.")

    class QAs(BaseModel):
        qas: List[QA] = Field(description="A list of question and answer pairs.")

    # System Prompt
    qa_system_prompt = """
    You are a highly intelligent AI assistant specializing in **retrieval-augmented generation (RAG)**. Your task is to generate **structured, diverse, and contextually relevant** questions and answers from a given text.

    🔹 **Your Goal:**
    - Extract **important facts**, **concepts**, and **insights** from the input text.
    - Generate **concise, unambiguous, and answerable** questions.
    - Ensure each question is **directly answerable from the text** without external knowledge.
    - Create a **variety of question types**, including:
    - **Fact-based questions** (Who, What, When, Where)
    - **Conceptual questions** (Why, How, Explain)
    - **Comparative questions** (How does X differ from Y?)
    - **Application-based questions** (How can X be used in real life?)
    - **Reasoning questions** (What are the implications of X?)
    - Ensure **no duplicate or overly similar questions**.
    - Use **formal, precise language** for professional contexts.

    🔹 **Rules:**
    1. **No hallucinations:** All answers must be explicitly stated in the input text.
    2. **Self-contained questions:** The question must be understandable on its own.
    3. **No leading questions:** Avoid assuming facts not present in the text.
    4. **Diverse phrasing:** Avoid repetition by varying sentence structure and vocabulary.

    🔹 **Example Input & Output:**
    ### 📖 **Input Text:**
    *"Marie Curie was a Polish-born physicist and chemist known for her pioneering research on radioactivity. She discovered the elements polonium and radium and was the first woman to win a Nobel Prize."*

    ### 📝 **Expected Output:**
    ```json
    [
    {{
        "question": "Who was Marie Curie?",
        "answer": "Marie Curie was a Polish-born physicist and chemist known for her research on radioactivity."
    }},
    {{
        "question": "What elements did Marie Curie discover?",
        "answer": "She discovered the elements polonium and radium."
    }},
    {{
        "question": "What was Marie Curie's major scientific contribution?",
        "answer": "She conducted pioneering research on radioactivity."
    }},
    {{
        "question": "Why is Marie Curie significant in scientific history?",
        "answer": "She was the first woman to win a Nobel Prize and made groundbreaking discoveries in radioactivity."
    }}
    ]
    generate an approporaite number of questions and answers based on the input text.
    """
    """
    # Prompt Template
    qa_prompt_template = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        ("user", "{contents}")
    ])


    qa_aug_llm_config = AugLLMConfig(
        llm_config=AzureLLMConfig(model="gpt-4o"),
        structured_output_model=QAs,
        prompt_template=qa_prompt_template
    )
    from langchain_community.document_loaders import WebBaseLoader
    #from langchain_text_splitters import RecursiveCharacterTextSplitter

    qa_agent_config = SimpleAgentConfig.from_aug_llm(aug_llm=qa_aug_llm_config)
    qa_agent = create_simple_agent(
        engine=qa_aug_llm_config,
        name="simple_qa_agent",
        visualize=True,
        #structured_output_model=QAs
    )
    documents = WebBaseLoader("https://en.wikipedia.org/wiki/Differential_geometry").load()
    ##text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    #docs = text_splitter.split_documents(documents)
    #print(qa_agent.config.engine)
    #print(qa_agent.config.state_schema)

    events = qa_agent.app.stream(input={'contents':documents},config=qa_agent.config.runnable_config)
    for event in events:
        print(f"DEBUG: event: {event}")
        if 'contents' in event:
            print(f"DEBUG: contents: {event['contents'][:10]}")
        if 'qas' in event:
            print(f"DEBUG: qas: {event['qas']}")
        #qa_agent.run("What is the capital of France?")
        #print(type(event))
        """
    from textwrap import wrap

    from textwrap import wrap
    from pydantic import BaseModel, Field
    from typing import List

    class Subsection(BaseModel):
        title: str = Field(description="Title of the subsection.")
        content: str = Field(description="Concise summary of the subsection.")

    class Section(BaseModel):
        title: str = Field(description="Title of the section.")
        subsections: List[Subsection] = Field(description="List of subsections under this section.")

    class DocumentHierarchy(BaseModel):
        title: str = Field(description="Title of the document.")
        sections: List[Section] = Field(description="Structured sections and subsections.")

        def pretty_print(self):
            print(f"DEBUG: self.title: {self.title}")
            #print(f"DEBUG: self.sections: {self.sections}")
            for s in self.sections:
                print(f"DEBUG: s.title: {s.title}")
                for ss in s.subsections:
                    print(f"DEBUG: ss.title: {ss.title}")
                    print(f"DEBUG: ss.content: {ss.content}")   



    # ✅ **Step 2: Define LLM Prompts for Semantic Splitting**

    # 🔹 **Semantic Splitting Prompt**
    split_prompt = ChatPromptTemplate.from_messages([
        ("system", "Analyze the given document and split it into a structured hierarchy with sections and subsections."),
        ("user", "{contents}")
    ])

    split_aug_llm = AugLLMConfig(
        name="document_splitter",
        prompt_template=split_prompt,
        structured_output_model=DocumentHierarchy
    )

    # ✅ **Step 3: Create an Agent for Splitting**
    split_agent = create_simple_agent(
        engine=split_aug_llm,
        name="document_split_agent"
    )
    from langchain_community.document_loaders import WebBaseLoader
    # ✅ **Step 4: Load & Process Documents**
    documents = WebBaseLoader("https://en.wikipedia.org/wiki/Differential_geometry").load()
    #text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)  # Larger chunks for better structure
    #docs = text_splitter.split_documents(documents)

    # ✅ **Step 5: Run the Agent**
    doc_text = "\n\n".join([doc.page_content for doc in documents])
    #hierarchical_structure = split_agent.run(doc_text)
    #print(type(hierarchical_structure))
    #print(hierarchical_structure.keys())
    from pydantic import ValidationError
    import json

    # Run the agent
    raw_output = split_agent.app.invoke(input=split_agent.state_schema.model_validate({'contents':doc_text}),config=split_agent.config.runnable_config,stream_mode='values')
    for i,event in enumerate(raw_output):
        #print(f"DEBUG: event: {event}")
        #if 'contents' in event:
        #    print(f"DEBUG: contents: {event['contents'][:10]}")
        #print(f"DEBUG: event.keys(): {event.keys()}")
        print(f"DEBUG: event: {event}")
        if event == 'documenthierarchy':
            print(f"DEBUG: i: {i}")
            print(f"DEBUG: event: {event}")
           # print(f"DEBUG: event['documenthierarchy']: {event['documenthierarchy']}")
           # print(f"DEBUG: type(event['documenthierarchy']): {type(event['documenthierarchy'])}")
           # event['documenthierarchy'].pretty_print()
        #if 'documenthierarchy' in event.keys():
        #    print(f"DEBUG: documenthierarchy: {event['documenthierarchy']}")
        #    print(type(event['documenthierarchy']))
        #    #event['documenthierarchy'].pretty_print()
    print(f"DEBUG: raw_output: {raw_output}")