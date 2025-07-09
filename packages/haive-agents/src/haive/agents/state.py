import logging
from typing import Any

from agents.web_nav.models import BBox, Prediction
from langchain_core.messages import BaseMessage
from playwright.async_api import Page
from pydantic import BaseModel, ConfigDict, Field, field_validator

# -----------------------------------------------------------------------------
# Debugging Utility
# -----------------------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG)


def debug_print(message: str):
    """Helper function to print and log debug messages."""
    print(f"[DEBUG] {message}")
    logging.debug(message)


# -----------------------------------------------------------------------------
# WebNavState Class
# -----------------------------------------------------------------------------
class WebNavState(BaseModel):
    """Web Navigation State Model with Playwright Support & Serialization

    This model holds the state for a web navigation agent:
      - 'page': the live Playwright page (excluded from serialization)
      - 'page_url': the page URL (used for persistence)
      - Other fields (input, img, bboxes, prediction, scratchpad, observation)
    """

    # Use private attribute to store Page object
    _page: Page | None = None

    page_url: str | None = Field(
        default=None, description="URL of the Playwright page."
    )
    input: str = Field(..., description="User request.")
    img: str | None = Field(
        default=None, description="Base64 encoded screenshot (plain, no prefix)."
    )
    bboxes: list[BBox] = Field(
        default_factory=list, description="Bounding boxes from annotation."
    )
    prediction: Prediction | None = Field(
        default=None, description="The agent's output."
    )
    scratchpad: list[BaseMessage] = Field(
        default_factory=list, description="Intermediate system messages."
    )
    observation: str | None = Field(
        default=None, description="The most recent tool response."
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        # Remove Page from json_encoders to ensure it's not serialized
    )

    def __init__(self, **kwargs):
        """Extract page object and initialize the model."""
        # Extract page from kwargs and store it separately
        page = kwargs.pop("page", None)
        super().__init__(**kwargs)
        self._page = page
        debug_print("WebNavState initialized with values (excluding page)")

    @field_validator("prediction", mode="before")
    def ensure_prediction(cls, v):
        """Ensures prediction is either None or a valid object."""
        debug_print(f"Validating prediction: {v}")
        if isinstance(v, list) and len(v) == 0:
            debug_print("Prediction was an empty list. Converting to None.")
            return None
        return v

    @property
    def page(self) -> Page | None:
        """Getter for page property."""
        return self._page

    @page.setter
    def page(self, value: Page | None):
        """Setter for page property."""
        self._page = value
        if value:
            self.page_url = value.url

    def model_dump(self, **kwargs) -> dict[str, Any]:
        """Override model_dump to exclude _page attribute."""
        data = super().model_dump(**kwargs)
        # Make sure _page is not included
        if "_page" in data:
            del data["_page"]
        return data

    def dict(self, **kwargs) -> dict[str, Any]:
        """For compatibility with older Pydantic versions."""
        return self.model_dump(**kwargs)

    @classmethod
    async def from_page(cls, page: Page, **kwargs) -> "WebNavState":
        """Create a WebNavState from a live Playwright page.
        Both the live 'page' and its URL are set.
        """
        debug_print(f"Creating WebNavState from page: {page.url}")
        page_url = page.url if page else None
        state = cls(page=page, page_url=page_url, **kwargs)
        debug_print("WebNavState created successfully")
        return state

    async def to_page(self, browser) -> Page:
        """Recreate a live Playwright page from the stored URL."""
        debug_print(f"Recreating Playwright page for URL: {self.page_url}")
        page = await browser.new_page()
        if self.page_url:
            await page.goto(self.page_url)
        self._page = page
        debug_print(f"Page navigation complete for: {self.page_url}")
        return page
