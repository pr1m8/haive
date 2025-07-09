"""Augmented LLM configurations for taxonomy generation.

This module defines the prompt templates and configurations for various LLM-based
tasks in the taxonomy generation process. It includes configurations for:
- Document summarization
- Taxonomy generation
- Taxonomy updating
- Taxonomy review
- Document classification

Each configuration combines specific prompt templates with output parsing and
post-processing logic.

Example:
    Basic usage of augmented LLM configs::

        summary_config = summary_aug_llm_config
        llm = summary_config.create_runnable()
        result = llm.invoke({"content": "text to summarize"})
"""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from haive.agents.document_modifiers.tnt.utils import parse_summary, parse_taxonomy

# System Message: Provides instructions and context
SUMMARY_SYSTEM_MESSAGE = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["content"],
        template="""
        # Instruction

        ## Context
        - **Goal**: You are tasked with summarizing the input text for the given use case. 
          The summary will represent the input data for clustering in the next step.
        - **Data**: Your input data is a conversation history between a User and an AI agent.

        # Data
        <data>
        {content}
        </data>
        """,
    )
)

# Human Message: User provides specific task instructions
SUMMARY_HUMAN_MESSAGE = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["summary_length", "explanation_length"],
        template="""
        # Questions

        ## Q1. Summarize the input text in {summary_length} words or less for the use case.
        Write the summary between `<summary></summary>` tags.

        **Tips:**
        - The summary should contain the relevant information for the use case in as much detail as possible.
        - Be concise and clear. Do not add phrases like _"This is the summary of the data ..."_ or _"Summarized text: ..."_
        - Similarly, do not reference the user (`the user asked XYZ`) unless it's absolutely relevant.
        - Within {summary_length} words, include as much relevant information as possible.
        - Do not include any line breaks in the summary.
        - Provide your answer in **English** only.

        ## Q2. Explain how you wrote the summary in {explanation_length} words or less.

        **Provide your answers between the tags**:
        ```
        <summary>your answer to Q1</summary>
        <explanation>your answer to Q2</explanation>
        ```

        # Output
        """,
    ).partial(summary_length=20, explanation_length=30)
)

# ChatPromptTemplate combining system and human messages
SUMMARY_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [SUMMARY_SYSTEM_MESSAGE, SUMMARY_HUMAN_MESSAGE]
)
print(SUMMARY_PROMPT_TEMPLATE)
summary_aug_llm_config = AugLLMConfig(
    prompt_template=SUMMARY_PROMPT_TEMPLATE,
    output_parser=StrOutputParser(),
    # runtime_options={"run_name": "GenerateSummary"},
    postprocess=parse_summary,
)

# System Message: Provides instructions and context
TAXONOMY_UPDATE_SYSTEM_MESSAGE = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=[
            "cluster_description_length",
            "cluster_name_length",
            "cluster_table_xml",
            "data_xml",
            "max_num_clusters",
            "use_case",
        ],
        template="""
        # Instruction

        ## Context
        - **Goal**: Your goal is to review the given reference table based on the input data for the specified use case, then update the reference table if needed.
          - You will be given a reference cluster table, which is built on existing data. The reference table will be used to classify new data points.
          - You will compare the input data with the reference table, output a rating score of the quality of the reference table, suggest potential edits, and update the reference table if needed.

        - **Reference cluster table**: The input cluster table is in XML format with each cluster as a `<cluster>` element, containing the following sub-elements:
          - **id**: category index.
          - **name**: category name.
          - **description**: category description used to classify data points.

        - **Data**: The input data will be a list of human-AI conversation summaries in XML format, including the following elements:
          - **id**: conversation index.
          - **text**: conversation summary.

        - **Use case**: {use_case}

        ## Requirements
        ### Format
        - Output clusters in **XML format** with each cluster as a `<cluster>` element, containing the following sub-elements:
          - **id**: category number starting from 1 in an incremental manner.
          - **name**: category name should be **within {cluster_name_length} words**. It can be either a verb phrase or a noun phrase, whichever is more appropriate.
          - **description**: category description should be **within {cluster_description_length} words**.

        Here is an example of your output:
        ```xml
        <clusters>
          <cluster>
            <id>category id</id>
            <name>category name</name>
            <description>category description</description>
          </cluster>
        </clusters>
        ```
        - Total number of categories should be **no more than {max_num_clusters}**.
        - Output should be in **English** only.

        ### Quality Criteria
        - **No overlap or contradiction** among the categories.
        - **Name** should be a concise and clear label for the category. Use only phrases that are specific to each category and avoid generic phrases.
        - **Description** should differentiate one category from another.
        - **Name** and **description** should **accurately** and **consistently** classify new data points **without ambiguity**.
        - **Name** and **description** should be **consistent with each other**.
        - Output clusters should match the data as closely as possible, without missing important categories or adding unnecessary ones.
        - Output clusters should strive to be orthogonal, providing solid coverage of the target domain.
        - Output clusters should serve the given use case well.
        - Output clusters should be specific and meaningful. **Do not invent categories** that are not in the data.

        # Reference cluster table
        <reference_table>
        {cluster_table_xml}
        </reference_table>

        # Data
        <conversations>
        {data_xml}
        </conversations>
        """,
    )
)

