from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Dict,
    Generator,
    Literal,
    Optional,
    Protocol,
    Type,
)

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

if TYPE_CHECKING:
    from haive.core.engine.base import Engine
    from haive.core.graph.state_graph.base_graph2 import BaseGraph
    from haive.core.schema.state_schema import StateSchema
    from langgraph.graph.graph import CompiledGraph


class AgentProtocol(Protocol):
    """Protocol defining the interface an Agent class must provide for mixins."""

    # Attributes from Agent class required by ExecutionMixin
    name: str
    verbose: bool
    input_schema: Optional[Type[BaseModel]]
    output_schema: Optional[Type[BaseModel]]
    state_schema: Optional[Type["StateSchema"]]
    engine: Optional["Engine"]
    graph: Optional["BaseGraph"]
    checkpointer: Optional[Any]
    store: Optional[Any]
    config: Optional[Any]  # For self.config.runnable_config
    runnable_config: Optional[RunnableConfig]

    # Private attributes
    _app: Optional["CompiledGraph"]
    _checkpoint_mode: Literal["sync", "async"]
    _async_checkpointer: Optional[Any]
    _disable_checkpointing: bool

    # Methods from Agent
    def compile(self, **kwargs) -> "CompiledGraph": ...

    def save_state_history(self, config: RunnableConfig) -> None: ...

    # Methods from ExecutionMixin itself
    def _prepare_input(self, input_data: Any) -> Any: ...

    def _prepare_runnable_config(
        self,
        thread_id: str | None = None,
        config: RunnableConfig | None = None,
        **kwargs,
    ) -> RunnableConfig: ...

    def _process_output(self, output_data: Any) -> Any: ...

    def run(
        self,
        input_data: Any,
        thread_id: str | None = None,
        debug: bool | None = None,
        config: RunnableConfig | None = None,
        **kwargs,
    ) -> Any: ...

    async def arun(
        self,
        input_data: Any,
        thread_id: str | None = None,
        config: RunnableConfig | None = None,
        debug: bool | None = None,
        **kwargs,
    ) -> Any: ...

    def stream(
        self,
        input_data: Any,
        thread_id: str | None = None,
        stream_mode: str = "values",
        config: RunnableConfig | None = None,
        debug: bool | None = None,
        **kwargs,
    ) -> Generator[dict[str, Any], None, None]: ...

    async def astream(
        self,
        input_data: Any,
        thread_id: str | None = None,
        stream_mode: str = "values",
        config: RunnableConfig | None = None,
        debug: bool | None = None,
        **kwargs,
    ) -> AsyncGenerator[dict[str, Any], None]: ...

    def _process_stream_chunk(self, chunk: Any, stream_mode: str) -> dict[str, Any]: ...
