import json

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import ToolMessage
from langchain_core.output_parsers import PydanticToolsParser
from langgraph.types import Command
from pydantic import BaseModel, ValidationError


class ResponderWithRetries:
    """A responder that retries a given runnable a number of times if it fails to validate."""

    def __init__(
        self, aug_llm_config: AugLLMConfig, num_retries: int = 3, name: str = None
    ):
        """Args:
        aug_llm_config: The config for the LLM to use.
        num_retries: The number of times to retry the runnable.
        """
        self.runnable = aug_llm_config.create_runnable()
        print("runnable", self.runnable)
        # self.runnable.invoke(state.messages)
        print("setting validator")
        print("name", name)
        self.aug_llm_config = aug_llm_config
        print("tools", aug_llm_config.tools)
        self.validator = PydanticToolsParser(tools=aug_llm_config.tools)
        print("validator set")
        self.name = name
        self.num_retries = num_retries

    def respond(self, state: BaseModel):
        """Respond to the user's message."""
        response = []
        reflections_count = state.reflections_count
        for attempt in range(self.num_retries):
            print("attempt", attempt)
            response = self.runnable.invoke(
                {"messages": state.messages}, {"tags": [f"attempt:{attempt}"]}
            )
            try:
                print("validating response")
                print("response", response)
                self.validator.invoke(response)
                print("response validated")
                if self.name == "revisor":
                    return Command(
                        update={
                            "messages": response,
                            "reflections_count": reflections_count + 1,
                        }
                    )
                return Command(update={"messages": response})
            except ValidationError as e:
                print("validation error")
                print("response", response)
                response = [response] + [
                    ToolMessage(
                        content=f"{e!r}\n\nPay close attention to the function schema.\n\n"
                        + json.dumps(self.validator.schema(), indent=2)
                        + "\nRespond by fixing all validation errors.",
                        tool_call_id=response.tool_calls[0]["id"],
                    ),
                ]
                # print('messages',message)
                # return Command(update={"messages": message})
        if self.name == "revisor":
            return Command(
                update={
                    "messages": response,
                    "reflections_count": reflections_count + 1,
                }
            )
        return Command(update={"messages": response})
        # return Command(update={"messages": response})
