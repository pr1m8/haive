Example usecase for PhD academic research
This cell tests the workflow with several example queries. These queries are designed to evaluate the agent on the following aspects:

Completing tasks that are representative of the work a PhD researcher might need to perform.
Addressing more specific tasks that require researching papers within a defined timeframe.
Tackling tasks across multiple areas of research.
Critically evaluating its own responses by sourcing specific information from the papers.
test_inputs = [
    "Download and summarize the findings of this paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11379842/pdf/11671_2024_Article_4070.pdf",

    "Can you find 8 papers on quantum machine learning?",

    """Find recent papers (2023-2024) about CRISPR applications in treating genetic disorders, 
    focusing on clinical trials and safety protocols""",

    """Find and analyze papers from 2023-2024 about the application of transformer architectures in protein folding prediction, 
    specifically looking for novel architectural modifications with experimental validation."""
]

# Run tests and store the results for later visualisation
outputs = []
for test_input in test_inputs:
    final_answer = await print_stream(app, test_input)
    outputs.append(final_answer.content)
Display results
This cell displays the results of the test queries for a more compact visualisation of the results.

for input, output in zip(test_inputs, outputs):
    display(Markdown(f"## Input:\n\n{input}\n\n"))
    display(Markdown(f"## Output:\n\n{output}\n\n"))
Input:
Download and summarize the findings of this paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11379842/pdf/11671_2024_Article_4070.pdfs