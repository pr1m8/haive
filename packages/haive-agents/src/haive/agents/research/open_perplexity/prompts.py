"""Prompt templates for the open_perplexity research agent.

This module contains the prompt templates used by various components of the
research agent, including system prompts, task-specific prompts, and specialized
templates for different stages of the research process.

Each prompt is designed for a specific task in the research workflow:
- MAIN_SYSTEM_PROMPT: Primary system prompt for the research agent
- RESEARCH_SYSTEM_PROMPT: System prompt for the specialized research assistant
- TOPIC_EXTRACTION_PROMPT: Extracts research topics and questions from user input
- REPORT_PLANNING_PROMPT: Generates a research report plan with sections
- QUERY_GENERATION_PROMPT: Creates search queries for specific research sections
- SECTION_WRITING_PROMPT: Generates content for report sections
- SOURCE_EVALUATION_PROMPT: Evaluates reliability and relevance of sources
- CONFIDENCE_ASSESSMENT_PROMPT: Assesses overall confidence in research findings
- FINAL_REPORT_COMPILATION_PROMPT: Compiles the final research report
- DATA_SOURCE_SELECTION_PROMPT: Recommends data sources for specific research needs
"""

# System prompts for different components
MAIN_SYSTEM_PROMPT = """
You are an advanced research agent capable of performing in-depth research on any topic. Your goal is to gather information, analyze it critically, and generate comprehensive research reports.

Your capabilities include:
1. Breaking down complex research questions into manageable parts
2. Identifying optimal data sources for specific research needs
3. Conducting parallel searches across multiple sources
4. Critically evaluating the reliability and relevance of sources
5. Synthesizing information into cohesive findings
6. Identifying contradictions and alternative perspectives
7. Assessing confidence levels in research findings
8. Generating well-structured research reports

Follow the instructions carefully and maintain high research standards. Your research should be thorough, balanced, and well-sourced.
"""

RESEARCH_SYSTEM_PROMPT = """
You are a research assistant with access to various data sources. Your task is to find accurate and relevant information on the specified topic.

You should:
1. Use the most appropriate data sources for each query
2. Evaluate source credibility and relevance
3. Extract key information from sources
4. Flag contradictory information
5. Track citation information for all sources

Be thorough in your search and prioritize authoritative sources. Provide comprehensive results while filtering out irrelevant information.
"""

# Topic extraction prompt
TOPIC_EXTRACTION_PROMPT = """
I need to extract the main research topic and questions from a user's input.

Here is the user's input:
{input_text}

Please extract the following information in JSON format:
- research_topic: The main topic of research
- research_question: The specific research question (if any)
- search_parameters: Any parameters or constraints for the research
- additional_context: Any other relevant context

Only include fields if they are present in the information above. If uncertain, leave the field empty or make a reasonable inference.

Examples:
1. Input: "Research the latest advancements in quantum computing"
   Output: {"research_topic": "quantum computing", "research_question": "What are the latest advancements in quantum computing?"}

2. Input: "I need to understand the environmental impact of electric vehicles compared to gas vehicles."
   Output: {"research_topic": "environmental impact of electric vs. gas vehicles", "research_question": "How do electric vehicles compare to gas vehicles in terms of environmental impact?"}
"""

# Report planning prompt
REPORT_PLANNING_PROMPT = """
I need to create a research plan for the following topic:

Research Topic: {research_topic}
Research Question: {research_question}
Additional Context: {additional_context}

I have an initial plan with these sections:
{initial_sections}

Please review this plan and suggest any modifications to make this a comprehensive research report.
Consider:
1. Are there any missing sections specific to this topic?
2. Should any sections be removed or combined?
3. Are there specific data sources that would be particularly valuable for this research?

Respond with a complete, updated list of sections in JSON format. Each section should have:
- name: Section name
- description: Brief description of the section
- requires_research: Boolean indicating if research is needed for this section
"""

