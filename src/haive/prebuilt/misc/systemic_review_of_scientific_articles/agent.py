
# make first part as simple sequence and own agent graph 
#https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/systematic_review_of_scientific_articles.ipynb
class SystemicReviewOfScientificArticlesAgent(Agent):
    def __init__(self):
        super().__init__()
    def set_workflow(self):
        self.graph.add_node("process_input", process_input)
        self.graph.add_node("planner", plan_node)
        self.graph.add_node("researcher", research_node)
        self.graph.add_node("search_articles", take_action)
        self.graph.add_node("article_decisions", decision_node)
        self.graph.add_node("download_articles", article_download)
        self.graph.add_node("paper_analyzer", paper_analyzer)

        self.graph.add_node("write_abstract", write_abstract)
        self.graph.add_node("write_introduction", write_introduction)
        self.graph.add_node("write_methods", write_methods)
        self.graph.add_node("write_results", write_results)
        self.graph.add_node("write_conclusion", write_conclusion)
        self.graph.add_node("write_references", write_references)

        self.graph.add_node("aggregate_paper", aggregator)
        self.graph.add_node("critique_paper", critique)
        self.graph.add_node("revise_paper", paper_reviser)
        self.graph.add_node("final_draft", final_draft)


        self.graph.add_edge("process_input", "planner")
        self.graph.add_edge("planner", "researcher")
        self.graph.add_edge("researcher", "search_articles")
        self.graph.add_edge("search_articles", "article_decisions")
        self.graph.add_edge("article_decisions", "download_articles")
        self.graph.add_edge("download_articles", 'paper_analyzer')

        self.graph.add_edge("paper_analyzer", "write_abstract")
        self.graph.add_edge("paper_analyzer", "write_introduction")
        self.graph.add_edge("paper_analyzer", "write_methods")
        self.graph.add_edge("paper_analyzer", "write_results")
        self.graph.add_edge("paper_analyzer", "write_conclusion")
        self.graph.add_edge("paper_analyzer", "write_references")

        self.graph.add_edge("write_abstract", "aggregate_paper")
        self.graph.add_edge("write_introduction", "aggregate_paper")
        self.graph.add_edge("write_methods", "aggregate_paper")
        self.graph.add_edge("write_results", "aggregate_paper")
        self.graph.add_edge("write_conclusion", "aggregate_paper")
        self.graph.add_edge("write_references", "aggregate_paper")
        self.graph.add_edge("aggregate_paper", 'critique_paper')

        self.graph.add_conditional_edges(
            "critique_paper",
            exists_action,
            {"final_draft": "final_draft",
            "revise": "revise_paper",
            True: "search_articles"}
        )

        self.graph.add_edge("revise_paper", "critique_paper")
        self.graph.add_edge("final_draft", END)

        self.graph.set_entry_point("process_input") ## "llm"