"""
Comprehensive mock handler for Sphinx documentation build.
Handles missing imports gracefully to allow documentation generation.
"""

import sys
import types
from unittest.mock import MagicMock
import logging

logger = logging.getLogger(__name__)

# List of all external dependencies that might not be installed
EXTERNAL_DEPENDENCIES = [
    # LangChain providers
    "langchain_google_vertexai",
    "langchain_cerebras", 
    "langchain_cohere",
    "langchain_ai21",
    "langchain_openlm",
    
    # Cloud/API services
    "google.generativeai",
    "google.cloud",
    "vertexai",
    "azure.identity",
    "boto3",
    "supabase",
    
    # Tools and integrations
    "nlpcloud",
    "elevenlabs",
    "jinaai",
    "asknews",
    "o365",
    "semanticscholar",
    "python_steam_api",
    "wolframalpha",
    "stackapi",
    "praw",
    "pyowm",
    "pygithub",
    "google_auth_oauthlib",
    "googleapiclient",
    "googlemaps",
    "amadeus",
    "atlassian",
    "slack_sdk",
    "gradio_tools",
    "discord",
    "tweepy",
    "dropbox",
    "gitpython",
    "feedparser",
    "listparser",
    "newspaper3k",
    "arxiv",
    "python_decouple",
    
    # Database drivers
    "pymongo",
    "psycopg2",
    "redis",
    "weaviate",
    "qdrant_client",
    "pinecone",
    
    # ML/Data libraries that might be optional
    "transformers",
    "sentence_transformers",
    "faiss",
    "chromadb",
    "torch",
    "tensorflow",
    "sklearn",
    "numpy",
    "pandas",
    "matplotlib",
    "plotly",
    "streamlit",
    
    # Other optional dependencies
    "beautifulsoup4",
    "lxml",
    "pypdf",
    "docx2txt",
    "pptx",
    "openpyxl",
    "xlrd",
    "camelot",
    "tabula",
    "pytesseract",
    "PIL",
    "cv2",
]

def mock_missing_modules():
    """Mock all missing external modules."""
    for module_name in EXTERNAL_DEPENDENCIES:
        if module_name not in sys.modules:
            # Create a mock module
            mock_module = types.ModuleType(module_name)
            
            # Add common attributes that might be accessed
            mock_module.__version__ = "0.0.0"
            mock_module.__file__ = f"<mock:{module_name}>"
            
            # Create a mock class that can be instantiated
            class MockClass:
                def __init__(self, *args, **kwargs):
                    pass
                def __getattr__(self, name):
                    return MagicMock()
            
            # Add the mock class as a common name pattern
            setattr(mock_module, "Client", MockClass)
            setattr(mock_module, "API", MockClass)
            setattr(mock_module, module_name.split(".")[-1].title(), MockClass)
            
            # Make the module itself callable and return MagicMock for any attribute
            mock_module.__getattr__ = lambda name: MagicMock()
            
            sys.modules[module_name] = mock_module
            logger.debug(f"Mocked module: {module_name}")

