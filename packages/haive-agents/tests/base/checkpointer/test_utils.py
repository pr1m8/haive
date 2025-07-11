"""Utilities for testing agents with controllable responses."""

from typing import Any

from langchain_core.runnables import RunnableConfig


class MockLLM:
    """A mock LLM that returns predefined responses for testing."""

    def __init__(
        self,
        responses: list[str] | None = None,
        response_map: dict[str, str] | None = None,
        default_response: str = "This is a test response from MockLLM.",
    ):
        """Initialize the MockLLM.

        Args:
            responses: A list of responses to return in sequence
            response_map: A mapping of input text fragments to responses
            default_response: The default response if no specific response is found
        """
        self.responses = responses or []
        self.response_map = response_map or {}
        self.default_response = default_response
        self.response_index = 0
        self.invoke_count = 0
        self.inputs = []

    def invoke(
        self,
        input_data: str | dict[str, Any],
        config: RunnableConfig | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """Mock invoke method."""
        self.invoke_count += 1
        self.inputs.append(input_data)

        # Process the input to extract the essential text for matching
        input_text = self._extract_text(input_data)

        # Get the appropriate response
        response_text = self._get_response(input_text)

        # Format as an agent response
        return {"messages": [{"role": "assistant", "content": response_text}]}

    async def ainvoke(
        self,
        input_data: str | dict[str, Any],
        config: RunnableConfig | None = None,
        **kwargs
    ) -> dict[str, Any]:
        """Async version of invoke."""
        return self.invoke(input_data, config, **kwargs)

    def stream(
        self,
        input_data: str | dict[str, Any],
        config: RunnableConfig | None = None,
        **kwargs
    ):
        """Stream responses."""
        self.invoke_count += 1
        self.inputs.append(input_data)

        # Process the input to extract the essential text for matching
        input_text = self._extract_text(input_data)

        # Get the appropriate response
        response_text = self._get_response(input_text)

        # Split the response into chunks for streaming
        chunks = self._split_into_chunks(response_text)

        # Yield each chunk
        for chunk in chunks:
            yield {"messages": [{"role": "assistant", "content": chunk}]}

    async def astream(
        self,
        input_data: str | dict[str, Any],
        config: RunnableConfig | None = None,
        **kwargs
    ):
        """Async version of stream."""
        for chunk in self.stream(input_data, config, **kwargs):
            yield chunk

    def _extract_text(self, input_data: str | dict[str, Any]) -> str:
        """Extract the text from various input formats."""
        if isinstance(input_data, str):
            return input_data

        if isinstance(input_data, dict):
            # Try to extract from messages
            if input_data.get("messages"):
                messages = input_data["messages"]
                if isinstance(messages, list) and len(messages) > 0:
                    # Get the last message content
                    last_message = messages[-1]
                    if hasattr(last_message, "content"):
                        return last_message.content
                    if isinstance(last_message, dict) and "content" in last_message:
                        return last_message["content"]

            # Try direct input field
            if "input" in input_data:
                return str(input_data["input"])

        # Fallback - convert to string
        return str(input_data)

    def _get_response(self, input_text: str) -> str:
        """Get the appropriate response based on input."""
        # Check if we have a sequential response to return
        if self.responses and self.response_index < len(self.responses):
            response = self.responses[self.response_index]
            self.response_index += 1
            return response

        # Check if the input matches any patterns in the response map
        for pattern, response in self.response_map.items():
            if pattern.lower() in input_text.lower():
                return response

        # Return default response
        return self.default_response

    def _split_into_chunks(self, text: str, num_chunks: int = 3) -> list[str]:
        """Split a response into chunks for streaming simulation."""
        if not text:
            return [""]

        chunk_size = max(1, len(text) // num_chunks)
        chunks = []

        for i in range(0, len(text), chunk_size):
            chunks.append(text[i : i + chunk_size])

        return chunks or [""]


class MockEngineBuilder:
    """Helper to build mock engine configurations for testing."""

    @staticmethod
    def create_mock_llm_config(
        responses: list[str] | None = None,
        response_map: dict[str, str] | None = None,
        default_response: str = "This is a test response.",
        system_message: str = "You are a test assistant.",
    ):
        """Create a configuration for a mock LLM.

        Args:
            responses: Sequential responses
            response_map: Mapping of input patterns to responses
            default_response: Default response if no match
            system_message: System message for the LLM

        Returns:
            A dict with the mock LLM configuration
        """
        from haive.core.engine.aug_llm import AugLLMConfig

        # Create the mock LLM
        mock_llm = MockLLM(
            responses=responses,
            response_map=response_map,
            default_response=default_response,
        )

        # Create an AugLLMConfig that will use our mock
        config = AugLLMConfig(system_message=system_message)

        # Instead of trying to modify the config object directly,
        # we'll monkey patch the correct method at the test level
        return config, mock_llm

    @staticmethod
    def patch_create_runnable(config, mock_llm):
        """Patches the create_runnable method for the given test.

        Args:
            config: The AugLLMConfig to patch
            mock_llm: The MockLLM to return

        Returns:
            A mock.patch context manager
        """
        from unittest import mock

        # Create a patch that replaces create_runnable with a function returning our mock
        return mock.patch.object(
            config.__class__, "create_runnable", return_value=mock_llm
        )
