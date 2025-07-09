from typing import (
    Annotated,
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command, Send
from pydantic import (
    BaseModel,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_serializer,
    model_validator,
)
from typing_extensions import TypedDict

from haive.core.schema.state_schema import StateSchema

# Define a callable type alias more precisely
# Command destination types for better type checking
CommandGoto = Union[str, Literal["END"], Send, List[Union[Send, str]]]
# Type variables for better type safety
StateInput = TypeVar("StateInput", bound=Union[BaseModel, Dict[str, Any], Any])
StateOutput = TypeVar(
    "StateOutput", bound=Union[Dict[str, Any], Command, Send, List[Send], Any]
)
ConfigType = Union[RunnableConfig, Dict[str, Any], None]

NodeCallable = Callable[
    [
        Union[StateSchema, BaseModel, Dict[str, Any], TypedDict],
        Union[BaseModel, dict, TypedDict, RunnableConfig],
        Union[Send, Command, BaseModel, Dict, Any],
    ]
]
NodeReturnType = TypeVar(
    "NodeReturnType", bound=Union[BaseModel, dict, TypedDict, RunnableConfig]
)
StateType = TypeVar("StateType", bound=Union[StateSchema, BaseModel, Dict])
NodeType = TypeVar("NodeType", bound=Union[BaseModel, NodeCallable])
EdgeType = TypeVar("EdgeType", bound=BaseModel)
BranchType = TypeVar(
    "BranchType",
    bound=Union[
        BaseModel,
        Callable[
            [StateType, Optional[ConfigType]], Union[bool, CommandGoto, List[str]]
        ],
    ],
)


class BaseGraph(BaseModel, Generic[NodeType, EdgeType]):
    """
    Base class for all graph models.
    """

    nodes: List[NodeType] = Field(default_factory=list)
    edges: List[EdgeType] = Field(default_factory=list)

    @computed_field
    @property
    def number_of_nodes(self) -> int:
        """
        Get the number of nodes in the graph.
        """
        return len(self.nodes)

    @computed_field
    @property
    def number_of_edges(self) -> int:
        """
        Get the number of edges in the graph.
        """
        return len(self.edges)
