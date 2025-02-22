# add notebook loader
from langchain_community.document_loaders import (
    TextLoader, UnstructuredFileLoader, CSVLoader, UnstructuredCSVLoader,
    UnstructuredHTMLLoader, UnstructuredPDFLoader, UnstructuredWordDocumentLoader,
    UnstructuredCHMLoader, UnstructuredEPubLoader, UnstructuredEmailLoader,
    UnstructuredExcelLoader, UnstructuredImageLoader, UnstructuredMarkdownLoader,
    UnstructuredODTLoader, UnstructuredOrgModeLoader, UnstructuredPowerPointLoader,
    UnstructuredRSTLoader, UnstructuredRTFLoader, UnstructuredTSVLoader,
    UnstructuredXMLLoader, Docx2txtLoader, PDFMinerLoader, PDFMinerPDFasHTMLLoader,
    PDFPlumberLoader, PyMuPDFLoader, PyPDFDirectoryLoader, PyPDFLoader, PyPDFium2Loader,
    AmazonTextractPDFLoader, DedocPDFLoader, MathpixPDFLoader, OnlinePDFLoader, PagedPDFSplitter,NotebookLoader,
    PythonLoader
)
from src.core.text_splitting.config import TextSplitterConfig
from langchain.tools import tool
from typing import Optional, List, Dict
import os
import asyncio
#from langchain.storage.
from src.agents.summarizer.summarizer_agent import SummarizerAgent
#summarizer = SummarizerAgent()
#result = asyncio.run(summarizer.run(notebook_docs))

