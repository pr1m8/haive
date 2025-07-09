from langchain_core.runnables import RunnableConfig


def get_user_id(config: RunnableConfig) -> str:
    user_id = config["configurable"].get("user_id", None)
    if user_id is None:
        raise ValueError("User ID needs to be provided to save a memory.")

    return user_id
