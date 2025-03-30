https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/essay_grading_system_langgraph.ipynb# Define the fact-checking prompt
fact_checking_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Fact-check the texts provided. For each statement, identify any factual inaccuracies, misleading information, "
        "unsupported claims, or vague language lacking specific details. Confirm accuracy for each claim where possible, "
        "or provide suggestions for further searches. Flag statements as 'vague' if they are overly broad or lacking "
        "critical specifics (e.g., missing names, dates, or descriptions of technologies)."
        "Suggest keyword if you can't confirm or refute the statement.\n\n"
        "{text}\n\n"
        "Return the results in this JSON format:\n"
        "{{\n"
        "  \"results\": [\n"
        "    {{\n"
        "      \"statement\": \"<Original statement>\",\n"
        "      \"status\": \"<confirmed | refuted | unverifiable | vague>\",\n"
        "      \"explanation\": \"<Brief explanation of findings or reason for vagueness>\",\n"
        "      \"suggested_keywords\": [\"<keyword1>\", \"<keyword2>\"]\n"
        "    }},\n"
        "    {{...}}\n"
        "  ]\n"
        "}}\n"
    )
)

# Define the structured output llm for the fact-checking pipeline
structured_output_llm = llm.with_structured_output(FactCheckResult)

# Define the fact-checking pipeline
fact_checking_pipeline = fact_checking_prompt | structured_output_llm



def fact_check_article(article_text: str, chunks=None):
    """
    Fact-check the given text by identifying factual inaccuracies, misleading information, unsupported claims, or vague language.
    """
    # Split the full article text into manageable chunks if not provided
    if not chunks:
        chunks = chunk_large_text(article_text)
    
    # Fact-check each chunk of the article
    fact_check_results = []
    for chunk in chunks:
        fact_check_result = fact_checking_pipeline.invoke({"text": chunk})
        # Add search results for suggested keywords
        for statement in fact_check_result["result"]:
            suggested_keywords = statement.get('suggested_keywords', [])
            if suggested_keywords:
                statement['search_results'] = [
                    search_and_summarize(keyword) for keyword in suggested_keywords
                ]
        
        fact_check_results.extend(fact_check_result["result"])

    return fact_check_results
tone_analysis_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Analyze the tones of the following article. Does it appear neutral, positive, critical, or opinionated? "
        "Provide a short explanation for each detected tone. "
        "Use specific examples from the article to support your analysis.\\n\n{text}"
    )
)

tone_pipeline = tone_analysis_prompt | llm

def tone_analysis_article(article_text: str, chunks=None):
    """
    Analyze the tones of the given article text.
    """
    # Split the full article text into manageable chunks if not provided
    if not chunks:
        chunks = chunk_large_text(article_text)
    
    # Analyze the tones of each chunk of the article
    tone_results = []
    for chunk in chunks:
        tone_result = tone_pipeline.invoke({"text": chunk})
        tone_results.append(tone_result.content)
    
    return tone_results

# Quote extraction
quote_extraction_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Identify direct quotes in the following content, noting the speaker's name "
        "and the context of each quote. If there are no quotes, return 'No quotes found'.\n\n"
        "Text: {text}"
    )
)

# Define the quote extraction pipeline
quote_extraction_pipeline = quote_extraction_prompt | llm



def quote_extraction_article(article_text: str, chunks=None):
    """
    Extract direct quotes from the given article text.
    """
    # Split the full article text into manageable chunks if not provided
    if not chunks:
        chunks = chunk_large_text(article_text)
    
    # Extract quotes from each chunk of the article
    quote_results = []
    for chunk in chunks:
        quote_result = quote_extraction_pipeline.invoke({"text": chunk})
        quote_results.append(quote_result.content)
    
    return quote_results
# Define a prompt template for reviewing the grammar and bias of the article
review_prompt = PromptTemplate(
    input_variables=["text"],
    template=(
        "Review the following article for grammar, spelling, punctuation, and bias. "
        "Provide feedback on each aspect in form of a list of the issues found and some suggestions for improvement.\n\n"
        "{text}"
    )
)

# Define the review pipeline
grammar_and_bias_review = review_prompt | llm



