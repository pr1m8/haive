"""
Prompt templates for the KYC report generation agent.
"""

# Risk appetite statement to be used in prompts
CORPAY_RISK_APPETITE_STATEMENT = """
Corpay Risk Appetite Statement

Prohibitions

Corpay has no appetite for customers who engage in any of the following:

Intentional or willfully negligent breaches of law, regulation, or policy applicable to Financial Crime Risk.
Repeated unintentional or repeated accidental breaches of law, regulation, or policy applicable to Financial Crime Risk.
Misusing as account for the purposes of money laundering or terrorism financing.
Facilitating business activities which could be construed as a tax offence.
Refusing to provide sufficient information or documentation to demonstrate compliance with the standards outlined in this statement.
The Company intends to conduct business only with reputable customers who use their own products, services, and related accounts for legitimate purposes, and whose identities can be determined and verified. In keeping with that principle, the Company will not knowingly conduct business with clients that seek to process payments through Corpay involving:

 
Illegal or illicit activities, including:
o Dealers involved in the distribution of arms and munitions
o Unlawful drugs (including cannabis industry)
o Red light businesses/adult entertainment
o Human trafficking
o Human exploitation
o Unlicensed and unlawful gambling
Virtual Currencies: unauthorized, unlicensed or unregulated exchanges
Unlicensed, unregistered and / or unregulated MSBs
Anonymous numbered accounts
Payable through accounts
Unlicensed banks
Shell banks
On-line gambling entities: For U.S. Dollar clearing accounts, transactions that are restricted or unlawful under the Unlawful Internet Gambling Enforcement Act (UIGEA) and Regulation GG of the Federal Reserve Board, 12 C.F.R. Part 233, Corpay understands that online gambling is not illegal in certain countries; however, Corpay is citing a U.S. regulation that prohibits these flows through U.S. Dollar accounts.
Restrictions
Corpay has heightened concerns about the risk presented by the following types of industries and will look to restrict activities which it deems suspicious in nature. For these categories, Corpay Compliance will perform enhanced due diligence and may reach out to the applicable front office employee and/or the prospective customer, to better understand transactional flows:

 
Arms, defense, military;
Call-Ins (at least and until it can be determined that the risk of fraud/identity theft has been 
removed).
Charities and other not-for-profit organizations;
Cash-intensive businesses, the type of which have known to have been used for money laundering and/or the financing of terror (including, for example, restaurants, bars and nightclubs, laundromats);
Dealers in high value/high portability luxury goods (such as dealers in diamonds and precious stones, precious metals, furs, art, boats, planes, vehicles, art dealers, including auctioneers dealing in any such goods);
Embassies/ consulates;
Entities operating under offshore banking licenses
Financial Services Providers or "Gatekeepers" including Money Services Businesses and other fiduciaries or intermediaries (including businesses that feature credit and stored value cards, smartcards, e-cash, and/or online banking, ecommerce/online retail businesses, payment service providers (PSPs), and including such professionals as Lawyers, Accountants, Securities Brokers/Dealers, Real Estate Brokers/Dealers, and Financial Advisors);
Gambling entities (excluding state sponsored lotteries);
General Trading Companies;
Cannabis-related businesses;
Multi-level Marketing Companies or Direct Sellers;
Politically Exposed Persons and Heads of International Organizations (HIOs);
Travel and tour operators;
Third Party Payment Processors;
Used Vehicle Dealers;
Virtual Asset Service Providers; and
Where beneficial ownership information cannot be confirmed.
Corpay employees are expected to properly identify these industries during the prospecting and onboarding 
processes.
"""

# System prompts for different components
MAIN_SYSTEM_PROMPT = """
You are a KYC (Know Your Customer) analyst tasked with researching companies and generating detailed risk assessment reports.
Your goal is to gather information about companies, analyze their business activities, and determine their risk level according to the company's risk appetite.

Follow the instructions carefully and be thorough in your research. Your assessment could prevent financial crime and protect the company from regulatory issues.
"""

RESEARCH_SYSTEM_PROMPT = """
You are a research assistant helping with a KYC (Know Your Customer) investigation.
Your task is to find accurate and relevant information about the target company.
Focus on business activities, regulatory status, and potential risk factors.
Use search tools to find information and be thorough in your research.

Pay particular attention to:
1. Company's primary business activities
2. Regulatory compliance and licensing
3. Beneficial ownership structure
4. Potential prohibited activities
5. Negative news or regulatory actions

Be factual and avoid speculation. Cite sources for all information gathered.
"""

