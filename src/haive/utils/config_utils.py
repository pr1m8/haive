from langchain_core.runnables import RunnableConfig
import uuid
def get_user_id(config: RunnableConfig) -> str:
    """
    Get the user ID from the config.
    
    Args:
        config (RunnableConfig): The config to get the user ID from.
        
    Returns:
        str: The user ID.
    """
    user_id = config["configurable"].get("user_id")
    if user_id is None:
        raise ValueError("User ID needs to be provided to save a memory.")

    return user_id