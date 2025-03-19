import asyncio
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_transformers import (
    Html2TextTransformer,
    MarkdownifyTransformer,
    BeautifulSoupTransformer,
    DoctranQATransformer,
    DoctranPropertyExtractor,
    OpenAIMetadataTagger,
    LongContextReorder,
    NucliaTextTransformer
)
from langchain_core.documents import Document
import pandas as pd
import re
#from ..src.haive.agents.summarizer.agent import SummarizerAgent,SummarizerAgentConfig
# Assume you have a SummarizerAgentConfig
#summarizer = SummarizerAgent(SummarizerAgentConfig())
from dotenv import load_dotenv
load_dotenv('.env.example')
async def apply_transformers(documents):
    """Apply every document transformer and save results for comparison."""
    results = {"Original": [doc.page_content for doc in documents]}
    
    transformers = {
        "Html2Text": Html2TextTransformer(),
        "Markdownify": MarkdownifyTransformer(),
        "BeautifulSoup": BeautifulSoupTransformer(),
        "DoctranQA": DoctranQATransformer(),
        "DoctranPropertyExtractor": DoctranPropertyExtractor(),
        "OpenAIMetadataTagger": OpenAIMetadataTagger(
            #llm=summarizer.config.engines["reduce_chain"].llm_config.instantiate_llm(model="gpt-4o")
        ),
        "LongContextReorder": LongContextReorder(),
        "NucliaText": NucliaTextTransformer()
    }

    for name, transformer in transformers.items():
        try:
            transformed_docs = transformer.transform_documents(documents)
            results[name] = [doc.page_content for doc in transformed_docs]
            print(f"✅ Successfully transformed with {name}")
        except Exception as e:
            results[name] = [f"❌ Error: {str(e)}"]
            print(f"⚠️ Error in {name}: {e}")

    return results

def clean_and_format_text(text: str) -> str:
    """Cleans and formats text by replacing artifacts and ensuring proper newlines."""
    
    # Replace non-breaking spaces with regular spaces
    text = text.replace("\xa0", " ")

    # Remove excessive newlines (more than 2 consecutive newlines)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Ensure that full stops followed by a capital letter have a newline
    text = re.sub(r'(?<=[a-z])\.\s+(?=[A-Z])', '.\n', text)

    # Add newlines before "External links" and similar section headers
    text = re.sub(r'(\bExternal links\b|\bRetrieved from\b|\bSee also\b)', r'\n\n\1', text)

    # Remove unnecessary Wikipedia footer text (Terms of Use, Privacy Policy, etc.)
    text = re.sub(r'\nPrivacy policy.*', '', text, flags=re.DOTALL)

    # Remove stray whitespace at beginning/end of lines
    text = "\n".join(line.strip() for line in text.splitlines())

    return text

async def main():
    """Load Wikipedia page, apply transformers, and save results."""
    # Step 1: Load documents
    loader = WebBaseLoader("https://en.wikipedia.org/wiki/Differential_geometry")
    documents = loader.load()
    
    # Step 2: Apply text cleanup first
    documents = [Document(page_content=clean_and_format_text(d.page_content), metadata=d.metadata) for d in documents]
    
    # Step 3: Apply all transformers
    transformed_results = await apply_transformers(documents)
    
    # Step 4: Save results in a Pandas DataFrame
    df = pd.DataFrame(transformed_results)
    
    # Display the formatted results
    import ace_tools as tools
    tools.display_dataframe_to_user(name="Transformed Documents Comparison", dataframe=df)

if __name__ == "__main__":
    asyncio.run(main())
