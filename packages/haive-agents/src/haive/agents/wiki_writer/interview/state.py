from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage

from agents.wiki_writer.interview.models import Editor
from agents.wiki_writer.interview.utils import (
    add_messages,
    update_editor,
    update_references,
)


class InterviewState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    references: Annotated[dict | None, update_references]
    editor: Annotated[Editor | None, update_editor]
