from pydantic import BaseModel
from typing import Dict, Optional

class AgentAction(BaseModel):
   """
   Model representing an agent's action decision.

   Attributes:
       action (str): The specific action to be taken (e.g., "search_calendar", "analyze_tasks")
       thought (str): The reasoning process behind the action choice
       tool (Optional[str]): The specific tool to be used for the action (if needed)
       action_input (Optional[Dict]): Input parameters for the action

   Example:
       >>> action = AgentAction(
       ...     action="search_calendar",
       ...     thought="Need to check schedule conflicts",
       ...     tool="calendar_search",
       ...     action_input={"date_range": "next_week"}
       ... )
   """
   action: str      # Required action to be performed
   thought: str     # Reasoning behind the action
   tool: Optional[str] = None        # Optional tool specification
   action_input: Optional[Dict] = None  # Optional input parameters

class AgentOutput(BaseModel):
   """
   Model representing the output from an agent's action.

   Attributes:
       observation (str): The result or observation from executing the action
       output (Dict): Structured output data from the action

   Example:
       >>> output = AgentOutput(
       ...     observation="Found 3 free time slots next week",
       ...     output={
       ...         "free_slots": ["Mon 2PM", "Wed 10AM", "Fri 3PM"],
       ...         "conflicts": []
       ...     }
       ... )
   """
   observation: str  # Result or observation from the action
   output: Dict     # Structured output data