from typing import Annotated

from agents.wiki_writer.models import Editor
from agents.wiki_writer.utils import add_messages, update_editor, update_references
from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict


class InterviewState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    references: Annotated[dict | None, update_references]
    editor: Annotated[Editor | None, update_editor]
