import asyncio
import base64
import logging
import platform
import re
import uuid
from typing import Any

from haive.core.engine.agent.agent import Agent, AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from IPython import display
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.runnables import RunnableLambda
from langgraph.graph import START
from playwright.async_api import Browser, Page, async_playwright
from playwright_stealth import stealth_async
from pydantic import BaseModel, ConfigDict, Field, field_validator

# -----------------------------------------------------------------------------
# Debugging Utility
# -----------------------------------------------------------------------------
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def debug_print(message: str):
    """Helper function to print and log debug messages."""
    print(f"[DEBUG] {message}")
    logger.debug(message)


# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------
class BBox(BaseModel):
    """Bounding box for web elements."""

    x: float
    y: float
    width: float
    height: float
    ariaLabel: str | None = None
    text: str | None = None
    type: str


class Prediction(BaseModel):
    """Agent prediction model."""

    thought: str
    action: str
    args: list[str] | None = None

    @field_validator("args", mode="before")
    def ensure_args(cls, v):
        """Ensures args is a list."""
        if v is None:
            return []
        return v


# -----------------------------------------------------------------------------
# WebNavState Class
# -----------------------------------------------------------------------------
class WebNavState(BaseModel):
    """Web Navigation State Model with Playwright Support"""

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
    observation: str = Field(default="", description="The most recent tool response.")
    bbox_descriptions: str | None = Field(
        default=None, description="Formatted bounding box descriptions."
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @field_validator("prediction", mode="before")
    def ensure_prediction(cls, v):
        """Ensures prediction is either None or a valid object."""
        debug_print(f"Validating prediction: {v}")
        if isinstance(v, list) and len(v) == 0:
            debug_print("Prediction was an empty list. Converting to None.")
            return None
        return v


# -----------------------------------------------------------------------------
# WebNavAgentConfig
# -----------------------------------------------------------------------------
class WebNavAgentConfig(AgentConfig):
    """Configuration for the Web Navigator Agent."""

    aug_llm_config: AugLLMConfig = Field(
        ..., description="LLM config for Web Navigator"
    )
    headless: bool = Field(default=False, description="Run browser in headless mode")
    max_steps: int = Field(default=3, description="Maximum steps")
    state_schema: type[BaseModel] = Field(
        default=WebNavState, description="State schema for the agent"
    )


# -----------------------------------------------------------------------------
# WebNavAgent Implementation
# -----------------------------------------------------------------------------
class WebNavAgent(Agent[WebNavAgentConfig]):
    """An interactive web navigation agent using Playwright & LangGraph with integrated tools."""

    def __init__(self, config: WebNavAgentConfig):
        self.config = config
        self.headless = config.headless
        self.max_steps = config.max_steps
        self.screenshots = []
        self.browser: Browser | None = None
        self.page: Page | None = None
        self.state: WebNavState | None = None
        # self.st
        # Initialize LLM
        self.llm = compose_runnable(config.aug_llm_config)

        # JavaScript for page annotation
        with open("src/haive/agents/web_nav/utils/mark.js") as f:
            self.mark_page_script = f.read()

        # Build agent chain: annotate -> format_descriptions -> LLM -> parse
        # Build agent chain
        self.agent = (
            RunnableLambda(self.annotate_page)
            | RunnableLambda(
                lambda state_dict: {
                    **state_dict,
                    "bbox_descriptions": self.format_descriptions(state_dict),
                }
            )
            | RunnableLambda(
                lambda enriched_state: {
                    **enriched_state,
                    "prediction": self.llm.invoke(
                        enriched_state
                    ).model_dump(),  # Convert Prediction to dict
                }
            )
        )

        # Initialize parent agent
        super().__init__(config)

    # -------------------------------------------------------------------------
    # Core Agent Functions
    # -------------------------------------------------------------------------
    def setup_workflow(self):
        """Sets up the workflow graph for the agent."""
        # Add agent node
        self.graph.add_node("agent", self.agent)
        self.graph.add_edge(START, "agent")

        # Add update_scratchpad node
        self.graph.add_node("update_scratchpad", self.update_scratchpad)
        self.graph.add_edge("update_scratchpad", "agent")

        # Add tool nodes
        tools = {
            "Click": self.tool_click,
            "Type": self.tool_type,
            "Scroll": self.tool_scroll,
            "Wait": self.tool_wait,
            "GoBack": self.tool_go_back,
            "Google": self.tool_to_google,
            "ANSWER": self.tool_answer,
        }

        for node_name, tool_func in tools.items():
            self.graph.add_node(
                node_name,
                RunnableLambda(tool_func)
                | RunnableLambda(lambda observation: {"observation": observation}),
            )
            self.graph.add_edge(node_name, "update_scratchpad")

        # Add conditional routing
        self.graph.add_conditional_edges("agent", self.select_tool)

    def select_tool(self, state: dict[str, Any]) -> str:
        """Routes the agent's prediction to the correct tool."""
        prediction = state.prediction
        if prediction:
            action = prediction.action
            if action == "ANSWER":
                return "ANSWER"
            if action in ["Click", "Type", "Scroll", "Wait", "GoBack", "Google"]:
                return action
            if action == "retry":
                return "agent"
        return "agent"

    def update_scratchpad(self, state):
        """Updates the scratchpad with the latest observation and agent's reasoning."""
        debug_print("Updating scratchpad")
        print(
            f"Scratchpad: {state.get('scratchpad') if isinstance(state, dict) else getattr(state, 'scratchpad', [])}"
        )

        # Extract scratchpad
        scratchpad = []
        if isinstance(state, dict):
            scratchpad = state.get("scratchpad", [])
        else:
            scratchpad = getattr(state, "scratchpad", [])

        # Extract observation
        observation = ""
        if isinstance(state, dict):
            observation = state.get("observation", "")
        else:
            observation = getattr(state, "observation", "")

        # Ensure observation is a string
        if isinstance(observation, dict):
            observation = observation.get("message", str(observation))

        # Extract thought from prediction
        thought = None
        prediction = None
        if isinstance(state, dict):
            prediction = state.get("prediction", {})
        else:
            prediction = getattr(state, "prediction", None)

        if prediction:
            if hasattr(prediction, "thought"):
                thought = prediction.thought
            elif isinstance(prediction, dict) and "thought" in prediction:
                thought = prediction["thought"]

        # Format step count
        step = 1
        if scratchpad:
            first_message = scratchpad[0]
            # Check if the message is a dictionary or an object with content attribute
            if isinstance(first_message, dict) and "content" in first_message:
                content = first_message["content"]
            elif hasattr(first_message, "content"):
                content = first_message.content
            else:
                content = str(first_message)

            last_line = content.rsplit("\n", 1)[-1]
            match = re.match(r"\d+", last_line)
            step = int(match.group()) + 1 if match else 1

        # Build new scratchpad text
        if scratchpad:
            # Extract content from the first message
            first_message = scratchpad[0]
            if isinstance(first_message, dict) and "content" in first_message:
                text = first_message["content"]
            elif hasattr(first_message, "content"):
                text = first_message.content
            else:
                text = str(first_message)
        else:
            text = "Previous action observations:\n"

        # Add thought if available
        if thought:
            text += f"\n{step}. Thought: {thought}"
            step += 1

        # Add observation
        text += f"\n{step}. Observation: {observation}"

        # Create new scratchpad message - ensure it's a proper SystemMessage
        new_scratchpad = [SystemMessage(content=text)]

        # Return updated state
        if isinstance(state, dict):
            return {**state, "scratchpad": new_scratchpad, "observation": observation}
        # Create a dictionary with the same fields as the input state
        state_dict = {}
        for field in dir(state):
            if (
                not field.startswith("_")
                and field != "scratchpad"
                and field != "observation"
            ):
                try:
                    state_dict[field] = getattr(state, field)
                except:
                    pass

        return {**state_dict, "scratchpad": new_scratchpad, "observation": observation}

    # -------------------------------------------------------------------------
    # Browser Management Functions
    # -------------------------------------------------------------------------
    async def start_browser(self):
        """Launch the browser and navigate to Google."""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=True,
            # executable_path="/mnt/c/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe",
            args=[
                "--no-sandbox",  # Disable sandboxing for WSL compatibility
                "--disable-setuid-sandbox",  # Further sandbox disable
                "--disable-gpu",  # WSL doesn't support GPU acceleration properly
                # "--disable-dev-shm-usage",  # Avoid crashes due to limited /dev/shm
                "--disable-software-rasterizer",  # Prevent software rendering crashes
                # "--remote-debugging-port=9222",  # Enable remote debugging
                # 3"--disable-background-networking",  # Reduce Brave network calls
                "--disable-default-apps",  # Start with a blank slate
                # "--disable-extensions",  # Ensure no extension interference
                # "--disable-hang-monitor",  # Avoid Playwright thinking Brave has hung
                "--disable-popup-blocking",  # Allow all popups (for automation)
                "--disable-renderer-backgrounding",  # Keep tabs active
                # "--disable-background-timer-throttling",  # Prevent timeouts
                # "--disable-backgrounding-occluded-windows",  # Keep processes alive
                # "--disable-breakpad",  # Disable Brave crash reporting (unnecessary)
                # "--disable-component-extensions-with-background-pages",  # Prevent auto-running extensions
                # "--disable-sync",  # Avoid syncing issues
                # "--disable-ipc-flooding-protection",  # Prevent Playwright issues
                # "--disable-features=site-per-process",  # Prevent multi-process site management
                # "--enable-automation",  # Ensure Playwright isn't blocked
                # "--password-store=basic",  # Avoid Brave password manager interference
                # "--use-mock-keychain",  # Prevent keychain authentication popups
                # "--window-size=1920,1080",  # Set a large window size
                "--ignore-certificate-errors",  # Bypass SSL issues
            ],
            # headless=False  # Show browser window
        )

        self.page = await self.browser.new_page()
        await stealth_async(self.page)
        await self.page.goto("https://www.google.com")

        # Take initial screenshot
        screenshot = await self.capture_screenshot()

        # Initialize state
        self.state = WebNavState(
            page_url=self.page.url, input="", img=screenshot, observation=""
        )

    async def stop_browser(self):
        """Closes the browser instance."""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.page = None

    async def capture_screenshot(self) -> str:
        """Captures a screenshot and returns a base64 string."""
        if not self.page:
            return ""

        try:
            screenshot_bytes = await self.page.screenshot()
            plain_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
            # self.screenshots.append(plain_base64)
            return plain_base64
        except Exception as e:
            logger.error(f"Error capturing screenshot: {e}")
            return ""

    # -------------------------------------------------------------------------
    # Page Annotation and Formatting
    # -------------------------------------------------------------------------
    async def annotate_page(self, state: dict[str, Any]) -> dict[str, Any]:
        """Annotates the page with bounding boxes."""
        # Convert state to dict if needed
        if hasattr(state, "model_dump"):
            state_dict = state.model_dump()
        elif isinstance(state, dict):
            state_dict = state
        else:
            try:
                state_dict = dict(state)
            except:
                state_dict = {"input": getattr(state, "input", "")}

        # Check if page is available
        if not self.page:
            logger.error("Page not initialized")
            return {
                **state_dict,
                "bboxes": [],
                "img": state_dict.get("img", ""),
                "observation": "Error: Browser page not available",
            }

        try:
            # Run the mark page script
            await self.page.evaluate(self.mark_page_script)

            # Try to get bounding boxes with retry
            bboxes = []
            try:
                bboxes = await self.page.evaluate("markPage()")
            except Exception as e:
                logger.warning(f"Error getting bboxes: {e}")
                # If we can't get bboxes, don't fail completely

            # Process bounding boxes to ensure they have all required fields
            processed_bboxes = []
            for bbox in bboxes:
                # Ensure all required fields are present
                processed_bbox = {
                    "x": bbox.get("x", 0),
                    "y": bbox.get("y", 0),
                    "width": bbox.get("width", 10),  # Default width if missing
                    "height": bbox.get("height", 10),  # Default height if missing
                    "text": bbox.get("text", ""),
                    "type": bbox.get("type", "element"),
                    "ariaLabel": bbox.get("ariaLabel", ""),
                }
                processed_bboxes.append(processed_bbox)

            # Take screenshot
            screenshot = await self.capture_screenshot()

            # Clean up annotations
            try:
                await self.page.evaluate("unmarkPage()")
            except Exception as e:
                logger.warning(f"Error clearing annotations: {e}")

            # Return state with annotations
            return {
                **state_dict,
                "img": screenshot,
                "bboxes": processed_bboxes,
                "page_url": self.page.url,
            }

        except Exception as e:
            logger.error(f"Error in annotate_page: {e}")

            # Try to get a screenshot even if annotation failed
            screenshot = ""
            try:
                screenshot = await self.capture_screenshot()
            except:
                pass

            # Return state with whatever we have
            return {
                **state_dict,
                "img": screenshot or state_dict.get("img", ""),
                "bboxes": state_dict.get("bboxes", []),
                "observation": f"Error during page annotation: {e!s}",
                "page_url": (
                    self.page.url if self.page else state_dict.get("page_url", "")
                ),
            }

    def format_descriptions(self, state: dict[str, Any]) -> str:
        """Formats bounding boxes into readable descriptions."""
        bboxes = state.get("bboxes", [])
        labels = []

        for i, bbox in enumerate(bboxes):
            text = bbox.get("ariaLabel") or bbox.get("text", "")
            el_type = bbox.get("type", "")
            labels.append(f'{i} (<{el_type}/>): "{text}"')

        return "\nValid Bounding Boxes:\n" + "\n".join(labels)

    def parse_prediction(self, text: str) -> dict[str, Any]:
        """Parses LLM output into a structured prediction."""
        # Find the action line
        action_prefix = "Action: "
        action_line = None
        thought_lines = []

        for line in text.strip().split("\n"):
            if line.startswith(action_prefix):
                action_line = line
                break
            thought_lines.append(line)

        # If no action found, return retry
        if not action_line:
            return {
                "thought": "\n".join(thought_lines),
                "action": "retry",
                "args": ["Could not parse LLM Output"],
            }

        # Extract action and args
        thought = "\n".join(thought_lines)
        action_str = action_line[len(action_prefix) :].strip()
        split_output = action_str.split(" ", 1)

        if len(split_output) == 1:
            action, action_input = split_output[0], []
        else:
            action, action_input_str = split_output
            action_input = [
                inp.strip().strip("[]") for inp in action_input_str.strip().split(";")
            ]

        return {"thought": thought, "action": action.strip(), "args": action_input}

    # -------------------------------------------------------------------------
    # Integrated Tool Functions (Avoids Serialization Issues)
    # -------------------------------------------------------------------------
    async def tool_click(self, state: dict[str, Any]) -> str:
        """Clicks on an element identified by its bounding box index."""
        if not self.page:
            return "No live page available."

        prediction = state.prediction
        args = prediction.args

        if not args or len(args) < 1:
            return "Invalid click arguments. Need bbox index."

        try:
            bbox_id = int(args[0])
            bboxes = state.bboxes

            if bbox_id >= len(bboxes):
                return f"Invalid bounding box ID: {bbox_id} (out of range)"

            bbox = bboxes[bbox_id]
            x, y = bbox.x, bbox.y

            # Execute click
            await self.page.mouse.click(x, y)
            await self.page.wait_for_load_state("networkidle")
            return f"Clicked element {bbox_id} at ({x}, {y})"

        except (ValueError, IndexError, KeyError) as e:
            logger.error(f"Error clicking element: {e}")
            return f"Error clicking element: {e}"

    async def tool_type(self, state: dict[str, Any]) -> str:
        """Types text into an identified bounding box."""
        if not self.page:
            return "No live page available."

        try:
            # Get prediction
            prediction = None
            if hasattr(state, "prediction"):
                prediction = state.prediction
            elif isinstance(state, dict):
                prediction = state.get("prediction", {})

            # Get args
            args = []
            if prediction:
                if hasattr(prediction, "args"):
                    args = prediction.args
                elif isinstance(prediction, dict):
                    args = prediction.get("args", [])

            if not args or len(args) < 2:
                return "Invalid type arguments. Need bbox index and text."

            # Get bboxes
            bboxes = []
            if hasattr(state, "bboxes"):
                bboxes = state.bboxes
            elif isinstance(state, dict):
                bboxes = state.get("bboxes", [])

            try:
                bbox_id = int(args[0])
                text_content = args[1]

                if bbox_id >= len(bboxes):
                    return f"Invalid bounding box ID: {bbox_id} (out of range)"

                bbox = bboxes[bbox_id]

                # Use proper attribute access for BBox object
                # Access x and y properly whether bbox is a dict or a BBox object
                if hasattr(bbox, "x") and hasattr(bbox, "y"):
                    x, y = bbox.x, bbox.y
                elif isinstance(bbox, dict):
                    x, y = bbox.get("x", 0), bbox.get("y", 0)
                else:
                    return f"Cannot extract coordinates from bbox type: {type(bbox)}"

                # Click on element
                await self.page.mouse.click(x, y)

                # Select all existing text
                select_all = "Meta+A" if platform.system() == "Darwin" else "Control+A"
                await self.page.keyboard.press(select_all)
                await self.page.keyboard.press("Backspace")

                # Type new text
                await self.page.keyboard.type(text_content)
                await self.page.keyboard.press("Enter")

                # Wait for navigation to complete
                try:
                    await self.page.wait_for_load_state("networkidle", timeout=30000)
                except Exception as e:
                    logger.warning(f"Navigation timeout after typing: {e}")

                return f"Typed '{text_content}' in element {bbox_id}"

            except (ValueError, IndexError, KeyError) as e:
                logger.error(f"Error typing text: {e}")
                return f"Error typing text: {e}"
        except Exception as e:
            logger.error(f"Unexpected error in tool_type: {e}")
            return f"Unexpected error in tool_type: {e!s}"

    async def tool_scroll(self, state: dict[str, Any]) -> str:
        """Scrolls either the window or a specific element."""
        if not self.page:
            return "No live page available."

        prediction = state.prediction
        args = prediction.args

        if not args or len(args) < 2:
            return "Invalid scroll arguments. Need target and direction."

        target, direction = args
        scroll_amount = 500 if target.upper() == "WINDOW" else 200
        scroll_direction = (
            -scroll_amount if direction.lower() == "up" else scroll_amount
        )

        try:
            if target.upper() == "WINDOW":
                await self.page.evaluate(f"window.scrollBy(0, {scroll_direction})")
                return f"Scrolled window {direction}"
            target_id = int(target)
            bboxes = state.bboxes

            if target_id >= len(bboxes):
                return f"Invalid bounding box ID: {target_id} (out of range)"

            bbox = bboxes[target_id]
            x, y = bbox.x, bbox.y

            await self.page.mouse.move(x, y)
            await self.page.mouse.wheel(0, scroll_direction)
            return f"Scrolled element {target_id} {direction}"

        except Exception as e:
            logger.error(f"Error scrolling: {e}")
            return f"Error scrolling: {e}"

    async def tool_wait(self, state: dict[str, Any]) -> str:
        """Waits for a fixed period (3s)."""
        sleep_time = 3
        await asyncio.sleep(sleep_time)
        return f"Waited for {sleep_time} seconds"

    async def tool_go_back(self, state: dict[str, Any]) -> str:
        """Navigates back in browser history."""
        if not self.page:
            return "No live page available."

        try:
            await self.page.go_back()
            await self.page.wait_for_load_state("networkidle")
            return f"Navigated back to {self.page.url}"
        except Exception as e:
            logger.error(f"Error navigating back: {e}")
            return f"Error navigating back: {e}"

    async def tool_to_google(self, state: dict[str, Any]) -> str:
        """Navigates to Google homepage."""
        if not self.page:
            return "No live page available."

        try:
            await self.page.goto("https://www.google.com/")
            await self.page.wait_for_load_state("networkidle")
            return "Navigated to Google homepage"
        except Exception as e:
            logger.error(f"Error navigating to Google: {e}")
            return f"Error navigating to Google: {e}"

    async def tool_answer(self, state: dict[str, Any]) -> str:
        """Returns final answer to user query."""
        prediction = state.prediction
        args = prediction.args

        if not args or len(args) < 1:
            return "No answer provided."

        return f"FINAL ANSWER: {args[0]}"

    # -------------------------------------------------------------------------
    # Public API Methods
    # -------------------------------------------------------------------------
    async def run(self, question: str, show_images: bool = False) -> str | None:
        """Run the agent on a given question and return the final answer."""
        # Start browser if needed
        if not self.page:
            await self.start_browser()

        # Prepare input state
        input_state = {
            "page_url": self.page.url,
            "input": question,
            "observation": "",
            "scratchpad": [],
        }

        # Set runtime config
        runtime_config = {
            "configurable": {
                "thread_id": str(uuid.uuid4()),
                "recursion_limit": self.max_steps,
            }
        }

        # Run agent
        final_answer = None
        steps = []

        # Stream results
        event_stream = self.app.astream(input_state, config=runtime_config, debug=True)

        async for event in event_stream:
            prediction = event.get("prediction", {})
            observation = event.get("observation", "")
            action = prediction.get("action", "") if prediction else ""

            # Display progress
            display.clear_output(wait=True)
            step_str = f"{len(steps)+1}. {action}"
            if prediction and "args" in prediction:
                step_str += f": {prediction['args']}"
            steps.append(step_str)
            print("\n".join(steps))
            print(f"Latest observation: {observation}")

            # Show screenshot only if show_images is True
            if show_images and "img" in event and event["img"]:
                display.display(display.Image(base64.b64decode(event["img"])))

            # Check for answer
            if action == "ANSWER" and prediction and prediction.get("args"):
                final_answer = prediction["args"][0]
                break

        return final_answer

    async def close(self):
        """Clean up resources."""
        await self.stop_browser()


# Example usage
async def run_web_navigator():
    # Import web_nav_aug_llm from your module
    from agents.web_nav.aug_llms import web_nav_aug_llm

    config = WebNavAgentConfig(
        aug_llm_config=web_nav_aug_llm,
        headless=False,
        max_steps=5,
    )

    agent = WebNavAgent(config)

    try:
        result = await agent.run(
            "How far is Toronto Pearson airport from 1289 Queen Street West, Toronto?"
        )
        print(f"Final answer: {result}")
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(run_web_navigator())
