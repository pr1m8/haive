"""Agent and Game registry - discovers all available components."""

import importlib
import inspect
from dataclasses import dataclass, field


@dataclass
class AgentInfo:
    """Metadata about a registered agent."""

    name: str
    module_path: str
    class_name: str
    category: str
    description: str = ""
    factory_method: str | None = None  # "from_documents", etc.
    requires_docs: bool = False
    requires_tools: bool = False
    tags: list[str] = field(default_factory=list)


@dataclass
class GameInfo:
    """Metadata about a registered game."""

    name: str
    module_path: str
    class_name: str
    category: str  # board, card, single_player, social_deduction, strategy
    description: str = ""
    min_players: int = 2
    max_players: int = 2
    has_example: bool = True
    has_config: bool = True
    has_ui: bool = False
    config_module: str = ""
    config_class: str = ""
    example_module: str = ""
    tags: list[str] = field(default_factory=list)


# ── Agent Registry ──────────────────────────────────────────────────

AGENT_REGISTRY: list[AgentInfo] = [
    # Core agents
    AgentInfo("Simple Agent", "haive.agents.simple.agent", "SimpleAgent", "core",
             "Basic conversational agent with LLM", tags=["conversation", "basic"]),
    AgentInfo("React Agent", "haive.agents.react.agent", "ReactAgent", "core",
             "Reasoning + Acting agent with tool use", requires_tools=True, tags=["tools", "reasoning"]),
    AgentInfo("Supervisor", "haive.agents.supervisor.agent", "ReactAgent", "core",
             "Orchestrates multiple sub-agents with tool use", tags=["multi-agent", "orchestration"]),
    AgentInfo("Dynamic Supervisor", "haive.agents.dynamic_supervisor.agent", "DynamicSupervisorAgent", "core",
             "Creates and manages agents dynamically", tags=["multi-agent", "dynamic"]),

    # RAG agents
    AgentInfo("Adaptive RAG", "haive.agents.rag.adaptive.agent", "AdaptiveRAGAgent", "rag",
             "Routes queries to optimal RAG strategy", factory_method="from_documents", requires_docs=True, tags=["rag", "adaptive"]),
    AgentInfo("Corrective RAG", "haive.agents.rag.corrective.agent", "CorrectiveRAGAgent", "rag",
             "Self-correcting RAG with document grading", factory_method="from_documents", requires_docs=True, tags=["rag", "self-correcting"]),
    AgentInfo("FLARE RAG", "haive.agents.rag.flare.agent", "FLARERAGAgent", "rag",
             "Forward-Looking Active REtrieval", factory_method="from_documents", requires_docs=True, tags=["rag", "active-retrieval"]),
    AgentInfo("Fusion RAG", "haive.agents.rag.fusion.agent", "RAGFusionAgent", "rag",
             "Multi-query fusion retrieval", factory_method="from_documents", requires_docs=True, tags=["rag", "fusion"]),
    AgentInfo("HyDE RAG", "haive.agents.rag.hyde.agent", "HyDERAGAgent", "rag",
             "Hypothetical Document Embeddings", factory_method="from_documents", requires_docs=True, tags=["rag", "hyde"]),
    AgentInfo("Multi-Query RAG", "haive.agents.rag.multi_query.agent", "MultiQueryRAGAgent", "rag",
             "Generates multiple query variants", factory_method="from_documents", requires_docs=True, tags=["rag", "multi-query"]),
    AgentInfo("Self-Route RAG", "haive.agents.rag.self_route.agent", "SelfRouteRAGAgent", "rag",
             "Self-routing between RAG strategies", factory_method="from_documents", requires_docs=True, tags=["rag", "routing"]),
    AgentInfo("Speculative RAG", "haive.agents.rag.speculative.agent", "SpeculativeRAGAgent", "rag",
             "Hypothesis-driven speculative retrieval", factory_method="from_documents", requires_docs=True, tags=["rag", "speculative"]),
    AgentInfo("Step-Back RAG", "haive.agents.rag.step_back.agent", "StepBackRAGAgent", "rag",
             "Abstraction-based step-back prompting", factory_method="from_documents", requires_docs=True, tags=["rag", "step-back"]),
    AgentInfo("Memory-Aware RAG", "haive.agents.rag.memory_aware.agent", "MemoryAwareRAGAgent", "rag",
             "RAG with persistent memory context", factory_method="from_documents", requires_docs=True, tags=["rag", "memory"]),
    AgentInfo("Document Grading RAG", "haive.agents.rag.document_grading.agent", "DocumentGradingRAGAgent", "rag",
             "RAG with relevance-based document grading", factory_method="from_documents", requires_docs=True, tags=["rag", "grading"]),
    AgentInfo("Agentic RAG", "haive.agents.rag.agentic.agent", "AgenticRAGAgent", "rag",
             "Tool-augmented agentic RAG", tags=["rag", "agentic"]),
    AgentInfo("Filtered RAG", "haive.agents.rag.filtered.agent", "FilteredRAGAgent", "rag",
             "RAG with metadata filtering", tags=["rag", "filtered"]),
    AgentInfo("Hallucination Grader", "haive.agents.rag.hallucination_grading.agent", "HallucinationGraderAgent", "rag",
             "Detects and grades hallucinations", tags=["rag", "grading"]),
    AgentInfo("Query Decomposer", "haive.agents.rag.query_decomposition.agent", "QueryDecomposerAgent", "rag",
             "Decomposes complex queries", tags=["rag", "decomposition"]),

    # Reasoning agents
    AgentInfo("Self-Discover", "haive.agents.reasoning_and_critique.self_discover.v2.agent", "self_discovery", "reasoning",
             "Self-discovering reasoning structures", tags=["reasoning"]),
    AgentInfo("Reflection", "haive.agents.reasoning_and_critique.reflection.agent", "ReflectionAgent", "reasoning",
             "Iterative self-reflection", tags=["reasoning", "reflection"]),
    AgentInfo("Reflexion", "haive.agents.reasoning_and_critique.reflexion.agent", "ReflexionAgent", "reasoning",
             "Reflexion with memory and self-improvement", tags=["reasoning", "reflexion"]),
    AgentInfo("Tree of Thought", "haive.agents.reasoning_and_critique.tot.agent", "ToTAgent", "reasoning",
             "Tree-structured reasoning exploration", tags=["reasoning", "tot"]),
    AgentInfo("LATS", "haive.agents.reasoning_and_critique.lats.agent", "LATSAgent", "reasoning",
             "Language Agent Tree Search", tags=["reasoning", "search"]),
    AgentInfo("MCTS", "haive.agents.reasoning_and_critique.mcts.agent", "MCTSAgent", "reasoning",
             "Monte Carlo Tree Search reasoning", tags=["reasoning", "mcts"]),
    AgentInfo("Logic Agent", "haive.agents.reasoning_and_critique.logic.agent", "create_synthesis_agent", "reasoning",
             "Formal logic-based reasoning synthesis", tags=["reasoning", "logic"]),

    # Planning agents
    AgentInfo("Plan & Execute", "haive.agents.planning.plan_and_execute.agent", "PlanAndExecuteAgent", "planning",
             "Plan then execute step-by-step", tags=["planning"]),
    AgentInfo("ReWOO V3", "haive.agents.planning.rewoo_v3.agent", "ReWOOV3Agent", "planning",
             "Reasoning Without Observation", tags=["planning", "rewoo"]),
    AgentInfo("LLM Compiler V3", "haive.agents.planning.llm_compiler_v3.agent", "LLMCompilerV3Agent", "planning",
             "Compiles tasks into execution plans", tags=["planning", "compiler"]),
    AgentInfo("Plan Execute V3", "haive.agents.planning.plan_execute_v3.agent", "PlanExecuteV3Agent", "planning",
             "Enhanced plan-execute with evaluation", tags=["planning"]),

    # Research agents
    AgentInfo("Open Perplexity", "haive.agents.research.open_perplexity.agent", "ResearchAgent", "research",
             "Open-source Perplexity-style search", tags=["research", "search"]),
    AgentInfo("Person Research", "haive.agents.research.person.agent", "PersonResearchAgent", "research",
             "Research information about people", tags=["research", "person"]),

    # Conversation agents
    AgentInfo("Conversation Agent", "haive.agents.conversation", "BaseConversationAgent", "conversation",
             "Multi-turn conversational agent", tags=["conversation"]),
]


