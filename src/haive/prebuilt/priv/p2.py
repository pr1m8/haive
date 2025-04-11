"""
Prompt templates for KYC compliance analysis.

These templates are used by the KYC agent to:
1. Generate targeted search queries for client research
2. Analyze web content for compliance risks
3. Evaluate client against risk appetite statement
4. Reflect on information completeness
"""

# Generic system prompt for KYC analysis
KYC_SYSTEM_PROMPT = """
You are a KYC (Know Your Customer) compliance analyst working for Corpay, 
a financial services company that specializes in cross-border payments and 
currency risk management solutions.

Your role is to evaluate potential clients against the company's risk appetite statement
to determine if they should be categorized as:

1. PROHIBITED - Client is engaged in activities explicitly prohibited by the risk appetite statement
2. RESTRICTED - Client is engaged in activities requiring enhanced due diligence
3. ACCEPTABLE - Client does not appear to be engaged in prohibited or restricted activities

You must be thorough, accurate, and provide evidence-based assessments with clear reasoning.
"""

# Prompt for generating search queries
QUERY_GENERATOR_PROMPT = """
You are generating targeted search queries to research a potential client for KYC compliance purposes.

Client Name: {client_name}

Initial Information:
{initial_information}

Your goal is to determine if this client is involved in any of the following prohibited or restricted activities:

RISK APPETITE STATEMENT:
{risk_appetite_statement}

Generate {max_search_queries} effective search queries that will:
1. Reveal the client's primary business activities and business model
2. Identify any subsidiaries, affiliates, or parent companies
3. Discover regulatory issues, legal problems, or compliance violations
4. Determine presence in sanctioned countries or high-risk jurisdictions
5. Identify ultimate beneficial owners and key executives
6. Uncover any connection to prohibited industries or activities
7. Find evidence of proper licensing and registration status

Create targeted, specific queries using the company name combined with relevant terms from the risk appetite statement.
"""

# Prompt for analyzing web content
WEB_CONTENT_ANALYSIS_PROMPT = """
You are analyzing web content related to a potential client for KYC compliance purposes.

Client Name: {client_name}

RISK APPETITE STATEMENT:
{risk_appetite_statement}

Web Content to Analyze:
URL: {url}
Title: {title}

{content}

Analyze this content and extract:
1. Primary business activities and services offered
2. Industries the client operates in
3. Geographic regions of operation
4. Regulatory status and licensing information
5. Corporate structure and ownership information
6. Indications of prohibited or restricted activities
7. Evidence of proper compliance controls

Focus specifically on information relevant to the prohibited and restricted activities
in the risk appetite statement. Note any risk indicators, red flags, or areas requiring 
further investigation.
"""

# Prompt for comprehensive client analysis
CLIENT_ANALYSIS_PROMPT = """
You are performing a comprehensive KYC analysis of a potential client against our risk appetite statement.

Client Name: {client_name}

RISK APPETITE STATEMENT:
{risk_appetite_statement}

RESEARCH FINDINGS:
{research_notes}

Based on the research findings, perform a detailed analysis to determine:

1. If the client is engaged in any PROHIBITED activities as defined in the risk appetite statement
2. If the client is engaged in any RESTRICTED activities requiring enhanced due diligence
3. The overall risk level and appropriate classification (PROHIBITED, RESTRICTED, or ACCEPTABLE)

Your analysis should:
- Clearly identify all prohibited or restricted activities detected
- Provide specific evidence from the research findings
- Explain your reasoning for the classification
- Assess your confidence level in the determination
- Note any areas requiring further investigation

Be particularly vigilant about the following high-risk areas:
- Money laundering or terrorism financing risks
- Connections to illegal or illicit industries
- Unlicensed or unregistered financial operations
- Shell companies or entities with unclear ownership
- Operations in high-risk jurisdictions
"""

# Prompt for reflection on information completeness
REFLECTION_PROMPT = """
You are reviewing a KYC compliance analysis to ensure it's based on sufficient information
to make a confident determination.

Client Name: {client_name}

Current Analysis:
{analysis}

Research Notes:
{research_notes}

RISK APPETITE STATEMENT:
{risk_appetite_statement}

Determine if the current analysis has sufficient information to make a reliable compliance determination:

1. Is there enough information about the client's core business activities?
2. Do we understand the client's corporate structure and beneficial ownership?
3. Is there sufficient information about regulatory status and licensing?
4. Do we have adequate geographic coverage of the client's operations?
5. Have we explored all potential connections to prohibited or restricted activities?
6. Is the confidence level appropriate given the information available?

Identify any critical information gaps that would prevent making a reliable determination.

If information is incomplete, suggest specific additional search queries that would fill 
these knowledge gaps and improve confidence in the compliance determination.
"""

