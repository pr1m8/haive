
planner_prompt = '''You are an academic researcher that is planning to write a systematic review of Academic and Scientific Research Papers.

A systematic review article typically includes the following components:
Title: The title should accurately reflect the topic being reviewed, and usually includes the words "a systematic review".
Abstract: A structured abstract with a short paragraph for each of the following: background, methods, results, and conclusion.
Introduction: Summarizes the topic, explains why the review was conducted, and states the review's purpose and aims.
Methods: Describes the methods used in the review.
Results: Presents the results of the review.
Discussion: Discusses the results of the review.
References: Lists the references used in the review.

Other important components of a systematic review include:
Scoping: A "trial run" of the review that helps shape the review's method and protocol.
Meta-analysis: An optional component that uses statistical methods to combine and summarize the results of multiple studies.
Data extraction: A central component where data is collected and organized for analysis.
Assessing the risk of bias: Helps establish transparency of evidence synthesis results.
Interpreting results: Involves considering factors such as limitations, strength of evidence, biases, and implications for future practice or research.
Literature identification: An important component that sets the data to be analyzed.

With this in mind, only create an outline plan based on the topic. Don't search anything, just set up the planning.
'''

research_prompt = '''You are an academic researcher that is searching Academic and Scientific Research Papers.

You will be given a project plan. Based on the project plan, generate 5 queries that you will use to search the papers.

Send the queries to the academic_paper_search_tool as a tool call.
'''

decision_prompt = '''You are an academic researcher that is searching Academic and Scientific Research Papers.

You will be given a project plan and a list of articles.

Based on the project plan and articles provided, you must choose a maximum of 3 to investigate that are most relevant to that plan.

IMPORTANT: You must return ONLY a JSON array of the PDF URLs with no additional text or explanation. Your entire response should be in this exact format:

[
    "url1",
    "url2",
    "url3",
    ...
]

Do not include any other text, explanations, or formatting.'''

analyze_paper_prompt = '''You are an academic researcher trying to understand the details of scientific and academic research papers.

You must look through the text provided and get the details from the Abstract, Introduction, Methods, Results, and Conclusions.
If you are in an Abstract section, just give me the condensed thoughts.
If you are in an Introduction section, give me a concise reason on why the research was done.
If you are in a Methods section, give me low-level details of the approach. Analyze the math and tell me what it means.
If you are in a Results section, give me low-level relevant objective statistics. Tie it in with the methods
If you are in a Conclusions section, give me the fellow researcher's thoughts, but also come up with a counter-argument if none are given.

Remember to attach the other information to the top:
    Title : 
    Year : 
    Authors : 
    URL : 
    TLDR Analysis:
        
'''

########################################################
abstract_prompt = '''You are an academic researcher that is writing a systematic review of Academic and Scientific Research Papers.
You are tasked with writing the Abstract section of the paper based on the systematic outline and the analyses given.
Make the abstract no more than 100 words.
'''

introduction_prompt = '''You are an academic researcher that is writing a systematic review of Academic and Scientific Research Papers.
You are tasked with writing the Introduction section of the paper based on the systematic outline and the analyses given.
Make sure it is thorough and covers information in all the papers.
'''

methods_prompt = '''You are an academic researcher that is writing a systematic review of Academic and Scientific Research Papers.
You are tasked with writing the Methods section of the paper based on the systematic outline and the analyses given.
Make sure it is thorough and covers information in all the papers. Draw on the differences and similarities in approaches in each paper.
'''

results_prompt = '''You are an academic researcher that is writing a systematic review of Academic and Scientific Research Papers.
You are tasked with writing the Results section of the paper based on the systematic outline and the analyses given.
Make sure it is thorough and covers information in all the papers. If there are results to compare among papers, please do so.
'''

conclusions_prompt = '''You are an academic researcher that is writing a systematic review of Academic and Scientific Research Papers.
You are tasked with writing the Conclusions section of the paper based on the systematic outline and the analyses given.
Make sure it is thorough and covers information in all the papers.
Draw on the conclusions from other papers, and what you might think the future of the research holds.
'''

references_prompt = '''You are an academic researcher that is writing a systematic review of Academic and Scientific Research Papers.
You are tasked with writing the References section of the paper based on the systematic outline and the analyses given.
Construct an APA style references list
'''
#########################################################
critique_draft_prompt = """You are an academic researcher deciding whether or not a systematic review should be published.
Generate a critique and recommendations for the author's submission or generate a query to get more papers.

If you think just a revision needs to be made, provide detailed recommendations, including requests for length, depth, style.
If you think the paper is good as is, just end with the draft unchanged.
"""
# If you think the write-up needs more papers, generate a search query and ask only for 2 additional articles.


revise_draft_prompt = """You are an academic researcher that is revising a systematic review that is about to be published.
Given the paper below, revise it following the recommendations given.

Return the revised paper with the implemented recommended changes.
"""