# ── Game Registry ───────────────────────────────────────────────────

GAME_REGISTRY: list[GameInfo] = [
    # Board games
    GameInfo("Chess", "haive.games.chess.agent", "ChessAgent", "board",
             "Classic chess with LLM players", min_players=2, max_players=2,
             has_ui=True, config_module="haive.games.chess.config", config_class="ChessConfig",
             example_module="haive.games.chess.example", tags=["strategy", "classic"]),
    GameInfo("Go", "haive.games.go.agent", "GoAgent", "board",
             "Ancient strategy game of territory", min_players=2, max_players=2,
             config_module="haive.games.go.config", config_class="GoAgentConfig",
             example_module="haive.games.go.example", tags=["strategy", "classic"]),
    GameInfo("Checkers", "haive.games.checkers.agent", "CheckersAgent", "board",
             "Classic checkers/draughts", min_players=2, max_players=2,
             has_ui=True, config_module="haive.games.checkers.config", config_class="CheckersAgentConfig",
             example_module="haive.games.checkers.example", tags=["strategy", "classic"]),
    GameInfo("Tic Tac Toe", "haive.games.tic_tac_toe.agent", "TicTacToeAgent", "board",
             "Simple 3x3 grid game", min_players=2, max_players=2,
             has_ui=True, config_module="haive.games.tic_tac_toe.config", config_class="TicTacToeConfig",
             example_module="haive.games.tic_tac_toe.example", tags=["simple", "classic"]),
    GameInfo("Connect 4", "haive.games.connect4.agent", "Connect4Agent", "board",
             "Connect four in a row", min_players=2, max_players=2,
             has_ui=True, config_module="haive.games.connect4.config", config_class="Connect4AgentConfig",
             example_module="haive.games.connect4.example", tags=["strategy", "classic"]),
    GameInfo("Battleship", "haive.games.battleship.agent", "BattleshipAgent", "board",
             "Naval strategy game", min_players=2, max_players=2,
             config_module="haive.games.battleship.config", config_class="BattleshipAgentConfig",
             example_module="haive.games.battleship.example", tags=["strategy"]),
    GameInfo("Reversi", "haive.games.reversi.agent", "ReversiAgent", "board",
             "Flip opponent pieces to win", min_players=2, max_players=2,
             config_module="haive.games.reversi.config", config_class="ReversiConfig",
             example_module="haive.games.reversi.example", tags=["strategy"]),
    GameInfo("Mancala", "haive.games.mancala.agent", "MancalaAgent", "board",
             "Ancient seed-sowing game", min_players=2, max_players=2,
             config_module="haive.games.mancala.config", config_class="MancalaConfig",
             example_module="haive.games.mancala.example", tags=["strategy", "classic"]),

    # Card games
    GameInfo("Poker", "haive.games.poker.agent", "PokerAgent", "card",
             "Texas Hold'em poker", min_players=2, max_players=8,
             has_ui=True, config_module="haive.games.poker.config", config_class="PokerAgentConfig",
             example_module="haive.games.poker.example", tags=["cards", "betting"]),
    GameInfo("Hold'em", "haive.games.hold_em.game_agent", "HoldemGameAgent", "card",
             "Texas Hold'em variant", min_players=2, max_players=8,
             has_ui=True, config_module="haive.games.hold_em.config", config_class="HoldemGameAgentConfig",
             example_module="haive.games.hold_em.example", tags=["cards", "betting"]),
    GameInfo("Dominoes", "haive.games.dominoes.agent", "DominoesAgent", "card",
             "Classic domino tile game", min_players=2, max_players=4,
             has_ui=True, config_module="haive.games.dominoes.config", config_class="DominoesAgentConfig",
             example_module="haive.games.dominoes.example", tags=["tiles"]),

    # Strategy games
    GameInfo("Risk", "haive.games.risk.agent", "RiskAgent", "strategy",
             "World domination strategy", min_players=2, max_players=6,
             config_module="haive.games.risk.config", config_class="RiskConfig",
             example_module="haive.games.risk.example", tags=["strategy", "territory"]),
    GameInfo("Monopoly", "haive.games.monopoly.agent", "MonopolyAgent", "strategy",
             "Property trading game", min_players=2, max_players=6,
             has_ui=True, config_module="haive.games.monopoly.config", config_class="MonopolyGameAgentConfig",
             example_module="haive.games.monopoly.example", tags=["strategy", "economic"]),
    GameInfo("Nim", "haive.games.nim.agent", "NimAgent", "strategy",
             "Mathematical strategy game", min_players=2, max_players=2,
             has_ui=True, config_module="haive.games.nim.config", config_class="NimConfig",
             example_module="haive.games.nim.example", tags=["math", "simple"]),
    GameInfo("Fox & Geese", "haive.games.fox_and_geese.agent", "FoxAndGeeseAgent", "strategy",
             "Asymmetric pursuit game", min_players=2, max_players=2,
             has_ui=True, config_module="haive.games.fox_and_geese.config", config_class="FoxAndGeeseConfig",
             example_module="haive.games.fox_and_geese.example", tags=["asymmetric"]),

    # Social deduction
    GameInfo("Mafia", "haive.games.mafia.agent", "MafiaAgent", "social_deduction",
             "Social deduction party game", min_players=4, max_players=12,
             config_module="haive.games.mafia.config", config_class="MafiaAgentConfig",
             example_module="haive.games.mafia.example", tags=["social", "deduction"]),
    GameInfo("Among Us", "haive.games.among_us.agent", "AmongUsAgent", "social_deduction",
             "Impostor detection game", min_players=4, max_players=10,
             has_ui=True, config_module="haive.games.among_us.config", config_class="AmongUsAgentConfig",
             example_module="haive.games.among_us.demo", tags=["social", "deduction"]),
    GameInfo("Clue", "haive.games.clue.agent", "ClueAgent", "social_deduction",
             "Classic murder mystery", min_players=3, max_players=6,
             has_ui=True, config_module="haive.games.clue.config", config_class="ClueConfig",
             example_module="haive.games.clue.example", tags=["mystery", "deduction"]),

    # Single player / puzzle
    GameInfo("Mastermind", "haive.games.mastermind.agent", "MastermindAgent", "single_player",
             "Code-breaking logic puzzle", min_players=1, max_players=2,
             has_ui=True, config_module="haive.games.mastermind.config", config_class="MastermindConfig",
             example_module="haive.games.mastermind.example", tags=["puzzle", "logic"]),

    # Debate
    GameInfo("Debate", "haive.games.debate.agent", "DebateAgent", "debate",
             "Structured LLM debate", min_players=2, max_players=4,
             config_module="haive.games.debate.config", config_class="DebateAgentConfig",
             example_module="haive.games.debate.example", tags=["debate", "argumentation"]),
]


def try_import(module_path: str, class_name: str):
    """Try to import a class, return (cls, None) or (None, error_str)."""
    try:
        mod = importlib.import_module(module_path)
        cls = getattr(mod, class_name)
        return cls, None
    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)[:100]}"


def get_agents_by_category() -> dict[str, list[AgentInfo]]:
    """Group agents by category."""
    cats: dict[str, list[AgentInfo]] = {}
    for a in AGENT_REGISTRY:
        cats.setdefault(a.category, []).append(a)
    return cats


def get_games_by_category() -> dict[str, list[GameInfo]]:
    """Group games by category."""
    cats: dict[str, list[GameInfo]] = {}
    for g in GAME_REGISTRY:
        cats.setdefault(g.category, []).append(g)
    return cats


def get_class_docstring(module_path: str, class_name: str) -> str:
    """Get docstring for a class."""
    cls, err = try_import(module_path, class_name)
    if cls and cls.__doc__:
        return inspect.cleandoc(cls.__doc__)
    return ""


def try_import_game_config(game_info: GameInfo):
    """Try to import a game's config class."""
    if not game_info.config_module or not game_info.config_class:
        return None, "No config module specified"
    return try_import(game_info.config_module, game_info.config_class)
