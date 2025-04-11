from typing import Optional, List, Dict, Any, Union
from pydantic import Field
import uuid
from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_core.tools import BaseTool

from src.haive.core.models.llm.base import AzureLLMConfig
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.agents.v2.config import ReactAgentConfig
from src.haive.agents.rag.base.config import BaseRAGConfig
from src.haive.core.engine.retriever import VectorStoreRetrieverConfig
from src.haive.core.models.vectorstore.base import VectorStoreConfig

# Import KYC-specific modules
from src.haive.prebuilt.priv.kyc.prompts import RESEARCH_SYSTEM_PROMPT
from src.haive.prebuilt.priv.kyc.structured_tools import KYC_TOOLS

def create_kyc_react_agent_config(name: Optional[str] = None, 
                                 llm_model: str = "gpt-4o", 
                                 temperature: float = 0.2) -> ReactAgentConfig:
    """
    Create a ReactAgentConfig specifically for KYC research tasks.
    
    Args:
        name: Optional name for the agent
        llm_model: Model to use (default: gpt-4o)
        temperature: Temperature setting (default: 0.2)
        
    Returns:
        Configured ReactAgentConfig
    """
    # Create a name if not provided
    if not name:
        name = f"kyc_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Create LLM configuration
    llm_config = AzureLLMConfig(
        model=llm_model,
        parameters={
            "temperature": temperature,
            "max_tokens": 4000
        }
    )
    
    # Create system message for the ReactAgent
    system_message = RESEARCH_SYSTEM_PROMPT
    
    # Create ReactAgentConfig with KYC-specific tools
    react_config = ReactAgentConfig(
        name=name,
        llm_config=llm_config,
        system_prompt=system_message,
        tools=KYC_TOOLS,
        max_iterations=10,  # Increased for thorough research
        verbose=True
    )
    
    return react_config

def create_kyc_rag_engine(name: Optional[str] = None,
                         llm_model: str = "gpt-4o",
                         temperature: float = 0.2) -> AugLLMConfig:
    """
    Create an AugLLMConfig for KYC document retrieval tasks.
    
    Args:
        name: Optional name for the engine
        llm_model: Model to use (default: gpt-4o)
        temperature: Temperature setting (default: 0.2)
        
    Returns:
        Configured AugLLMConfig for RAG
    """
    # Create a name if not provided
    if not name:
        name = f"kyc_retrieval_engine_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Create LLM configuration
    llm_config = AzureLLMConfig(
        model=llm_model,
        parameters={
            "temperature": temperature,
            "max_tokens": 4000
        }
    )
    
    # Create system message
    system_message = """
    You are a KYC document retrieval assistant. Your role is to:
    1. Retrieve relevant documents about a company or individual
    2. Extract key information for KYC assessment
    3. Focus on business activities, regulatory compliance, and risk factors
    
    Be thorough and accurate in your retrieval and analysis.
    """
    
    # Create AugLLM configuration
    rag_engine = AugLLMConfig(
        name=name,
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages([
            SystemMessage(content=system_message),
            MessagesPlaceholder(variable_name="messages")
        ])
    )
    
    return rag_engine

def create_kyc_rag_agent_config(vectorstore_config: VectorStoreConfig, 
                               name: Optional[str] = None,
                               llm_model: str = "gpt-4o",
                               temperature: float = 0.2) -> BaseRAGConfig:
    """
    Create a BaseRAGConfig for KYC document retrieval tasks.
    This function requires a vectorstore_config with loaded documents.
    
    Args:
        vectorstore_config: Vector store configuration with loaded documents
        name: Optional name for the agent
        llm_model: Model to use (default: gpt-4o)
        temperature: Temperature setting (default: 0.2)
        
    Returns:
        Configured BaseRAGConfig
    """
    # Create a name if not provided
    if not name:
        name = f"kyc_retrieval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Create the RAG engine
    rag_engine = create_kyc_rag_engine(
        name=f"{name}_engine",
        llm_model=llm_model,
        temperature=temperature
    )
    
    # Create a retriever config from the vector store
    retriever_config = VectorStoreRetrieverConfig(
        name=f"retriever_for_{name}",
        vector_store_config=vectorstore_config,
        search_type="similarity",
        search_kwargs={"k": 5}
    )
    
    # Create BaseRAGConfig with proper retriever configuration
    rag_config = BaseRAGConfig(
        name=name,
        engine=rag_engine,
        retriever_config=retriever_config
    )
    
    return rag_config