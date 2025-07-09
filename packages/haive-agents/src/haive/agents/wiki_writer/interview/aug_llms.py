from agents.wiki_writer.interview.models import AnswerWithCitations, Queries
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate

GEN_QUESTION_PROMPT = gen_qn_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an experienced Wikipedia writer and want to edit a specific page. \
Besides your identity as a Wikipedia writer, you have a specific focus when researching the topic. \
Now, you are chatting with an expert to get information. Ask good questions to get more useful information.

When you have no more questions to ask, say "Thank you so much for your help!" to end the conversation.\
Please only ask one question at a time and don't ask what you have asked before.\
Your questions should be related to the topic you want to write.
Be comprehensive and curious, gaining as much unique insight from the expert as possible.\

Stay true to your specific perspective:

{persona}""",
        ),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)

gen_qn_aug_llm_config = AugLLMConfig().from_prompt(GEN_QUESTION_PROMPT)


GEN_QUERIES_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful research assistant. Query the search engine to answer the user's questions.",
        ),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)
gen_queries_aug_llm_config = AugLLMConfig(
    prompt_template=GEN_QUERIES_PROMPT,
    structured_output_model=Queries,
    structured_output_params={"include_raw": True},
)


GEN_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert who can use information effectively. You are chatting with a Wikipedia writer who wants\
 to write a Wikipedia page on the topic you know. You have gathered the related information and will now use the information to form a response.

Make your response as informative as possible and make sure every sentence is supported by the gathered information.
Each response must be backed up by a citation from a reliable source, formatted as a footnote, reproducing the URLS after your response.""",
        ),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)

gen_answer_aug_llm_config = AugLLMConfig(
    prompt_template=GEN_ANSWER_PROMPT,
    structured_output_model=AnswerWithCitations,
    structured_output_params={"include_raw": True},
)
