from haive.core.engine.agent.config import AgentConfig
from haive.core.engine.agent.react import ReactAgentConfig
from haive.core.engine.base import Engine
from pydantic import BaseModel

from haive.agents.planning.plan_and_execute.state import PlanAndExecuteState


class PlanAndExecuteConfig(AgentConfig):
    engines: dict[str, Engine] = {
        "planner": planner_aug_llm_config,
        "replanner": rPlanAndExecuteStatenfig,
    }
    agent_executor_config: ReactAgentConfig = ReactAgentConfig()
    state_schema: type[BaseModel] | list[BaseModel] = PlanAndExecuteState
    default_input_schema: dict[str, list] = {"input": [("user", "{}")]}
