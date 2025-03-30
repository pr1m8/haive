from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
#from src.haive.core.prompts.base import PromptTemplateConfig
#from src.haive.core.runnables.runnable import LLMRunnableConfig
from src.haive.agents.graph_db.models import ValidateCypherOutput,CypherQueryOutput
from src.haive.core.engine.aug_llm import AugLLMConfig
# Update the example fewshot examples
CORRECT_CYPHER_SYSTEM_PROMPT = """
You are a Cypher expert reviewing a statement written by a junior developer. 
You need to correct the Cypher statement based on the provided errors. No pre-amble.
Do not wrap the response in any backticks or anything else. Respond with a Cypher statement only!
"""
CORRECT_CYPHER_USER_PROMPT = """Check for invalid syntax or semantics and return a corrected Cypher statement.

Schema:
{schema}

Note: Do not include any explanations or apologies in your responses.
Do not wrap the response in any backticks or anything else.
Respond with a Cypher statement only!

Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.

The question is:
{question}

The Cypher statement is:
{cypher}

The errors are:
{errors}


"""
CORRECT_CYPHER_PROMPT_TEMPLATE=ChatPromptTemplate.from_messages([
        (
            "system",
            (
                CORRECT_CYPHER_SYSTEM_PROMPT
            ),
        ),
        (
            "human",
            (
                CORRECT_CYPHER_USER_PROMPT
            ),
        )
    ]
)

correct_cypher_aug_llm_config= AugLLMConfig(
    prompt_template=CORRECT_CYPHER_PROMPT_TEMPLATE,
    structured_output_model=CypherQueryOutput,
    #output_parser=StrOutputParser()
)

VALIDATE_CYPHER_SYSTEM_PROMPT = """
You are a Cypher expert reviewing a statement written by a junior developer.
"""

VALIDATE_CYPHER_USER_PROMPT = """You must check the following:
* Are there any syntax errors in the Cypher statement?
* Are there any missing or undefined variables in the Cypher statement?
* Are any node labels missing from the schema?
* Are any relationship types missing from the schema?
* Are any of the properties not included in the schema?
* Does the Cypher statement include enough information to answer the question?

Examples of good errors:
* Label (:Foo) does not exist, did you mean (:Bar)?
* Property bar does not exist for label Foo, did you mean baz?
* Relationship FOO does not exist, did you mean FOO_BAR?

Schema:
{schema}

The question is:
{question}

The Cypher statement is:
{cypher}

Make sure you don't make any mistakes!"""

validate_cypher_prompt =ChatPromptTemplate.from_messages([
        (
            "system",
            VALIDATE_CYPHER_SYSTEM_PROMPT,
        ),
        (
            "human",
            VALIDATE_CYPHER_USER_PROMPT,
        ),
    ]
)

validate_cypher_aug_llm_config= AugLLMConfig(
    prompt_template=validate_cypher_prompt,
    structured_output_model=ValidateCypherOutput
)




TEXT2CYPHER_SYSTEM_PROMPT = """
You are a Neo4j expert. Given an input question, create a syntactically correct Cypher query to run.
Do not wrap the response in any backticks or anything else. Respond with a Cypher statement only!
"""
TEXT2CYPHER_USER_PROMPT = """

Below are a number of examples of questions and their corresponding Cypher queries.

{fewshot_examples}

User input: {question}
Cypher query:
"""
TEXT2CYPHER_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
        (
            "system",
            TEXT2CYPHER_SYSTEM_PROMPT,
        ),
        (
            "human",
            (
                TEXT2CYPHER_USER_PROMPT
            ),
        ),
    ]
)
text2cypher_aug_llm_config= AugLLMConfig(
    prompt_template=TEXT2CYPHER_PROMPT_TEMPLATE,
    output_parser=StrOutputParser()
)


GUARDRAILS_SYSTEM_PROMPT = """
As an intelligent assistant, your primary objective is to decide whether a given question is related to movies or not. 
If the question is related to movies, output "movie". Otherwise, output "end".
To make this decision, assess the content of the question and determine if it refers to any movie, actor, director, film industry, 
or related topics. Provide only the specified output: "movie" or "end".
"""
GUARDRAILS_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
        (
            "system",
            GUARDRAILS_SYSTEM_PROMPT,
        ),
        (
            "human",
            "{question}",
        ),
    ]
)

guardrails_aug_llm_config = AugLLMConfig(
    prompt_template=GUARDRAILS_PROMPT_TEMPLATE,
    output_parser=StrOutputParser()
)

GENERATE_FINAL_HUMAN_PROMPT = """Use the following results retrieved from a database to provide
a succinct, definitive answer to the user's question.

Respond as if you are answering the question directly.

Results: {results}
Question: {question}"""

GENERATE_FINAL_PROMPT_TEMPLATE= ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful assistant",
        ),
        (
            "human",
            (
            GENERATE_FINAL_HUMAN_PROMPT
            ),
        ),
    ]
)


generate_final_aug_llm_config = AugLLMConfig(
    prompt_template=GENERATE_FINAL_PROMPT_TEMPLATE,
    output_parser=StrOutputParser()
)
