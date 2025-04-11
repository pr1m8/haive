#https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/taskifier.ipynb
from src.haive.prebuilt.misc.taskifier.state import ApproachState
class TaskifierAgent(Agent):
    def __init__(self):
        super().__init__()
    def set_workflow(self):
        # Initialize the StateGraph
        # Add nodes to the graph
        self.graph.add_node("approach_analysis", approach_analysis)
        self.graph.add_node("task_knowledge_retrieval", task_manifest)
        self.graph.add_node("customized_approach_generation", result_approach)

        # Define and add conditional edges
        self.graph.add_edge("approach_analysis", "task_knowledge_retrieval")
        self.graph.add_edge("task_knowledge_retrieval", "customized_approach_generation")

        # Set the entry point
        self.graph.set_entry_point("approach_analysis")

        # Set the exit point
        self.graph.add_edge("customized_approach_generation", END)

