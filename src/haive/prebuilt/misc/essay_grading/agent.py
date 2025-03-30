


class EssayGradingAgent(Agent):
    def __init__(self):
        super().__init__()
    def set_workflow(self):
        # Add nodes to the graph
        self.graph.add_node("check_relevance", check_relevance)
        self.graph.add_node("check_grammar", check_grammar)
        self.graph.add_node("analyze_structure", analyze_structure)
        self.graph.add_node("evaluate_depth", evaluate_depth)
        self.graph.add_node("calculate_final_score", calculate_final_score)

        # Define and add conditional edges
        self.graph.add_conditional_edges(
            "check_relevance",
            lambda x: "check_grammar" if x["relevance_score"] > 0.5 else "calculate_final_score"
        )
        self.graph.add_conditional_edges(
            "check_grammar",
            lambda x: "analyze_structure" if x["grammar_score"] > 0.6 else "calculate_final_score"
        )
        self.graph.add_conditional_edges(
            "analyze_structure",
            lambda x: "evaluate_depth" if x["structure_score"] > 0.7 else "calculate_final_score"
        )
        self.graph.add_conditional_edges(
            "evaluate_depth",
            lambda x: "calculate_final_score"
        )

        # Set the entry point
        self.graph.set_entry_point("check_relevance")

        # Set the exit point
        self.graph.add_edge("calculate_final_score", END)

        # Compile the graph
        self.app = self.graph.compile()