# Risk appetite parser prompt to extract key prohibitions and restrictions
RISK_APPETITE_PARSER_PROMPT = """
You are parsing a company's risk appetite statement to extract a structured list
of prohibited and restricted activities for KYC compliance analysis.

Risk Appetite Statement:
{risk_appetite_statement}

Extract and organize:
1. All explicitly prohibited activities or client types
2. All restricted activities or client types requiring enhanced due diligence
3. Any nuanced conditions or exceptions

Organize these into clear categories that can be easily used to evaluate potential clients.
"""

# Entity extraction prompt for identifying key entities
ENTITY_EXTRACTION_PROMPT = """
You are extracting key entities and relationships from text about a potential client.

Client Name: {client_name}

Text to analyze:
{text}

Extract the following types of entities:
1. Company names (the client and any related entities)
2. Key individuals (executives, founders, beneficial owners)
3. Locations (countries, jurisdictions of operation)
4. Industry sectors and business activities
5. Products and services offered
6. Regulatory bodies or licenses mentioned
7. Any sanctions, legal issues, or compliance concerns

For each entity, provide:
- The entity type
- The exact text where it appears
- Any relationships to other entities (e.g., "X is a subsidiary of Y")

Focus on information relevant to KYC compliance analysis.
"""

# Document classification prompt for categorizing documents
DOCUMENT_CLASSIFICATION_PROMPT = """
You are classifying web pages and documents related to a potential client for KYC analysis.

Document URL: {url}
Document Title: {title}

Content snippet:
{content_snippet}

Classify this document into one or more of the following categories:
1. Company profile or overview
2. Products and services
3. Regulatory or compliance information
4. Financial information
5. Leadership and governance
6. News or press releases
7. Geographic presence
8. Industry affiliations
9. Potential risk indicators
10. Other (specify)

For each category assigned, provide:
- Confidence score (0-100)
- Brief justification
- Key information extracted relevant to KYC analysis

Focus on information that helps determine if the client is engaged in prohibited or restricted activities.
"""

# Red flag detection prompt for identifying compliance concerns
RED_FLAG_DETECTION_PROMPT = """
You are reviewing information about a potential client to identify KYC red flags.

Client Name: {client_name}

Information to analyze:
{information}

Based on the company's risk appetite statement, identify any potential red flags or compliance concerns:

{risk_appetite_statement}

For each potential red flag identified:
1. Describe the specific concern
2. Quote the exact text that raised the concern
3. Explain why this is relevant to the risk appetite statement
4. Rate the severity (Low, Medium, High)
5. Suggest what additional information would help validate or dismiss the concern

Be thorough but fair - flag genuine concerns without being overly conservative.
"""

# Final determination prompt for making the compliance decision
FINAL_DETERMINATION_PROMPT = """
You are making a final KYC compliance determination for a potential client.

Client Name: {client_name}

Risk Appetite Statement:
{risk_appetite_statement}

Complete Analysis:
{complete_analysis}

Red Flags Identified:
{red_flags}

Make a final determination on whether this client should be:
1. PROHIBITED - Hard rejection due to prohibited activities
2. RESTRICTED - Acceptance with enhanced due diligence required
3. ACCEPTABLE - Standard onboarding process

Your determination must include:
- The final classification with clear justification
- Specific references to the risk appetite statement
- Evidence from the research supporting your conclusion
- Assessment of confidence in this determination (0-100%)
- If RESTRICTED, specific enhanced due diligence measures recommended
- If PROHIBITED, exact prohibitions that apply

Remember that this determination directly affects business decisions and compliance obligations.
Be accurate, fair, and thoroughly evidence-based.
"""

# Complete collection of prompts
KYC_PROMPTS = {
    "system": KYC_SYSTEM_PROMPT,
    "query_generator": QUERY_GENERATOR_PROMPT,
    "web_content_analysis": WEB_CONTENT_ANALYSIS_PROMPT,
    "client_analysis": CLIENT_ANALYSIS_PROMPT,
    "reflection": REFLECTION_PROMPT,
    "risk_appetite_parser": RISK_APPETITE_PARSER_PROMPT,
    "entity_extraction": ENTITY_EXTRACTION_PROMPT,
    "document_classification": DOCUMENT_CLASSIFICATION_PROMPT,
    "red_flag_detection": RED_FLAG_DETECTION_PROMPT,
    "final_determination": FINAL_DETERMINATION_PROMPT
}