# Human Message: User provides specific task instructions
TAXONOMY_UPDATE_HUMAN_MESSAGE = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["explanation_length", "max_num_clusters", "suggestion_length"],
        template="""
        # Questions

        ## Q1: Review the given reference table and the input data, and provide a rating score of the reference table.  
        The rating score should be an **integer between 0 and 100** (higher means better quality).  
        You should consider the following factors:

        - **Intrinsic quality**:
          - 1) If the cluster table meets the *Requirements* section, with clear and consistent category names and descriptions, and no overlap or contradiction.
          - 2) If the categories in the cluster table are relevant to the given use case.
          - 3) If the cluster table includes any vague categories such as `"Other", "General", "Unclear", "Miscellaneous", or "Undefined"`.

        - **Extrinsic quality**:
          - 1) If the cluster table can accurately and consistently classify the input data without ambiguity.
          - 2) If there are missing categories in the cluster table that appear in the input data.
          - 3) If there are unnecessary categories in the cluster table that do not appear in the input data.

        ## Q2: Explain your rating score in Q1 **within {explanation_length} words**.

        ## Q3: Based on your review, decide if you need to edit the reference table to improve its quality.
        If yes, suggest potential edits **within {suggestion_length} words**. If no, output `"N/A"`.

        **Tips**:
        - You can edit the category name, description, or remove a category.
        - You can also merge or add new categories if needed.  
        - Your edits should meet the *Requirements* section.
        - The cluster table should be a **flat list** of **mutually exclusive** categories.  
        - You can have *fewer than {max_num_clusters} categories*, but **do not exceed the limit**.
        - Be **specific** about each category. **Do not include vague categories** like `"Other", "General", "Unclear", "Miscellaneous"`.
        - You can ignore low-quality or ambiguous data points.

        ## Q4: If you decide to edit the reference table, please provide your updated reference table.
        If you decide **not** to edit the reference table, please output the original reference table.

        ## Provide your answers between the following tags:
        ```
        <rating_score>integer between 0 and 100</rating_score>
        <explanation>explanation of your rating score within {explanation_length} words</explanation>
        <suggestions>suggested edits within {suggestion_length} words, or "N/A" if no edits needed</suggestions>
        <updated_table>
        your updated cluster table in XML format if you decided to edit the reference table,
        or the original reference table if no edits made
        </updated_table>
        ```

        # Output
        """,
    )
)

# ChatPromptTemplate combining system and human messages
TAXONOMY_UPDATE_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [TAXONOMY_UPDATE_SYSTEM_MESSAGE, TAXONOMY_UPDATE_HUMAN_MESSAGE]
)

taxonomy_update_aug_llm_config = AugLLMConfig(
    prompt_template=TAXONOMY_UPDATE_PROMPT_TEMPLATE,
    output_parser=StrOutputParser(),
    # runtime_options={"run_name": "UpdateTaxonomy"},
    postprocess=parse_taxonomy,
)

# System Message: Provides instructions and context
TAXONOMY_GENERATION_SYSTEM_MESSAGE = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=[
            "cluster_description_length",
            "cluster_name_length",
            "data_xml",
            "max_num_clusters",
            "use_case",
        ],
        template="""
        # Instruction

        ## Context
        - **Goal**: Your goal is to cluster the input data into meaningful categories for the given use case.
        - **Data**: The input data will be a list of human-AI conversation summaries in XML format, including the following elements:
          - **id**: conversation index.
          - **text**: conversation summary.
        - **Use case**: {use_case}

        ## Requirements
        ### Format
        - Output clusters in **XML format** with each cluster as a `<cluster>` element, containing the following sub-elements:
          - **id**: category number starting from 1 in an incremental manner.
          - **name**: category name should be **within {cluster_name_length} words**. It can be either a verb phrase or a noun phrase, whichever is more appropriate.
          - **description**: category description should be **within {cluster_description_length} words**.

        Here is an example of your output:
        ```xml
        <clusters>
          <cluster>
            <id>category id</id>
            <name>category name</name>
            <description>category description</description>
          </cluster>
        </clusters>
        ```
        - Total number of categories should be **no more than {max_num_clusters}**.
        - Output should be in **English** only.

        ### Quality Criteria
        - **No overlap or contradiction** among the categories.
        - **Name** should be a concise and clear label for the category. Use only phrases that are specific to each category and avoid generic phrases.
        - **Description** should differentiate one category from another.
        - **Name** and **description** should **accurately** and **consistently** classify new data points **without ambiguity**.
        - **Name** and **description** should be **consistent with each other**.
        - Output clusters should match the data as closely as possible, without missing important categories or adding unnecessary ones.
        - Output clusters should strive to be orthogonal, providing solid coverage of the target domain.
        - Output clusters should serve the given use case well.
        - Output clusters should be specific and meaningful. **Do not invent categories** that are not in the data.

        # Data
        <conversations>
        {data_xml}
        </conversations>
        """,
    )
)