def grammary_and_bias_analysis_article(article_text: str, chunks=None):
    """
    Review the given article text for grammar, spelling, punctuation, and bias.
    """
    # Split the full article text into manageable chunks if not provided
    if not chunks:
        chunks = chunk_large_text(article_text)
    
    # Review each chunk of the article
    review_results = []
    for chunk in chunks:
        review_result = grammar_and_bias_review.invoke({"text": chunk})
        review_results.append(review_result.content)
    
    return review_results
def get_or_create_chunks(state: State):
    """
    This function gets the article text from the state and splits it into manageable chunks.
    The chunks are stored in the state to avoid recomputing them multiple times.
    """
    article_text = state["article_text"]
    chunks = state.get("chunks", [])
    if not chunks:
        chunks = chunk_large_text(article_text)
        state["chunks"] = chunks

    return chunks


def categorize_user_input(state: State) -> State:
    """
    This node handles the categorization of the user input to identify the intended actions.
    """
    query = state["current_query"]
    actions = get_user_actions(query)
    return {"actions": actions}


def summarization_node(state):
    """
    This node generates a summary of the article text.
    """
    chunks = get_or_create_chunks(state)
    article_text = state["article_text"]
    summary_result = summarize_article(article_text, chunks)
    return {"summary_result": summary_result}


def fact_checking_node(state: State) -> State:
    chunks = get_or_create_chunks(state)
    article_text = state["article_text"]
    fact_checking_results = fact_check_article(article_text, chunks)
    return {"fact_check_result": fact_checking_results}


def tone_analysis_node(state: State) -> State:
    chunks = get_or_create_chunks(state)
    article_text = state["article_text"]
    tone_analysis_results = tone_analysis_article(article_text, chunks)
    return {"tone_analysis_result": tone_analysis_results}


def quote_extraction_node(state: State) -> State:
    chunks = get_or_create_chunks(state)
    article_text = state["article_text"]
    quote_extraction_results = quote_extraction_article(article_text, chunks)
    return {"quote_extraction_result": quote_extraction_results}
class SystemAction(TypedDict):
    actions: List[str]

# Define a prompt template for identifying the user's intended actions based on their input
action_prompt = PromptTemplate(
    input_variables=["input_text"],
    template=(
        "Identify the user's intended actions based on their input and return the actions in the following JSON format:\n"
        "{{\n"
        '  "actions": ["<summarization | fact-checking | tone-analysis | quote-extraction | grammar-and-bias-review | no-action-required | invalid>"]\n'
        "}}\n\n"
        "Guidelines:\n"
        "- If the user requests all actions or says 'everything' or 'full report,' respond with the list of all individual actions:\n"
        '{{\n'
        '    "actions": ["summarization", "fact-checking", "tone-analysis", "quote-extraction", "grammar-and-bias-review"]\n'
        "}}\n"
        "- If the user input requests multiple specific actions, list each action requested (e.g., 'summarization' and 'tone analysis' together as ['summarization', 'tone-analysis']).\n"
        "- If the user’s input does not relate to any accessible action, respond with:\n"
        '{{\n'
        '    "actions": ["invalid"]\n'
        "}}\n"
        "- If the user's input does not require any specific action, or wants to end the conversation, respond with:\n"
        '{{\n'
        '    "actions": ["no-action-required"]\n'
        "}}\n\n"
        "Important:\n"
        "- Only list all actions ('summarization', 'fact-checking', 'tone-analysis', 'quote-extraction', 'grammar-and-bias-review') if the user explicitly requests a comprehensive overview or all actions.\n"
        "- List only the actions explicitly requested by the user without inferring additional ones.\n\n"
        "Examples:\n"
        "- User input: 'Can you summarize the main points of this article for me?'\n"
        '  System action: {{ "actions": ["summarization"] }}\n'
        "- User input: 'I need to verify some claims in this article. Can you fact-check it?'\n"
        '  System action: {{ "actions": ["fact-checking"] }}\n'
        "- User input: 'Could you tell me the tone conveyed by this article?'\n"
        '  System action: {{ "actions": ["tone-analysis"] }}\n'
        "- User input: 'Identify any key quotes in this article that stand out.'\n"
        '  System action: {{ "actions": ["quote-extraction"] }}\n'
        "- User input: 'Can you check the grammar and point out any bias in this article?'\n"
        '  System action: {{ "actions": ["grammar-and-bias-review"] }}\n'
        "- User input: 'Please provide a comprehensive analysis, including all aspects.'\n"
        '  System action: {{ "actions": ["summarization", "fact-checking", "tone-analysis", "quote-extraction", "grammar-and-bias-review"] }}\n'
        "- User input: 'I want a tone analysis and quote extraction, please.'\n"
        '  System action: {{ "actions": ["tone-analysis", "quote-extraction"] }}\n'
        "- User input: 'I have another question that’s not related to these functions.'\n"
        '  System action: {{ "actions": ["invalid"] }}\n\n'
        "Input text:\n{input_text}"
    )
)


