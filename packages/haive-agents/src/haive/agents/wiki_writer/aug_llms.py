from agents.wiki_writer.models import Outline, Perspectives, RelatedSubjects
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate

DIRECT_GEN_OUTLINE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Wikipedia writer. Write an outline for a Wikipedia page about a user-provided topic. Be comprehensive and specific.",
        ),
        ("user", "{topic}"),
    ]
)

# Add option for fast llm here ?
direct_gen_outline_aug_llm_config = AugLLMConfig(
    prompt=DIRECT_GEN_OUTLINE_PROMPT,
    output_parser=Outline,
)

GEN_RELATED_TOPICS_PROMPT = ChatPromptTemplate.from_template(
    """I'm writing a Wikipedia page for a topic mentioned below. Please identify and recommend some Wikipedia pages on closely related subjects. I'm looking for examples that provide insights into interesting aspects commonly associated with this topic, or examples that help me understand the typical content and structure included in Wikipedia pages for similar topics.

Please list the as many subjects and urls as you can.

Topic of interest: {topic}
"""
)


gen_related_topics_aug_llm_config = AugLLMConfig(
    prompt=GEN_RELATED_TOPICS_PROMPT,
    output_parser=RelatedSubjects,
)


GEN_PERSPECTIVES_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You need to select a diverse (and distinct) group of Wikipedia editors who will work together to create a comprehensive article on the topic. Each of them represents a different perspective, role, or affiliation related to this topic.\
    You can use other Wikipedia pages of related topics for inspiration. For each editor, add a description of what they will focus on.

    Wiki page outlines of related topics for inspiration:
    {examples}""",
        ),
        ("user", "Topic of interest: {topic}"),
    ]
)
gen_perspectives_aug_llm_config = AugLLMConfig(
    prompt=GEN_PERSPECTIVES_PROMPT,
    output_parser=Perspectives,
)