# Human Message: User provides specific task instructions
TAXONOMY_GENERATION_HUMAN_MESSAGE = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["explanation_length", "max_num_clusters"],
        template="""
        # Questions

        ## Q1. Please generate a cluster table from the input data that meets the requirements.

        **Tips**:
        - The cluster table should be a **flat list** of **mutually exclusive** categories. Sort them based on their semantic relatedness.
        - Though you should aim for {max_num_clusters} categories, you can have *fewer than {max_num_clusters} categories* in the cluster table, but **do not exceed the limit**.
        - Be **specific** about each category. **Do not include vague categories** such as `"Other", "General", "Unclear", "Miscellaneous", or "Undefined"`.
        - You can ignore low-quality or ambiguous data points.

        ## Q2. Why did you cluster the data the way you did? Explain your reasoning **within {explanation_length} words**.

        **Provide your answers between the following tags**:
        ```
        <cluster_table>your generated cluster table with no more than {max_num_clusters} categories</cluster_table>
        <explanation>explanation of your reasoning process within {explanation_length} words</explanation>
        ```

        # Output
        """,
    )
)

# ChatPromptTemplate combining system and human messages
TAXONOMY_GENERATION_PROMPT_TEMPLATE = ChatPromptTemplate(
    messages=[TAXONOMY_GENERATION_SYSTEM_MESSAGE, TAXONOMY_GENERATION_HUMAN_MESSAGE]
)
taxonomy_generation_aug_llm_config = AugLLMConfig(
    prompt_template=TAXONOMY_GENERATION_PROMPT_TEMPLATE,
    output_parser=StrOutputParser(),
    postprocess=parse_taxonomy,
)


from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

# System Message: Provides instructions and context
TAXONOMY_REVIEW_SYSTEM_MESSAGE = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=[
            "cluster_description_length",
            "cluster_name_length",
            "cluster_table_xml",
            "max_num_clusters",
            "use_case",
        ],
        template="""
        # Instruction

        ## Context
        - **Goal**: Your goal is to review the given reference table based on the requirements and the specified use case, then update the reference table if needed.
          - You will be given a reference cluster table, which is built on existing data. The reference table will be used to classify new data points.
          - You will compare the reference table with the requirements, output a rating score of the quality of the reference table, suggest potential edits, and update the reference table if needed.

        - **Reference cluster table**: The input cluster table is in XML format with each cluster as a `<cluster>` element, containing the following sub-elements:
          - **id**: category index.
          - **name**: category name.
          - **description**: category description used to classify data points.

        - **Use case**: {use_case}

        ## Requirements
        ### Format
        - Output clusters in **XML format** with each cluster as a `<cluster>` element, containing the following sub-elements:
          - **id**: category number starting from 1 in an incremental manner.
          - **name**: category name should be **within {cluster_name_length} words**. It can be either a verb phrase or a noun phrase, whichever is more appropriate.
          - **description**: category description should be **within {cluster_description_length} words**.

        Here is an example of your output:
        ```xml
        <clusters>
          <cluster>
            <id>category id</id>
            <name>category name</name>
            <description>category description</description>
          </cluster>
        </clusters>
        ```
        - Total number of categories should be **no more than {max_num_clusters}**.
        - Output should be in **English** only.

        ### Quality Criteria
        - **No overlap or contradiction** among the categories.
        - **Name** should be a concise and clear label for the category. Use only phrases that are specific to each category and avoid generic phrases.
        - **Description** should differentiate one category from another.
        - **Name** and **description** should **accurately** and **consistently** classify new data points **without ambiguity**.
        - **Name** and **description** should be **consistent with each other**.
        - Output clusters should match the data as closely as possible, without missing important categories or adding unnecessary ones.
        - Output clusters should strive to be orthogonal, providing solid coverage of the target domain.
        - Output clusters should serve the given use case well.
        - Output clusters should be specific and meaningful. **Do not invent categories** that are not in the data.

        # Reference cluster table
        <reference_table>
        {cluster_table_xml}
        </reference_table>
        """,
    )
)

