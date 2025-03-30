


class InterviewAgent(Agent):
    def __init__(self, llm: BaseLLM, state: PodcastGeneratorState):
    

    def setup_workflow(self):
        self.graph.add_node("Host question", generate_question)
        self.graph.add_node("Web research", search_web)
        self.graph.add_node("Wiki research", search_wikipedia)
        self.graph.add_node("Expert answer", generate_answer)
        self.graph.add_node("Save podcast", save_podcast)
        self.graph.add_node("Write script", write_section)

        # Flow
        self.graph.add_edge(START, "Host question")
        self.graph.add_edge("Host question", "Web research")
        self.graph.add_edge("Host question", "Wiki research")
        self.graph.add_edge("Web research", "Expert answer")
        self.graph.add_edge("Wiki research", "Expert answer")
        self.graph.add_conditional_edges("Expert answer", route_messages,['Host question','Save podcast'])
        self.graph.add_edge("Save podcast", "Write script")
        self.graph.add_edge("Write script", END)

