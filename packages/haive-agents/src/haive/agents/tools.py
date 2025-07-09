import asyncio
import logging
import platform
from typing import Any

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def click(state: dict[str, Any]) -> dict[str, Any]:
    """Clicks on an element identified by its bounding box index."""
    # Access page through the property
    page = getattr(state, "_page", None) or state.get("page")
    if not page:
        logger.error("No live page available for click action")
        return {"message": "No live page available."}

    # Access prediction through the property or dict
    prediction = state.get("prediction")
    if hasattr(state, "prediction"):
        prediction = state.prediction

    click_args = prediction.args if prediction else None
    if not click_args or len(click_args) != 1:
        logger.error(f"Invalid click arguments: {click_args}")
        return {"message": f"Invalid click arguments: {click_args}"}

    try:
        bbox_id = int(click_args[0])
        # Access bboxes through property or dict
        bboxes = state.get("bboxes", [])
        if hasattr(state, "bboxes"):
            bboxes = state.bboxes

        if bbox_id >= len(bboxes):
            return {"message": f"Invalid bounding box ID: {bbox_id} (out of range)"}

        bbox = bboxes[bbox_id]
        x, y = bbox["x"], bbox["y"]
        logger.debug(f"Clicking at coordinates: ({x}, {y})")
    except (ValueError, IndexError, KeyError) as e:
        logger.error(f"Error processing bbox: {e}")
        return {"message": f"Error processing bbox: {e}"}

    await page.mouse.click(x, y)
    page_url = page.url
    logger.debug(f"Clicked element {bbox_id} on page {page_url}")
    return {"message": f"Clicked element {bbox_id}", "page_url": page_url}


async def type_text(state: dict[str, Any]) -> dict[str, Any]:
    """Types text into an identified bounding box."""
    # Access page through the property
    state = state.model_dump()
    page = getattr(state, "_page", None) or state.get("page")
    if not page:
        logger.error("No live page available for type_text action")
        return {"message": "No live page available."}

    # Access prediction through the property or dict
    prediction = state.get("prediction")
    if hasattr(state, "prediction"):
        prediction = state.prediction

    type_args = prediction.args if prediction else None
    if not type_args or len(type_args) != 2:
        logger.error(f"Invalid type arguments: {type_args}")
        return {"message": f"Invalid type arguments: {type_args}"}

    try:
        bbox_id = int(type_args[0])
        text_content = type_args[1]

        # Access bboxes through property or dict
        bboxes = state.get("bboxes", [])
        if hasattr(state, "bboxes"):
            bboxes = state.bboxes

        if bbox_id >= len(bboxes):
            return {"message": f"Invalid bounding box ID: {bbox_id} (out of range)"}

        bbox = bboxes[bbox_id]
        x, y = bbox["x"], bbox["y"]
        logger.debug(f"Typing at coordinates: ({x}, {y})")
    except (ValueError, IndexError, KeyError) as e:
        logger.error(f"Error processing bbox for typing: {e}")
        return {"message": f"Error processing bbox for typing: {e}"}

    await page.mouse.click(x, y)
    select_all = "Meta+A" if platform.system() == "Darwin" else "Control+A"
    await page.keyboard.press(select_all)
    await page.keyboard.press("Backspace")
    await page.keyboard.type(text_content)
    await page.keyboard.press("Enter")
    page_url = page.url
    logger.debug(f"Typed '{text_content}' in element {bbox_id} on page {page_url}")
    return {
        "message": f"Typed '{text_content}' in element {bbox_id}",
        "page_url": page_url,
    }


async def scroll(state: dict[str, Any]) -> dict[str, Any]:
    """Scrolls either the window or a specific element."""
    # Access page through the property
    page = getattr(state, "_page", None) or state.get("page")
    if not page:
        logger.error("No live page available for scroll action")
        return {"message": "No live page available."}

    # Access prediction through the property or dict
    prediction = state.get("prediction")
    if hasattr(state, "prediction"):
        prediction = state.prediction

    scroll_args = prediction.args if prediction else None
    if not scroll_args or len(scroll_args) != 2:
        logger.error("Invalid scroll arguments.")
        return {"message": "Invalid scroll arguments."}

    target, direction = scroll_args
    scroll_amount = 500 if target.upper() == "WINDOW" else 200
    scroll_direction = -scroll_amount if direction.lower() == "up" else scroll_amount

    try:
        if target.upper() == "WINDOW":
            await page.evaluate(f"window.scrollBy(0, {scroll_direction})")
            logger.debug(f"Scrolled window {direction}")
        else:
            target_id = int(target)
            # Access bboxes through property or dict
            bboxes = state.get("bboxes", [])
            if hasattr(state, "bboxes"):
                bboxes = state.bboxes

            if target_id >= len(bboxes):
                return {
                    "message": f"Invalid bounding box ID: {target_id} (out of range)"
                }

            bbox = bboxes[target_id]
            x, y = bbox["x"], bbox["y"]
            await page.mouse.move(x, y)
            await page.mouse.wheel(0, scroll_direction)
            logger.debug(f"Scrolled element {target_id} {direction}")
    except Exception as e:
        logger.error(f"Failed to scroll: {e!s}")
        return {"message": f"Failed to scroll: {e!s}"}

    page_url = page.url
    return {
        "message": f"Scrolled {direction} in {'window' if target.upper() == 'WINDOW' else 'element'}",
        "page_url": page_url,
    }


async def wait(state: dict[str, Any]) -> dict[str, Any]:
    """Waits for a fixed period (5s)."""
    sleep_time = 5
    logger.debug(f"Waiting for {sleep_time}s")
    await asyncio.sleep(sleep_time)

    # Get page URL if available
    page_url = None
    page = getattr(state, "_page", None) or state.get("page")
    if page:
        page_url = page.url

    return {"message": f"Waited for {sleep_time}s.", "page_url": page_url}


async def go_back(state: dict[str, Any]) -> dict[str, Any]:
    """Navigates back in browser history."""
    # Access page through the property
    page = getattr(state, "_page", None) or state.get("page")
    if not page:
        logger.error("No live page available for go_back action")
        return {"message": "No live page available."}

    logger.debug("Navigating back in browser history")
    await page.go_back()
    page_url = page.url
    return {"message": f"Navigated back to {page_url}", "page_url": page_url}


async def to_google(state: dict[str, Any]) -> dict[str, Any]:
    """Navigates to Google homepage."""
    # Access page through the property
    page = getattr(state, "_page", None) or state.get("page")
    if not page:
        logger.error("No live page available for to_google action")
        return {"message": "No live page available."}

    logger.debug("Navigating to Google homepage")
    await page.goto("https://www.google.com/")
    # Wait for navigation to complete
    await page.wait_for_load_state("networkidle")
    logger.debug("Google homepage loaded")
    return {
        "message": "Navigated to google.com.",
        "page_url": "https://www.google.com/",
    }
