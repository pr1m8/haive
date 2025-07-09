from haive.agents.document_modifiers.tnt.agent import TaxonomyAgent, TaxonomyAgentConfig
from haive.agents.document_modifiers.tnt.state import TaxonomyGenerationState

# Markdown(format_taxonomy_md(step["__end__"]["clusters"][-1]))

# Instantiate and visualize
agent = TaxonomyAgent(TaxonomyAgentConfig())
agent.visualize_graph()
from langchain_community.document_loaders import WebBaseLoader

from haive.agents.document_modifiers.tnt.models import Doc

tutorial_doc = WebBaseLoader(
    "https://langchain-ai.github.io/langgraph/tutorials/tnt-llm/tnt-llm/"
).load()
tutorial_2_doc = WebBaseLoader(
    "https://langchain-ai.github.io/langgraph/tutorials/reflection/reflection/"
).load()
# print(tutorial_doc)
test_docs = [
    Doc(id=tutorial_doc[0].metadata["source"], content=tutorial_doc[0].page_content)
]
test_docs.append(
    Doc(id=tutorial_2_doc[0].metadata["source"], content=tutorial_2_doc[0].page_content)
)
state = TaxonomyGenerationState(documents=test_docs)
# config = {"configurable": {"batch_size": 1}}
result = agent.app.invoke(state, debug=True, config=agent.config.runtime_config)
print(result)
