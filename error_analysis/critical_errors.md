# Critical Errors Report

Errors that likely block functionality:

## Critical Errors (97)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/**init**.py:22

- **Message**: cannot import name 'SequentialAgent' from 'haive.agents.multi.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/base/**init**.py)
- **Package**: haive-agents
- **ID**: 79aa000b
- **Import Chain**:
  - from haive.agents.chain.examples import (
  - from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
  - from haive.agents.rag.hyde.agent_v2 import (

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/examples.py:21

- **Message**: cannot import name 'SequentialAgent' from 'haive.agents.multi.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/base/**init**.py)
- **Package**: haive-agents
- **ID**: 27c18379
- **Import Chain**:
  - from haive.agents.chain.examples import (
  - from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
  - from haive.agents.rag.hyde.agent_v2 import (

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/chain/multi_integration.py:0

- **Message**: cannot import name 'SequentialAgent' from 'haive.agents.multi.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/base/**init**.py)
- **Package**: haive-agents
- **ID**: 28ce1335
- **Import Chain**:
  - from haive.agents.chain.examples import (
  - from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
  - from haive.agents.rag.hyde.agent_v2 import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor.py:0

- **Message**: No module named 'haive.agents.experiments.supervisor.base_supervisor'
- **Package**: haive-agents
- **ID**: 73105d6c
- **Import Chain**:
  - from haive.agents.experiments.supervisor.base_supervisor import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/experiments/supervisor/**init**.py:39

- **Message**: No module named 'haive.agents.experiments.supervisor.base_supervisor'
- **Package**: haive-agents
- **ID**: fde7c888
- **Import Chain**:
  - from haive.agents.experiments.supervisor.base_supervisor import (

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/**init**.py:3

- **Message**: cannot import name 'tokenizer' from 'langchain_core.messages' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langchain_core/messages/**init**.py)
- **Package**: haive-agents
- **ID**: 2a050eee
- **Import Chain**:
  - from haive.agents.long_term_memory.agent import (
  - from langchain_core.messages import get_buffer_string, tokenizer
  - ImportError: cannot import name 'tokenizer' from 'langchain_core.messages' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langchain_core/messages/**init**.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/agent.py:9

- **Message**: cannot import name 'tokenizer' from 'langchain_core.messages' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langchain_core/messages/**init**.py)
- **Package**: haive-agents
- **ID**: 9b054315
- **Import Chain**:
  - from haive.agents.long_term_memory.agent import (
  - from langchain_core.messages import get_buffer_string, tokenizer
  - ImportError: cannot import name 'tokenizer' from 'langchain_core.messages' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langchain_core/messages/**init**.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/long_term_memory/state.py:0

- **Message**: cannot import name 'tokenizer' from 'langchain_core.messages' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langchain_core/messages/**init**.py)
- **Package**: haive-agents
- **ID**: b8767f4e
- **Import Chain**:
  - from haive.agents.long_term_memory.agent import (
  - from langchain_core.messages import get_buffer_string, tokenizer
  - ImportError: cannot import name 'tokenizer' from 'langchain_core.messages' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langchain_core/messages/**init**.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/**init**.py:3

- **Message**: cannot import name 'format_search_context' from 'haive.agents.memory.search.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/base.py)
- **Package**: haive-agents
- **ID**: 56a67986
- **Import Chain**:
  - from .base import (
  - ImportError: cannot import name 'format_search_context' from 'haive.agents.memory.search.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/base.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/base.py:0

- **Message**: cannot import name 'format_search_context' from 'haive.agents.memory.search.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/base.py)
- **Package**: haive-agents
- **ID**: e9453a77
- **Import Chain**:
  - from .base import (
  - ImportError: cannot import name 'format_search_context' from 'haive.agents.memory.search.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory/search/base.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/base/memory_state_original.py:16

- **Message**: No module named 'haive.agents.memory_reorganized.base.memory_models_standalone'
- **Package**: haive-agents
- **ID**: 97c886b2
- **Import Chain**:
  - from haive.agents.memory_reorganized.base.memory_models_standalone import (

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/search/**init**.py:3

- **Message**: cannot import name 'extract_memory_items' from 'haive.agents.memory_reorganized.search.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/search/base.py)
- **Package**: haive-agents
- **ID**: e563e0b0
- **Import Chain**:
  - from haive.agents.memory_reorganized.search.base import (
  - ImportError: cannot import name 'extract_memory_items' from 'haive.agents.memory_reorganized.search.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/memory_reorganized/search/base.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/llm_compiler/**init**.py:3

- **Message**: No module named 'haive.core.tools.dev_tools'
- **Package**: haive-agents
- **ID**: 4a53c913
- **Import Chain**:
  - from .agent import (
  - from .config import LLMCompilerAgentConfig
  - from haive.core.tools.dev_tools import python_repl_tool

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/**init**.py:3

- **Message**: No module named 'haive.agents.plan_and_execute'
- **Package**: haive-agents
- **ID**: a4c5cb4b
- **Import Chain**:
  - from .agent import PlanAndExecuteAgent, setup_workflow, should_end
  - from haive.agents.planning.plan_and_execute.engines import \*
  - from haive.agents.plan_and_execute.models import Act, Plan

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/engines.py:1

- **Message**: No module named 'haive.agents.plan_and_execute'
- **Package**: haive-agents
- **ID**: 302b1bce
- **Import Chain**:
  - from .agent import PlanAndExecuteAgent, setup_workflow, should_end
  - from haive.agents.planning.plan_and_execute.engines import \*
  - from haive.agents.plan_and_execute.models import Act, Plan

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/state.py:0

- **Message**: No module named 'haive.agents.plan_and_execute'
- **Package**: haive-agents
- **ID**: 987fd160
- **Import Chain**:
  - from .agent import PlanAndExecuteAgent, setup_workflow, should_end
  - from haive.agents.planning.plan_and_execute.engines import \*
  - from haive.agents.plan_and_execute.models import Act, Plan

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/**init**.py:0

- **Message**: No module named 'haive.agents.plan_and_execute'
- **Package**: haive-agents
- **ID**: 3ea022d9
- **Import Chain**:
  - from .agent import PlanAndExecuteAgent, setup_workflow, should_end
  - from haive.agents.planning.plan_and_execute.engines import \*
  - from haive.agents.plan_and_execute.models import Act, Plan

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/models.py:0

- **Message**: No module named 'haive.agents.plan_and_execute'
- **Package**: haive-agents
- **ID**: 8eb82a0b
- **Import Chain**:
  - from .agent import PlanAndExecuteAgent, setup_workflow, should_end
  - from haive.agents.planning.plan_and_execute.engines import \*
  - from haive.agents.plan_and_execute.models import Act, Plan

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/**init**.py:6

- **Message**: No module named 'models'
- **Package**: haive-agents
- **ID**: 882e6e1d
- **Import Chain**:
  - from .models.plans import ExecutionPlan
  - from models.join_step import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/planning/rewoo/models/**init**.py:3

- **Message**: No module named 'models'
- **Package**: haive-agents
- **ID**: 54ced7d0
- **Import Chain**:
  - from .models.plans import ExecutionPlan
  - from models.join_step import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/agentic/**init**.py:3

- **Message**: No module named 'agentic'
- **Package**: haive-agents
- **ID**: 929072df
- **Import Chain**:
  - from agentic.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/corrective/**init**.py:3

- **Message**: No module named 'corrective'
- **Package**: haive-agents
- **ID**: 2caed35f
- **Import Chain**:
  - from corrective.agent import CorrectiveRAGAgent, from_documents, grade_documents

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/corrective/agent.py:0

- **Message**: No module named 'corrective'
- **Package**: haive-agents
- **ID**: d101344e
- **Import Chain**:
  - from corrective.agent import CorrectiveRAGAgent, from_documents, grade_documents

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/**init**.py:3

- **Message**: cannot import name 'check_domain_relevance' from 'haive.agents.rag.db_rag.graph_db.agent' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/agent.py)
- **Package**: haive-agents
- **ID**: 8cfd02cb
- **Import Chain**:
  - from .agent import (
  - ImportError: cannot import name 'check_domain_relevance' from 'haive.agents.rag.db_rag.graph_db.agent' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/graph_db/agent.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/**init**.py:3

- **Message**: No module named 'sql_rag'
- **Package**: haive-agents
- **ID**: 94d5942c
- **Import Chain**:
  - from sql_rag.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/config.py:0

- **Message**: No module named 'sql_rag'
- **Package**: haive-agents
- **ID**: 2f7fc6ae
- **Import Chain**:
  - from sql_rag.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/db_rag/sql_rag/engines.py:0

- **Message**: No module named 'sql_rag'
- **Package**: haive-agents
- **ID**: 965460a4
- **Import Chain**:
  - from sql_rag.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/flare/**init**.py:3

- **Message**: No module named 'flare'
- **Package**: haive-agents
- **ID**: 73a6fad8
- **Import Chain**:
  - from flare.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/flare/agent.py:0

- **Message**: No module named 'flare'
- **Package**: haive-agents
- **ID**: 413d3495
- **Import Chain**:
  - from flare.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/fusion/**init**.py:3

- **Message**: No module named 'fusion'
- **Package**: haive-agents
- **ID**: d9e89b87
- **Import Chain**:
  - from fusion.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/fusion/agent.py:0

- **Message**: No module named 'fusion'
- **Package**: haive-agents
- **ID**: 597b94bd
- **Import Chain**:
  - from fusion.agent import (

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/**init**.py:4

- **Message**: cannot import name 'SequentialAgent' from 'haive.agents.multi.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/base/**init**.py)
- **Package**: haive-agents
- **ID**: b5824698
- **Import Chain**:
  - from haive.agents.rag.hyde.agent_v2 import (
  - from haive.agents.multi.base import SequentialAgent
  - ImportError: cannot import name 'SequentialAgent' from 'haive.agents.multi.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/base/**init**.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/hyde/agent_v2.py:19

- **Message**: cannot import name 'SequentialAgent' from 'haive.agents.multi.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/base/**init**.py)
- **Package**: haive-agents
- **ID**: 6a3e9295
- **Import Chain**:
  - from haive.agents.rag.hyde.agent_v2 import (
  - from haive.agents.multi.base import SequentialAgent
  - ImportError: cannot import name 'SequentialAgent' from 'haive.agents.multi.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/base/**init**.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/llm_rag/**init**.py:3

- **Message**: No module named 'llm_rag'
- **Package**: haive-agents
- **ID**: 79feaf76
- **Import Chain**:
  - from llm_rag.agent import (

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/**init**.py:25

- **Message**: cannot import name 'documents' from 'haive.agents.rag.multi_agent_rag.agents' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py)
- **Package**: haive-agents
- **ID**: 0a059fc7
- **Import Chain**:
  - from haive.agents.rag.multi_agent_rag.agents import (
  - ImportError: cannot import name 'documents' from 'haive.agents.rag.multi_agent_rag.agents' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/enhanced_state_schemas.py:0

- **Message**: cannot import name 'documents' from 'haive.agents.rag.multi_agent_rag.agents' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py)
- **Package**: haive-agents
- **ID**: 168444a9
- **Import Chain**:
  - from haive.agents.rag.multi_agent_rag.agents import (
  - ImportError: cannot import name 'documents' from 'haive.agents.rag.multi_agent_rag.agents' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/grading_components.py:0

- **Message**: cannot import name 'documents' from 'haive.agents.rag.multi_agent_rag.agents' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py)
- **Package**: haive-agents
- **ID**: 95e65ed6
- **Import Chain**:
  - from haive.agents.rag.multi_agent_rag.agents import (
  - ImportError: cannot import name 'documents' from 'haive.agents.rag.multi_agent_rag.agents' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/state.py:0

- **Message**: cannot import name 'documents' from 'haive.agents.rag.multi_agent_rag.agents' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py)
- **Package**: haive-agents
- **ID**: 6bb79606
- **Import Chain**:
  - from haive.agents.rag.multi_agent_rag.agents import (
  - ImportError: cannot import name 'documents' from 'haive.agents.rag.multi_agent_rag.agents' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_agent_rag/agents.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_query/agent.py:18

- **Message**: cannot import name 'SequentialAgent' from 'haive.agents.multi.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/base/**init**.py)
- **Package**: haive-agents
- **ID**: b8f8ae57
- **Import Chain**:
  - from haive.agents.multi.base import SequentialAgent
  - ImportError: cannot import name 'SequentialAgent' from 'haive.agents.multi.base' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/multi/base/**init**.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/multi_strategy/**init**.py:3

- **Message**: No module named 'multi_strategy'
- **Package**: haive-agents
- **ID**: c8fa9d59
- **Import Chain**:
  - from multi_strategy.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/rag/self_corr/**init**.py:3

- **Message**: No module named 'self_corr'
- **Package**: haive-agents
- **ID**: 6c0e51a0
- **Import Chain**:
  - from self_corr.agent import (

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/**init**.py:20

- **Message**: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)
- **Package**: haive-agents
- **ID**: 68a93153
- **Import Chain**:
  - from haive.agents.react_class.react_agent2.agent2 import (
  - ImportError: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent.py:0

- **Message**: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)
- **Package**: haive-agents
- **ID**: 3d61c21c
- **Import Chain**:
  - from haive.agents.react_class.react_agent2.agent2 import (
  - ImportError: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/config.py:0

- **Message**: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)
- **Package**: haive-agents
- **ID**: 302febd6
- **Import Chain**:
  - from haive.agents.react_class.react_agent2.agent2 import (
  - ImportError: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/example.py:0

- **Message**: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)
- **Package**: haive-agents
- **ID**: 2373991a
- **Import Chain**:
  - from haive.agents.react_class.react_agent2.agent2 import (
  - ImportError: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/example3.py:0

- **Message**: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)
- **Package**: haive-agents
- **ID**: 77e866f5
- **Import Chain**:
  - from haive.agents.react_class.react_agent2.agent2 import (
  - ImportError: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/models.py:0

- **Message**: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)
- **Package**: haive-agents
- **ID**: 6e50e673
- **Import Chain**:
  - from haive.agents.react_class.react_agent2.agent2 import (
  - ImportError: cannot import name 'chat' from 'haive.agents.react_class.react_agent2.agent2' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_agent2/agent2.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/**init**.py:3

- **Message**: cannot import name 'run' from 'haive.agents.react_class.react_v2.agent' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/agent.py)
- **Package**: haive-agents
- **ID**: 15d2b565
- **Import Chain**:
  - from haive.agents.react_class.react_v2.agent import ReactAgent, run, setup_workflow
  - ImportError: cannot import name 'run' from 'haive.agents.react_class.react_v2.agent' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v2/agent.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/react_class/react_v3/**init**.py:3

- **Message**: No module named 'react_v3'
- **Package**: haive-agents
- **ID**: c9e384e6
- **Import Chain**:
  - from react_v3.agent import (

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/**init**.py:7

- **Message**: cannot import name 'from_llms' from 'haive.agents.reasoning_and_critique.lats.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/config.py)
- **Package**: haive-agents
- **ID**: 7d3fa0fd
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.lats.config import LATSAgentConfig, from_llms
  - ImportError: cannot import name 'from_llms' from 'haive.agents.reasoning_and_critique.lats.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/config.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/state.py:0

- **Message**: cannot import name 'from_llms' from 'haive.agents.reasoning_and_critique.lats.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/config.py)
- **Package**: haive-agents
- **ID**: 8a03adce
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.lats.config import LATSAgentConfig, from_llms
  - ImportError: cannot import name 'from_llms' from 'haive.agents.reasoning_and_critique.lats.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/config.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/**init**.py:0

- **Message**: cannot import name 'from_llms' from 'haive.agents.reasoning_and_critique.lats.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/config.py)
- **Package**: haive-agents
- **ID**: e934d8c1
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.lats.config import LATSAgentConfig, from_llms
  - ImportError: cannot import name 'from_llms' from 'haive.agents.reasoning_and_critique.lats.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/config.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/v2/models.py:0

- **Message**: cannot import name 'from_llms' from 'haive.agents.reasoning_and_critique.lats.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/config.py)
- **Package**: haive-agents
- **ID**: ae7e640f
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.lats.config import LATSAgentConfig, from_llms
  - ImportError: cannot import name 'from_llms' from 'haive.agents.reasoning_and_critique.lats.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/config.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/**init**.py:3

- **Message**: cannot import name 'max_inference_chain' from 'haive.agents.reasoning_and_critique.logic.models' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/models.py)
- **Package**: haive-agents
- **ID**: 36326bfb
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.logic.models import (
  - ImportError: cannot import name 'max_inference_chain' from 'haive.agents.reasoning_and_critique.logic.models' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/models.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/models.py:0

- **Message**: cannot import name 'max_inference_chain' from 'haive.agents.reasoning_and_critique.logic.models' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/models.py)
- **Package**: haive-agents
- **ID**: 884e36a7
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.logic.models import (
  - ImportError: cannot import name 'max_inference_chain' from 'haive.agents.reasoning_and_critique.logic.models' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/logic/models.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/**init**.py:3

- **Message**: cannot import name 'from_llm_and_tools' from 'haive.agents.reasoning_and_critique.mcts.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/config.py)
- **Package**: haive-agents
- **ID**: 8ccca89f
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.mcts.config import (
  - ImportError: cannot import name 'from_llm_and_tools' from 'haive.agents.reasoning_and_critique.mcts.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/config.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/state.py:0

- **Message**: cannot import name 'from_llm_and_tools' from 'haive.agents.reasoning_and_critique.mcts.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/config.py)
- **Package**: haive-agents
- **ID**: 3bbf85c2
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.mcts.config import (
  - ImportError: cannot import name 'from_llm_and_tools' from 'haive.agents.reasoning_and_critique.mcts.config' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/mcts/config.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/**init**.py:3

- **Message**: cannot import name 'add_improvement' from 'haive.agents.reflection.state' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/state.py)
- **Package**: haive-agents
- **ID**: 9e76900e
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.reflection.agent import (
  - from haive.agents.reflection.config import ReflectionAgentConfig
  - from haive.agents.reflection.state import (

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflection/agent.py:7

- **Message**: cannot import name 'add_improvement' from 'haive.agents.reflection.state' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/state.py)
- **Package**: haive-agents
- **ID**: 6d6ac9f9
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.reflection.agent import (
  - from haive.agents.reflection.config import ReflectionAgentConfig
  - from haive.agents.reflection.state import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/**init**.py:3

- **Message**: No module named 'haive.agents.reflexion'
- **Package**: haive-agents
- **ID**: 72846be6
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.reflexion.agent import (
  - from haive.agents.reflexion.config import ReflexionConfig

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/reflexion/agent.py:3

- **Message**: No module named 'haive.agents.reflexion'
- **Package**: haive-agents
- **ID**: 255ea8fd
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.reflexion.agent import (
  - from haive.agents.reflexion.config import ReflexionConfig

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/**init**.py:3

- **Message**: cannot import name 'Config' from 'haive.agents.reasoning_and_critique.self_discover.v2.models' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/models.py)
- **Package**: haive-agents
- **ID**: 4b766d00
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.self_discover.v2.models import (
  - ImportError: cannot import name 'Config' from 'haive.agents.reasoning_and_critique.self_discover.v2.models' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/models.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/state.py:0

- **Message**: cannot import name 'Config' from 'haive.agents.reasoning_and_critique.self_discover.v2.models' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/models.py)
- **Package**: haive-agents
- **ID**: 69e3e809
- **Import Chain**:
  - from haive.agents.reasoning_and_critique.self_discover.v2.models import (
  - ImportError: cannot import name 'Config' from 'haive.agents.reasoning_and_critique.self_discover.v2.models' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/self_discover/v2/models.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/**init**.py:3

- **Message**: No module named 'modular'
- **Package**: haive-agents
- **ID**: 054f031a
- **Import Chain**:
  - from modular.state import ToTState, update_candidates

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/**init**.py:32

- **Message**: cannot import name 'add_improvement' from 'haive.agents.reflection.state' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/state.py)
- **Package**: haive-agents
- **ID**: c3d979e9
- **Import Chain**:
  - from haive.agents.reflection.state import (
  - ImportError: cannot import name 'add_improvement' from 'haive.agents.reflection.state' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/state.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/state.py:0

- **Message**: cannot import name 'add_improvement' from 'haive.agents.reflection.state' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/state.py)
- **Package**: haive-agents
- **ID**: 3cd4c60b
- **Import Chain**:
  - from haive.agents.reflection.state import (
  - ImportError: cannot import name 'add_improvement' from 'haive.agents.reflection.state' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/reflection/state.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/research/perplexity/pro_search/search/**init**.py:3

- **Message**: No module named 'perplexity_search_models'
- **Package**: haive-agents
- **ID**: c702d0f2
- **Import Chain**:
  - from haive.agents.research.perplexity.pro_search.search.models import (
  - from perplexity_search_models import QueryBatch, QueryReasoning, SearchSynthesis

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/**init**.py:96

- **Message**: cannot import name 'build_graph' from 'haive.agents.supervisor.simple_supervisor' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/simple_supervisor.py)
- **Package**: haive-agents
- **ID**: 5df6f699
- **Import Chain**:
  - from haive.agents.supervisor.simple_supervisor import (
  - ImportError: cannot import name 'build_graph' from 'haive.agents.supervisor.simple_supervisor' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/simple_supervisor.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/dynamic/**init**.py:0

- **Message**: cannot import name 'build_graph' from 'haive.agents.supervisor.simple_supervisor' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/simple_supervisor.py)
- **Package**: haive-agents
- **ID**: d583be89
- **Import Chain**:
  - from haive.agents.supervisor.simple_supervisor import (
  - ImportError: cannot import name 'build_graph' from 'haive.agents.supervisor.simple_supervisor' (/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/supervisor/simple_supervisor.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/**init**.py:3

- **Message**: No module named 'task_analysis'
- **Package**: haive-agents
- **ID**: 60cb8143
- **Import Chain**:
  - from task_analysis.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/base/**init**.py:0

- **Message**: No module named 'task_analysis'
- **Package**: haive-agents
- **ID**: c4e5cd32
- **Import Chain**:
  - from task_analysis.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/base/models.py:0

- **Message**: No module named 'task_analysis'
- **Package**: haive-agents
- **ID**: b488a483
- **Import Chain**:
  - from task_analysis.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/complexity/**init**.py:0

- **Message**: No module named 'task_analysis'
- **Package**: haive-agents
- **ID**: 54736c8d
- **Import Chain**:
  - from task_analysis.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/task_analysis/execution/**init**.py:0

- **Message**: No module named 'task_analysis'
- **Package**: haive-agents
- **ID**: 62f0746e
- **Import Chain**:
  - from task_analysis.agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/**init**.py:3

- **Message**: No module named 'wiki_writer'
- **Package**: haive-agents
- **ID**: 2592f9d8
- **Import Chain**:
  - from wiki_writer.agent import WikiWriterAgent, WikiWriterAgentConfig

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/wiki_writer/interview/**init**.py:0

- **Message**: No module named 'wiki_writer'
- **Package**: haive-agents
- **ID**: bb0d4165
- **Import Chain**:
  - from wiki_writer.agent import WikiWriterAgent, WikiWriterAgentConfig

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/splitters/**init**.py:80

- **Message**: cannot import name 'Document' from 'langchain.document_loaders.base' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langchain/document_loaders/base.py)
- **Package**: haive-core
- **ID**: d6e50d79
- **Import Chain**:
  - from haive.core.engine.document.splitters.base import ( # Core splitters; Token-based splitters; Language-specific splitters; NLP-based splitters; Types and utilities
  - from langchain.document_loaders.base import Document
  - ImportError: cannot import name 'Document' from 'langchain.document_loaders.base' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langchain/document_loaders/base.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/engine/document/transformers/**init**.py:78

- **Message**: No module named 'haive.core.common.config'
- **Package**: haive-core
- **ID**: 12ab49ff
- **Import Chain**:
  - from haive.core.engine.document.transformers.engine import (
  - from haive.core.common.config.runnable import RunnableConfig

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/graph/node/state_updating_validation_node.py:9

- **Message**: cannot import name 'END' from 'langgraph.types' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langgraph/types.py)
- **Package**: haive-core
- **ID**: 447eaee2
- **Import Chain**:
  - from langgraph.types import END, Send
  - ImportError: cannot import name 'END' from 'langgraph.types' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langgraph/types.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/app.py:39

- **Message**: No module named 'haive.dataflow.api.routes.auth'
- **Package**: haive-dataflow
- **ID**: 7b17ecf5
- **Import Chain**:
  - from haive.dataflow.api.routes.agent_routes import router as agent_router
  - from haive.dataflow.api.routes.auth.dependencies import require_auth

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive/dataflow/api/game_api.py:35

- **Message**: No module named 'haive.dataflow.api.engine'
- **Package**: haive-dataflow
- **ID**: 6bd27880
- **Import Chain**:
  - from haive.dataflow.api.engine.agent.agent import Agent

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/**init**.py:3

- **Message**: No module named 'game'
- **Package**: haive-games
- **ID**: 979f0ccf
- **Import Chain**:
  - from haive.games.core.game.core_board import (
  - from game.core.piece import GamePiece

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/core_board.py:15

- **Message**: No module named 'game'
- **Package**: haive-games
- **ID**: 68c4581c
- **Import Chain**:
  - from haive.games.core.game.core_board import (
  - from game.core.piece import GamePiece

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/**init**.py:3

- **Message**: cannot import name 'DebateV2Agent' from 'haive.games.debate_v2.agent' (/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/agent.py)
- **Package**: haive-games
- **ID**: 34f1d48d
- **Import Chain**:
  - from haive.games.debate_v2.agent import DebateV2Agent, DebateV2AgentConfig
  - ImportError: cannot import name 'DebateV2Agent' from 'haive.games.debate_v2.agent' (/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/debate_v2/agent.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/**init**.py:5

- **Message**: cannot import name 'MonopolyGame' from 'haive.games.monopoly.game' (/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/**init**.py)
- **Package**: haive-games
- **ID**: d65a91d0
- **Import Chain**:
  - from haive.games.monopoly.game import Card, MonopolyGame, SpecialSquareType
  - ImportError: cannot import name 'MonopolyGame' from 'haive.games.monopoly.game' (/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/**init**.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/config.py:0

- **Message**: cannot import name 'MonopolyGame' from 'haive.games.monopoly.game' (/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/**init**.py)
- **Package**: haive-games
- **ID**: 9a5d3fd1
- **Import Chain**:
  - from haive.games.monopoly.game import Card, MonopolyGame, SpecialSquareType
  - ImportError: cannot import name 'MonopolyGame' from 'haive.games.monopoly.game' (/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/monopoly/game/**init**.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/**init**.py:3

- **Message**: No module named 'mixins'
- **Package**: haive-mcp
- **ID**: 3e458bb5
- **Import Chain**:
  - from haive.mcp.agents.documentation_agent import (
  - from haive.mcp.mixins.mcp_mixin import MCPMixin
  - from mixins.mcp_mixin import MCPMixin, get_mcp_status, model_post_init, setup_mcp

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/agents/documentation_agent.py:73

- **Message**: No module named 'mixins'
- **Package**: haive-mcp
- **ID**: e292478e
- **Import Chain**:
  - from haive.mcp.agents.documentation_agent import (
  - from haive.mcp.mixins.mcp_mixin import MCPMixin
  - from mixins.mcp_mixin import MCPMixin, get_mcp_status, model_post_init, setup_mcp

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/**init**.py:33

- **Message**: No module named 'mixins'
- **Package**: haive-mcp
- **ID**: ce32f992
- **Import Chain**:
  - from haive.mcp.downloader.integration import (
  - from haive.mcp.agents import MCPAgent, TransferableMCPAgent
  - from haive.mcp.agents.documentation_agent import (

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/downloader/integration.py:48

- **Message**: No module named 'mixins'
- **Package**: haive-mcp
- **ID**: c7dc8789
- **Import Chain**:
  - from haive.mcp.downloader.integration import (
  - from haive.mcp.agents import MCPAgent, TransferableMCPAgent
  - from haive.mcp.agents.documentation_agent import (

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/manager.py:74

- **Message**: cannot import name 'stdio_client' from 'langchain_mcp_adapters.client' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langchain_mcp_adapters/client.py)
- **Package**: haive-mcp
- **ID**: 5da62c3f
- **Import Chain**:
  - from langchain_mcp_adapters.client import (
  - ImportError: cannot import name 'stdio_client' from 'langchain_mcp_adapters.client' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/langchain_mcp_adapters/client.py)

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mixins/**init**.py:3

- **Message**: No module named 'mixins'
- **Package**: haive-mcp
- **ID**: a329f052
- **Import Chain**:
  - from mixins.mcp_mixin import MCPMixin, get_mcp_status, model_post_init, setup_mcp

### ModuleNotFoundError in /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/mixins/mcp_mixin.py:0

- **Message**: No module named 'mixins'
- **Package**: haive-mcp
- **ID**: 65dee835
- **Import Chain**:
  - from mixins.mcp_mixin import MCPMixin, get_mcp_status, model_post_init, setup_mcp

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/**init**.py:4

- **Message**: cannot import name 'SSEServerTransport' from 'mcp.server.sse' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/mcp/server/sse.py)
- **Package**: haive-mcp
- **ID**: 1cc44e2c
- **Import Chain**:
  - from haive.mcp.servers.http_server import run_server
  - from mcp.server.sse import SSEServerTransport
  - ImportError: cannot import name 'SSEServerTransport' from 'mcp.server.sse' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/mcp/server/sse.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/servers/http_server.py:15

- **Message**: cannot import name 'SSEServerTransport' from 'mcp.server.sse' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/mcp/server/sse.py)
- **Package**: haive-mcp
- **ID**: dc3aca05
- **Import Chain**:
  - from haive.mcp.servers.http_server import run_server
  - from mcp.server.sse import SSEServerTransport
  - ImportError: cannot import name 'SSEServerTransport' from 'mcp.server.sse' (/home/will/Projects/haive/backend/haive/.venv/lib/python3.12/site-packages/mcp/server/sse.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/**init**.py:3

- **Message**: cannot import name 'explain_recommendation' from 'haive.mcp.tools.ai_assistant' (/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py)
- **Package**: haive-mcp
- **ID**: ed537f45
- **Import Chain**:
  - from haive.mcp.tools.ai_assistant import (
  - ImportError: cannot import name 'explain_recommendation' from 'haive.mcp.tools.ai_assistant' (/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive/mcp/tools/ai_assistant.py)

### ImportError in /home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/**init**.py:7

- **Message**: cannot import name 'create_client' from 'haive.tools.tools.toolkits.amadues_toolkit' (/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/amadues_toolkit.py)
- **Package**: haive-tools
- **ID**: a179179e
- **Import Chain**:
  - from haive.tools.tools.toolkits.amadues_toolkit import (
  - ImportError: cannot import name 'create_client' from 'haive.tools.tools.toolkits.amadues_toolkit' (/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive/tools/tools/toolkits/amadues_toolkit.py)