# Human Message: User provides specific task instructions
TAXONOMY_REVIEW_HUMAN_MESSAGE = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=[],
        template="""
        # Questions

        ## Q1: Review the given reference table and provide a rating score.  
        The rating score should be an **integer between 0 and 100** (higher means better quality).  
        You should consider the following factors:

        - **Intrinsic quality**:
          - If the cluster table meets the required quality with clear and consistent category names and descriptions, and no overlap or contradiction among the categories.
          - If the categories in the cluster table are relevant to the specified use case.
          - If the cluster table does not include any vague categories such as `"Other", "General", "Unclear", "Miscellaneous", or "Undefined"`.

        - **Extrinsic quality**:
          - If the cluster table can accurately and consistently classify the input data without ambiguity.
          - If there are missing categories in the cluster table that appear in the input data.
          - If there are unnecessary categories in the cluster table that do not appear in the input data.

        ## Q2: Explain your rating score in Q1.  
        The explanation should be concise and based on the **intrinsic and extrinsic qualities** evaluated in Q1.

        ## Q3: Based on your review, decide if you need to edit the reference table to improve its quality.  
        If yes, suggest **specific and actionable edits**.  
        If no, output `"N/A"`.

        **Tips**:
        - You can edit the category name, description, or remove a category.
        - You can also merge or add new categories if needed.
        - Your edits should **meet the formatting requirements** outlined in the instructions.
        - The cluster table should be a **flat list** of **mutually exclusive** categories.
        - You can have *fewer than {max_num_clusters} categories*, but **do not exceed the limit**.
        - Be **specific** about each category. **Do not include vague categories** like `"Other", "General", "Unclear", "Miscellaneous"`.

        ## Q4: If you decide to edit the reference table, provide your updated reference table.  
        If you decide **not** to edit the reference table, please output the original reference table.

        **Provide your answers between the following tags**:
        ```
        <rating_score>integer between 0 and 100</rating_score>
        <explanation>concise explanation of your rating score based on the intrinsic and extrinsic qualities</explanation>
        <suggestions>specific and actionable suggestions for edits, or "N/A" if no edits needed</suggestions>
        <updated_table>
        your updated cluster table in XML format if you decided to edit the reference table,
        or the original reference table if no edits made
        </updated_table>
        ```

        # Output
        """,
    )
)

# ChatPromptTemplate combining system and human messages
TAXONOMY_REVIEW_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [TAXONOMY_REVIEW_SYSTEM_MESSAGE, TAXONOMY_REVIEW_HUMAN_MESSAGE]
)

taxonomy_review_aug_llm_config = AugLLMConfig(
    prompt_template=TAXONOMY_REVIEW_PROMPT_TEMPLATE,
    output_parser=StrOutputParser(),
    # runtime_options={"run_name": "ReviewTaxonomy"},
    postprocess=parse_taxonomy,
)


TAXONOMY_CLASSIFICATION_SYSTEM_MESSAGE = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["taxonomy"],
        template="""
        # Instruction

        ## Context
        Your task is to use the provided taxonomy to categorize the overall topic or intent of a conversation between a human and an AI assistant.

        First, here is the taxonomy to use:

        <taxonomy>
        {taxonomy}
        </taxonomy>

        ## Steps:
        1. Carefully read through the entire conversation, paying attention to the key topics discussed and the apparent intents behind the human's messages.
        2. Consult the taxonomy and identify the **single most relevant category** that best captures the overall topic or intent of the conversation.
        3. Write out a **chain of reasoning** for why you selected that category. Explain how the category fits the content of the conversation, referencing specific statements or passages as evidence. Output this reasoning inside `<reasoning></reasoning>` tags.
        4. Output the **name of the category** you chose inside `<category></category>` tags.

        **Important Notes:**
        - Choose the **single most relevant** category.
        - **Do not choose multiple categories.**
        - **Think carefully** and explain your reasoning before giving your final category choice.
        """,
    )
)

# Human Message: User provides specific task instructions
TAXONOMY_CLASSIFICATION_HUMAN_MESSAGE = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["content"],
        template="""
        # Task

        Assign a **single category** to the following content:

        <content>
        {content}
        </content>

        Respond with your **reasoning and category** within XML tags. **Do not include a number, just the category text.**

        ```
        <reasoning>Your reasoning for selecting the category</reasoning>
        <category>The selected category</category>
        ```
        """,
    )
)

# ChatPromptTemplate combining system and human messages
TAXONOMY_CLASSIFICATION_PROMPT = ChatPromptTemplate.from_messages(
    [TAXONOMY_CLASSIFICATION_SYSTEM_MESSAGE, TAXONOMY_CLASSIFICATION_HUMAN_MESSAGE]
)
taxonomy_classification_aug_llm_config = AugLLMConfig(
    prompt_template=TAXONOMY_CLASSIFICATION_PROMPT,
    output_parser=StrOutputParser(),
)