async def load_file(file_path: str,load=True,save=False,
                  split=True,async_load=False,
                  metadata_modifier: Dict = None) -> List[Dict]:
    """
    Load a document based on its file type.

    This function determines the file type based on the file extension and uses the appropriate
    loader to load the document. It supports a wide range of file types, including text files,
    CSV files, HTML files, PDF files, Word documents, and more.

    Supported file types and their loaders:
    - .txt: TextLoader
    - .csv: CSVLoader
    - .html, .htm: UnstructuredHTMLLoader
    - .pdf: UnstructuredPDFLoader
    - .docx: UnstructuredWordDocumentLoader
    - .chm: UnstructuredCHMLoader
    - .epub: UnstructuredEPubLoader
    - .eml: UnstructuredEmailLoader
    - .xlsx, .xls: UnstructuredExcelLoader
    - .jpg, .jpeg, .png, .gif, .bmp, .tiff: UnstructuredImageLoader
    - .md: UnstructuredMarkdownLoader
    - .odt: UnstructuredODTLoader
    - .org: UnstructuredOrgModeLoader
    - .pptx, .ppt: UnstructuredPowerPointLoader
    - .ipynb: NotebookLoader
    - .py: PythonLoader
    - .png, .jpg: UnstructuredImageLoader
    - .rst: UnstructuredRSTLoader
    - .rtf: UnstructuredRTFLoader
    - .tsv: UnstructuredTSVLoader
    - .xml: UnstructuredXMLLoader
    - .doc: Docx2txtLoader
    - Other file types: UnstructuredFileLoader

    Args:
        file_path: Path to the document file.

    Returns:
        A list of dictionaries containing file content.
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    file_name = os.path.basename(file_path)
    if file_extension in ['.txt']:
        loader = TextLoader(file_path)
    elif file_extension in ['.csv']:
        loader = CSVLoader(file_path)
    elif file_extension in ['.html', '.htm']:
        loader = UnstructuredHTMLLoader(file_path)
    elif file_extension in ['.pdf']:
        loader = UnstructuredPDFLoader(file_path)
        """
        loader = PyMuPDFLoader(file_path)
        loader = PyPDFium2Loader(file_path)
        loader = PyPDFLoader(file_path)
        loader = PyPDFDirectoryLoader(file_path)
        loader = PyPDFium2Loader(file_path)
        loader = PyPDFLoader(file_path)
        loader = PyPDFium2Loader(file_path)
        """
    elif file_extension in ['.docx']:
        loader = UnstructuredWordDocumentLoader(file_path)
    elif file_extension in ['.chm']:
        loader = UnstructuredCHMLoader(file_path)
    elif file_extension in ['.epub']:
        loader = UnstructuredEPubLoader(file_path)
    elif file_extension in ['.eml']:
        loader = UnstructuredEmailLoader(file_path)
    elif file_extension in ['.xlsx', '.xls']:
        loader = UnstructuredExcelLoader(file_path)
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
        loader = UnstructuredImageLoader(file_path)
    elif file_extension in ['.md']:
        loader = UnstructuredMarkdownLoader(file_path)
    #elif file_extension in ['.ipynb']:
        #loader = NotebookLoader(file_path)
    elif file_extension in ['.png','.jpg']:
        loader = UnstructuredImageLoader(file_path)
    elif file_extension in ['.py']:
        loader = PythonLoader(file_path)
    elif file_extension in ['.odt']:
        loader = UnstructuredODTLoader(file_path)
    elif file_extension in ['.org']:
        loader = UnstructuredOrgModeLoader(file_path)
    elif file_extension in ['.pptx', '.ppt']:
        loader = UnstructuredPowerPointLoader(file_path)
    elif file_extension in ['.rst']:
        loader = UnstructuredRSTLoader(file_path)
    elif file_extension in ['.rtf']:
        loader = UnstructuredRTFLoader(file_path)
    elif file_extension in ['.tsv']:
        loader = UnstructuredTSVLoader(file_path)
    elif file_extension in ['.xml']:
        loader = UnstructuredXMLLoader(file_path)
    elif file_extension in ['.doc']:
        loader = Docx2txtLoader(file_path)
    elif file_extension in ['.ipynb']:
        loader = NotebookLoader(file_path)
    else:
        loader = UnstructuredFileLoader(file_path)
    
    if load and split: 
        documents = loader.load_and_split()
        #splitter=loader.load_and_split()
    elif load and not split:
        documents = loader.load()
    # Add get num tokens, 
    if metadata_modifier:
        documents = await add_metadata(documents,metadata_modifier)
    # Fix this
    #if save:
    #    with open(file_path, 'w') as f:
    #        f.write(documents)
    return documents

from langchain.docstore.document import Document

async def add_metadata(docs: List[Document],
                 metadata_modifier: Dict) -> List[Document]:
    
    if 'add_summary' in metadata_modifier:
        summarizer = SummarizerAgent()
        docs.metadata['summary'] = await summarizer.run(docs)
        print(docs.metadata['summary'], "add_metadata")
        #for doc in docs:
            #doc.metadata['summary'] = await summarizer.run(doc)
    return docs


from tqdm import tqdm
# Add typing
async def load_directory(directory_path: str,load=True,save=False,split=True,async_load=False,
                  filter_ext: str = None,metadata_modifier: Dict = None):
    docs = []
    for doc in tqdm(os.listdir(directory_path)):
        if filter_ext and doc.endswith(filter_ext):
            docs.append(await load_file(os.path.join(directory_path,doc),load=load,save=save,split=split,async_load=async_load,
                                     metadata_modifier=metadata_modifier))
        else:
            continue
    return docs
"""

notebook_docs = asyncio.run(load_directory(directory_path='/Users/will/Downloads/GenAI_Agents-main/all_agents_tutorials',
                load=True,save=False,split=True,async_load=True,filter_ext='.ipynb',
                metadata_modifier={'add_summary':True}))

#notebook_docs = load_document(file_path='/Users/will/Downloads/GenAI_Agents-main/all_agents_tutorials/agent_hackathon_genAI_career_assistant.ipynb',
#               load=True,save=False,split=False,async_load=False)
print(notebook_docs)

print(notebook_docs, "load_directory")
from src.core.vectorstore.config import VectorStoreConfig,create_vector_store,FAISS
from src.core.doc_loading.url_loaders import load_sitemap_documents
#summarizer = SummarizerAgent()
#result = asyncio.run(summarizer.run(notebook_docs))
#print(result)
a = VectorStoreConfig(vector_store_provider="FAISS",
                      vector_store_path="test.faiss",
                      embedding_model="text-embedding-3-small",
                      documents=notebook_docs)
#b = create_vector_store(a)
#print(b, "create_vector_store")
#b.save_local(folder_path="test_faiss",index_name="genai_agent_tutorials")
#print(b, "save_local")
#c = FAISS.load_local(folder_path="test_faiss",index_name="genai_agent_tutorials")
#print(c, "load_local")
#chain.invoke(notebook_docs)
#load_sitemap_documents(url="https://langchain-ai.github.io/langgraph")
"""