# Query generation prompt
QUERY_GENERATION_PROMPT = """
I need to generate search queries to research the following topic:

Research Topic: {research_topic}
Research Question: {research_question}
Section I'm researching: {section_name}
Section Description: {section_description}

Please generate {num_queries} specific search queries that would help gather information for this section.
For each query, also recommend the best data source type (web, academic, news, github, etc.) to use.

Each query should target a specific aspect relevant to this section of the research report.

For each query, provide:
1. The query text (specific and focused)
2. The purpose of this query (what information it aims to find)
3. The recommended data source type

Format as a JSON list of objects with "query", "purpose", and "data_source" keys.
"""

# Section writing prompt
SECTION_WRITING_PROMPT = """
Write a section for a research report.

Section: {section_name}
Section Description: {section_description}

Research Topic: {research_topic}
Research Question: {research_question}

Research Context (sources and findings):
{research_context}

Write a comprehensive section addressing the following:
1. Key findings from research related to this section
2. Analysis of the information
3. Supporting evidence and sources
4. Any contradictions or alternative perspectives found

Guidelines:
- Be factual and evidence-based
- Cite sources for all key information
- Be concise but thorough
- Format in professional style with markdown headings
- Evaluate the reliability of sources where relevant
- Include clear conclusions based on the evidence
"""

# Source evaluation prompt
SOURCE_EVALUATION_PROMPT = """
I need to evaluate the reliability and relevance of the following source:

Source Title: {source_title}
Source URL: {source_url}
Source Content:
{source_content}

Research Topic: {research_topic}
Research Question: {research_question}

Please evaluate this source on the following criteria:
1. Relevance to the research topic (0-1 scale)
2. Content reliability (HIGH, MEDIUM, LOW, UNKNOWN)
3. Content freshness/recency (VERY_RECENT, RECENT, SOMEWHAT_RECENT, OUTDATED, UNKNOWN)
4. Key information relevant to our research
5. Any potential biases or limitations

Provide your evaluation in a structured JSON format with ratings and brief explanations for each criterion.
"""

# Research confidence assessment prompt
CONFIDENCE_ASSESSMENT_PROMPT = """
Assess the confidence level in our research findings based on the collected information.

Research Topic: {research_topic}
Research Question: {research_question}

Research Summary:
{research_summary}

Source Statistics:
- Total sources: {sources_count}
- High reliability sources: {high_reliability_sources}
- Recent sources: {recent_sources}

Key Findings:
{key_findings}

Please analyze the research and determine:
1. Overall confidence level (HIGH, MEDIUM, LOW, INSUFFICIENT_DATA)
2. Explanation for this confidence assessment
3. Key strengths of the research
4. Limitations of the research
5. Areas where additional research would be beneficial

Output in JSON format with each of these elements.
"""

# Final report compilation prompt
FINAL_REPORT_COMPILATION_PROMPT = """
Compile a complete research report based on the provided sections and findings.

Research Topic: {research_topic}
Research Question: {research_question}

Confidence Assessment:
{confidence_assessment}

Section Content:
{section_content}

Please compile a professional, comprehensive research report with the following:
1. Executive summary with key findings and confidence level
2. All section content properly formatted with headings
3. Clear presentation of evidence and analysis
4. Acknowledgment of limitations and areas for further research
5. Bibliography with all sources properly cited

Format the report in professional markdown with proper headings, sections, and formatting.
"""

# Data source selection prompt
DATA_SOURCE_SELECTION_PROMPT = """
I need to determine the best data sources for researching the following topic:

Research Topic: {research_topic}
Research Question: {research_question}
Research Depth Required: {research_depth}

Available Data Sources:
{available_sources}

Please analyze which data sources would be most valuable for this research topic.
Consider:
1. Which sources are most likely to have relevant information
2. Which sources would provide the most reliable information
3. The appropriate mix of sources for comprehensive coverage
4. Any specialized sources that would be particularly valuable

Respond with a ranked list of recommended data sources in JSON format, with a brief explanation for each recommendation.
"""
