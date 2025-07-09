from typing import Literal

from langchain_community.graphs.graph_document import GraphDocument
from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field, model_validator


class IterativeGraphTransformerState(BaseModel):
    """The state of the iterative graph transformer."""

    contents: list[str | Document | AnyMessage | dict] = Field(
        description="The contents to convert into a knowledge graph."
    )
    index: int = Field(default=0)
    graph_doc: GraphDocument | None = Field(default=None)

    def should_refine(self) -> Literal["refine_summary", "__end__"]:
        return "refine_summary" if self.index < len(self.contents) else "__end__"

    @model_validator(mode="before")
    @classmethod
    def normalize_contents(cls, values: dict) -> dict:
        """Normalize all entries in `contents` to be `Document` objects."""
        contents = values.get("contents")
        if contents is None:
            return values

        docs = []
        if isinstance(contents, str):
            docs = [Document(page_content=contents)]
        elif isinstance(contents, list):
            for i, item in enumerate(contents):
                if isinstance(item, Document):
                    docs.append(item)
                elif isinstance(item, str):
                    docs.append(Document(page_content=item))
                elif isinstance(item, dict) and "page_content" in item:
                    docs.append(Document(**item))
                else:
                    raise ValueError(
                        f"Unsupported content type in `contents` at index {i}: {type(item)}"
                    )
        else:
            raise ValueError(
                f"Expected `contents` to be str or list, got {type(contents)}"
            )

        values["contents"] = docs
        return values
