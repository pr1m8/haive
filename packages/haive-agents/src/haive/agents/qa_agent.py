from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from pydantic import BaseModel, Field

from haive.agents.simple.agent import SimpleAgentConfig

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
"""
from typing import Annotated, Any

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate

# Define the union type for contents
ContentType = Annotated[
    str
    | list[str]
    | Document
    | list[Document]
    | BaseMessage
    | list[BaseMessage]
    | dict[str, Any],
    Field(
        description="Content to extract QA pairs from. Can be text, documents, messages, or structured data."
    ),
]

# Apply the type to your prompt template
qa_prompt_template = ChatPromptTemplate.from_messages(
    [("system", qa_system_prompt), ("human", "{contents}")]
)

# Set the input type
qa_prompt_template.input_types = {"contents": ContentType}


class QA(BaseModel):
    """A question and answer pair."""

    question: str = Field(description="The question that was asked.")
    answer: str = Field(description="The answer to the question.")


class QAs(BaseModel):
    """A list of question and answer pairs."""

    qas: list[QA] = Field(description="A list of question and answer pairs.")


qa_aug_llm_config = AugLLMConfig(
    llm=AzureLLMConfig(model="gpt-4o"),
    structured_output_model=QAs,
    prompt_template=qa_prompt_template,
)

qa_agent_config = SimpleAgentConfig.from_aug_llm(aug_llm=qa_aug_llm_config)
qa_agent = qa_agent_config.build_agent()

# Example usage

from langchain_community.document_loaders import WebBaseLoader

document = WebBaseLoader("https://en.wikipedia.org/wiki/Differential_geometry").load()

qas = qa_agent.run(input_data={"contents": document})