# Comprehensive list of missing Haive modules to mock
# Based on analysis of documentation build warnings
MISSING_HAIVE_MODULES = [
    # Agent submodules (55+ modules)
    "haive.agents.base.agent",
    "haive.agents.base.mixins",
    "haive.agents.base.mixins.state_mixin", 
    "haive.agents.base.mixins.execution_mixin",
    "haive.agents.rag.base",
    "haive.agents.rag.adaptive_rag",
    "haive.agents.rag.filtered",
    "haive.agents.rag.hyde", 
    "haive.agents.rag.self_corr",
    "haive.agents.rag.self_rag2",
    "haive.agents.rag.llm_rag",
    "haive.agents.rag.multi_strategy",
    "haive.agents.rag.db_rag",
    "haive.agents.conversation.base",
    "haive.agents.conversation.round_robin",
    "haive.agents.conversation.debate",
    "haive.agents.conversation.collaberative",
    "haive.agents.conversation.social_media",
    "haive.agents.conversation.directed.state",
    "haive.agents.document_modifiers.base",
    "haive.agents.document_modifiers.complex_extraction",
    "haive.agents.document_modifiers.summarizer",
    "haive.agents.document_modifiers.summarizer.iterative_refinement",
    "haive.agents.document_modifiers.summarizer.map_branch",
    "haive.agents.document_modifiers.tnt",
    "haive.agents.reasoning_and_critique.lats",
    "haive.agents.reasoning_and_critique.reflexion",
    "haive.agents.reasoning_and_critique.self_discover",
    "haive.agents.reasoning_and_critique.tot",
    "haive.agents.task_analysis.analysis",
    "haive.agents.task_analysis.context",
    "haive.agents.task_analysis.decomposer",
    "haive.agents.task_analysis.execution",
    "haive.agents.task_analysis.tree",
    "haive.agents.react.agent",
    "haive.agents.react.state",
    "haive.agents.simple.agent",
    "haive.agents.simple.config",
    "haive.agents.simple.factory",
    "haive.agents.simple.state",
    "haive.agents.simple.structured",
    "haive.agents.sequential.agent",
    "haive.agents.sequential.config",

    # Game modules (25+ modules) 
    "haive.games.base.agent",
    "haive.games.base.config",
    "haive.games.base.factory",
    "haive.games.base.state",
    "haive.games.base.state_manager",
    "haive.games.base.utils",
    "haive.games.base_v2",
    "haive.games.framework", 
    "haive.games.core",
    "haive.games.components",
    "haive.games.board_games",
    "haive.games.card_games",
    "haive.games.classic",
    "haive.games.other",
    "haive.games.chess",
    "haive.games.checkers",
    "haive.games.connect4",
    "haive.games.tic_tac_toe",
    "haive.games.go",
    "haive.games.mancala",
    "haive.games.reversi",
    "haive.games.nim",
    "haive.games.fox_and_geese",
    "haive.games.poker",
    "haive.games.among_us",
    "haive.games.mafia",
    "haive.games.debate",
    "haive.games.mastermind",
    "haive.games.single_player.wordle",
    "haive.games.monopoly",
    "haive.games.battleship",
    "haive.games.clue",
    "haive.games.cards.base",
    "haive.games.cards.blackjack",
    "haive.games.cards.poker",
    "haive.games.cards.uno",

    # Tool modules (20+ modules)
    "haive.tools.base",
    "haive.tools.core", 
    "haive.tools.individual",
    "haive.tools.utils",
    "haive.tools.utility",
    "haive.tools.general",
    "haive.tools.config",
    "haive.tools.content",
    "haive.tools.google",
    "haive.tools.injector",
    "haive.tools.tools.api",
    "haive.tools.tools.code",
    "haive.tools.tools.data",
    "haive.tools.tools.google",
    "haive.tools.tools.human",
    "haive.tools.tools.math",
    "haive.tools.tools.python",
    "haive.tools.tools.utility",
    "haive.tools.tools.web",

    # Core utility modules (5 modules)
    "haive.core.utils.discovery",
    "haive.core.utils.type_helpers",
    "haive.core.utils.schema_utils",
    "haive.core.engine.document",
]

# Create virtual modules for missing haive submodules based on common patterns
VIRTUAL_HAIVE_MODULES = {
    # Tools that don't exist but are referenced
    "haive.tools.base": {
        "Tool": type("Tool", (), {}),
        "BaseTool": type("BaseTool", (), {}),
    },
    "haive.tools.core": {
        "CoreTool": type("CoreTool", (), {}),
    },
    "haive.tools.individual": {
        "IndividualTool": type("IndividualTool", (), {}),
    },
    "haive.tools.search": {
        "WebSearch": type("WebSearch", (), {}),
        "SearchTool": type("SearchTool", (), {}),
    },
    "haive.tools.math": {
        "Calculator": type("Calculator", (), {}),
        "MathTool": type("MathTool", (), {}),
    },
    
    # Games that don't exist but are referenced
    "haive.games.board_games": {
        "Chess": type("Chess", (), {}),
        "Checkers": type("Checkers", (), {}),
    },
    "haive.games.card_games": {
        "Poker": type("Poker", (), {}),
        "Blackjack": type("Blackjack", (), {}),
    },
    "haive.games.classic": {
        "TicTacToe": type("TicTacToe", (), {}),
        "Connect4": type("Connect4", (), {}),
    },
    "haive.games.components": {
        "GameComponent": type("GameComponent", (), {}),
        "Board": type("Board", (), {}),
        "Deck": type("Deck", (), {}),
    },
    
    # Fix conversation module issues
    "haive.agents.conversation.directed.state": {
        "DirectedConversationState": type("DirectedConversationState", (), {}),
    },
}