# Specific task prompts
CUSTOMER_INFO_EXTRACTION_PROMPT = """
I need to extract key information about a customer for a KYC (Know Your Customer) report.

Here is the customer information:
{input_text}

Please extract the following information in JSON format:
- name: The name of the customer or business (IMPORTANT: Extract just the company name, e.g., if text says "I need to do a KYC for Bitfinex", the name should be "Bitfinex")
- customer_type: The type of customer (individual or business)
- website: The customer's website URL (if available)
- business_description: Brief description of business activities (if available)
- location: Customer's primary location or country (if available)
- additional_context: Any additional context provided

Only include fields if they are present in the information above. If uncertain, leave the field empty.

IMPORTANT RULES FOR NAME EXTRACTION:
1. If the text contains phrases like "KYC for X" or "X is a company", extract X as the name
2. Remove any phrase like "I need to do a KYC report for" to get just the company name
3. For company descriptions like "X is a cryptocurrency exchange", extract just "X" as the name
4. Return ONLY the specific entity name, not a full sentence

Example 1:
Input: "I need to do a KYC risk assessment for Bitfinex."
Correct name: "Bitfinex"

Example 2: 
Input: "Coinbase is a cryptocurrency exchange platform based in the US."
Correct name: "Coinbase"
"""

REPORT_PLANNING_PROMPT = """
I need to create a plan for a Know Your Customer (KYC) risk assessment report.

Customer Information:
- Name: {customer_name}
- Type: {customer_type}
- Business Description: {business_description}
- Location: {location}

Additional Context: {additional_context}

I have an initial plan with these sections:
{initial_sections}

Please review this plan and suggest any modifications to make this a comprehensive KYC report. 
Consider:
1. Are there any missing sections specific to this customer?
2. Should any sections be removed or combined?
3. Are there any special considerations based on the customer information?

Respond with a complete, updated list of sections in JSON format. Each section should have:
- name: Section name
- description: Brief description of the section
- requires_research: Boolean indicating if web research is needed
"""

QUERY_GENERATION_PROMPT = """
I need to generate search queries to research a company for KYC (Know Your Customer) purposes.

Company Information:
- Name: {customer_name}
- Business Description: {business_description}
- Location: {location}

Section I'm researching: {section_name}
Section Description: {section_description}

Please generate {num_queries} specific search queries that would help gather information for this section.
Each query should target a specific aspect relevant to this section of the KYC report.

For each query, provide:
1. The query text (specific and focused)
2. The purpose of this query (what information it aims to find)

Format as a JSON list of objects with "query" and "purpose" keys.
"""

SECTION_WRITING_PROMPT = """
Write a section for a KYC (Know Your Customer) risk assessment report.

Section: {section_name}
Section Description: {section_description}

Customer Information:
- Name: {customer_name}
- Business: {business_description}

Research Context (sources and findings):
{research_context}

Company Risk Appetite Statement:
{risk_appetite_statement}

Write a comprehensive section addressing the following:
1. Key findings from research related to this section
2. Any identified risk factors
3. Relevance to company's risk appetite
4. Supporting evidence and sources

Guidelines:
- Be factual and evidence-based
- Cite sources for all key information
- Be concise but thorough
- Highlight any red flags or concerns
- Format in professional business style with markdown headings
- Include clear conclusion about this aspect of the customer
"""

RISK_ASSESSMENT_PROMPT = """
Assess the risk level of a customer based on the KYC report findings.

Customer Information:
- Name: {customer_name}
- Type: {customer_type}
- Business: {business_description}

Report Findings:
{report_findings}

Company Risk Appetite Statement:
{risk_appetite_statement}

Please analyze the information and determine:
1. The primary business activity (from the BusinessActivity enum)
2. Any prohibited activities (from the ProhibitedActivity enum)
3. Whether the customer is politically exposed
4. Whether beneficial ownership is confirmed
5. The overall risk category (LOW_RISK, MEDIUM_RISK, HIGH_RISK, or PROHIBITED)
6. A compliance score between 0.0 and 1.0
7. Additional risk factors (as a dictionary)
8. Decision reasoning and recommended actions

Output in JSON format compatible with the CustomerRiskAssessmentModel.
"""

FINAL_REPORT_COMPILATION_PROMPT = """
Compile a complete KYC (Know Your Customer) risk assessment report based on the provided sections and risk assessment.

Customer Information:
- Name: {customer_name}
- Type: {customer_type}
- Business: {business_description}

Risk Assessment:
{risk_assessment}

KYC Decision:
{kyc_decision}

Section Content:
{section_content}

Please compile a professional, comprehensive KYC report with the following:
1. Executive summary with key findings and risk determination
2. All section content properly formatted with headings
3. Final risk assessment with clear explanation
4. Recommended actions based on the KYC decision
5. Appendix with sources and references

Format the report in professional markdown with proper headings, sections, and formatting.
"""