action_pipeline = action_prompt | llm.with_structured_output(SystemAction)



def get_user_actions(input_text: str) -> List[str]:
    """
    Identify the user's intended actions based on their input.
    """
    system_actions = action_pipeline.invoke({"input_text": input_text})
    
    return system_actions["actions"]
Sample usage
user_inputs = [
    "Can you summarize this article for me?",
    "I'm not sure about the accuracy of this article. Can you summarize it and fact-check it?",
    "I want to know the tone of this article.",
    "Can you extract any quotes from this article?",
    "I need a review of this article for grammar and bias.",
    "Can you provide a full report on this article?",
    "I would like to know everything about this article.",
    "I need help with something else.",
    "Ok, that's enough for now.",
    "What is the weather like today?",
]

for user_input in user_inputs:
    print(f"\n\nUser input: '{user_input}'")
    user_actions = get_user_actions(user_input)
    print(f"System actions: {user_actions}")

def grammar_and_bias_review_node(state: State) -> State:
    chunks = get_or_create_chunks(state)
    article_text = state["article_text"]
    grammar_and_bias_review_results = (
        grammary_and_bias_analysis_article(article_text, chunks)
    )
    return {"grammar_and_bias_review_result": grammar_and_bias_review_results}
def route(state: State) -> str:
    routes = []
    actions = state.get("actions", [])
    if "full report" in actions:
        routes = routes.values()
        routes.pop("no-action-required")
        routes.pop("invalid")
    else:
        for action in actions:
            if action in routes:
                routes.append(routes[action])

    if not routes:
        return END

    return routes



class JournamlsimReviewAgent(Agent):
    """
    Agent for reviewing the grammar and bias of an article.
    """
    def __init__(self, llm: BaseLLMConfig):
        super().__init__(llm)

    def setup_workflow(self):
        # Define constants for repeated literals - review
        CATEGORY = "category"
        SUMMARY = "summary"
        FACT_CHECKING = "fact checking"
        TONE_ANALYSIS = "tone analysis"
        QUOTE_EXTRACTION = "quote extraction"
        GRAMMAR_AND_BIAS_REVIEW = "grammar and bias review"

        # Create a graph
        

        # Define the nodes
        self.graph.add_node(CATEGORY, categorize_user_input)
        self.graph.add_node(SUMMARY, summarization_node)
        self.graph.add_node(FACT_CHECKING, fact_checking_node)
        self.graph.add_node(TONE_ANALYSIS, tone_analysis_node)
        self.graph.add_node(QUOTE_EXTRACTION, quote_extraction_node)
        self.graph.add_node(GRAMMAR_AND_BIAS_REVIEW, grammar_and_bias_review_node)

        self.graph.set_entry_point(CATEGORY)

        self.graph.add_conditional_edges(
            CATEGORY,
            lambda state: state["actions"],
            {
                "summarization": SUMMARY,
                "fact-checking": FACT_CHECKING,
                "tone-analysis": TONE_ANALYSIS,
                "quote-extraction": QUOTE_EXTRACTION,
                "grammar-and-bias-review": GRAMMAR_AND_BIAS_REVIEW,
                "no-action-required": END,
                "invalid": END,
            }
        )

        self.graph.add_edge(SUMMARY, END)
        self.graph.add_edge(FACT_CHECKING, END)
        self.graph.add_edge(TONE_ANALYSIS, END)
        self.graph.add_edge(QUOTE_EXTRACTION, END)
        self.graph.add_edge(GRAMMAR_AND_BIAS_REVIEW, END)