def create_missing_haive_modules():
    """Create mock modules for all missing Haive modules."""
    for module_path in MISSING_HAIVE_MODULES:
        if module_path not in sys.modules:
            # Create the module
            module = types.ModuleType(module_path)
            
            # Add common attributes based on module type
            if "agent" in module_path:
                setattr(module, "Agent", type("Agent", (), {}))
                setattr(module, "BaseAgent", type("BaseAgent", (), {}))
            elif "tool" in module_path:
                setattr(module, "Tool", type("Tool", (), {}))
                setattr(module, "BaseTool", type("BaseTool", (), {}))
            elif "game" in module_path:
                setattr(module, "Game", type("Game", (), {}))
                setattr(module, "BaseGame", type("BaseGame", (), {}))
            
            # Add generic attributes
            setattr(module, "Config", type("Config", (), {}))
            setattr(module, "State", type("State", (), {}))
            setattr(module, "Factory", type("Factory", (), {}))
            
            # Make module callable and return MagicMock for any attribute
            module.__getattr__ = lambda name: MagicMock()
            
            # Register the module
            sys.modules[module_path] = module
            logger.debug(f"Created missing Haive module: {module_path}")
            
            # Also create parent modules if needed
            parts = module_path.split(".")
            for i in range(1, len(parts)):
                parent_path = ".".join(parts[:i])
                if parent_path not in sys.modules:
                    parent_module = types.ModuleType(parent_path)
                    parent_module.__getattr__ = lambda name: MagicMock()
                    sys.modules[parent_path] = parent_module

def create_virtual_modules():
    """Create virtual modules for missing haive submodules."""
    for module_path, contents in VIRTUAL_HAIVE_MODULES.items():
        if module_path not in sys.modules:
            # Create the module
            module = types.ModuleType(module_path)
            
            # Add the contents
            for name, obj in contents.items():
                setattr(module, name, obj)
            
            # Register the module
            sys.modules[module_path] = module
            logger.debug(f"Created virtual module: {module_path}")
            
            # Also create parent modules if needed
            parts = module_path.split(".")
            for i in range(1, len(parts)):
                parent_path = ".".join(parts[:i])
                if parent_path not in sys.modules:
                    sys.modules[parent_path] = types.ModuleType(parent_path)

# Mock specific problematic imports
def mock_specific_imports():
    """Mock specific imports that cause issues."""
    # Mock langchain imports that might fail
    if "langchain" in sys.modules:
        langchain = sys.modules["langchain"]
        if not hasattr(langchain, "llms"):
            langchain.llms = MagicMock()
        if not hasattr(langchain, "chat_models"):
            langchain.chat_models = MagicMock()
    
    # Mock pydantic v1/v2 compatibility
    if "pydantic" in sys.modules:
        pydantic = sys.modules["pydantic"]
        if not hasattr(pydantic, "v1"):
            pydantic.v1 = pydantic

# Run all mocking functions
def initialize_mocks():
    """Initialize all mocks for documentation build."""
    mock_missing_modules()
    create_missing_haive_modules()  # Add the comprehensive mock system
    create_virtual_modules()
    mock_specific_imports()
    logger.info(f"Documentation mocks initialized: {len(MISSING_HAIVE_MODULES) + len(EXTERNAL_DEPENDENCIES)} modules mocked")

# Initialize on import
initialize_mocks()