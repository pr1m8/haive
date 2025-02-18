from langchain.docstore.document import Document
from src.haive.agents.summarizer import SummarizerAgent
from typing import List, Dict

async def add_metadata(docs: List[Document],
                 metadata_modifier: Dict) -> List[Document]:
    
    if 'add_summary' in metadata_modifier:
        summarizer = SummarizerAgent()
        docs.metadata['summary'] = await summarizer.run(docs)
        print(docs.metadata['summary'], "add_metadata")
        #for doc in docs:
            #doc.metadata['summary'] = await summarizer.run(doc)
    return docs
