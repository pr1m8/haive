import time
from typing import Any

from langgraph.types import RetryPolicy
from pydantic import BaseModel, Field


class RetryPolicy(BaseModel):
    """Base retry policy for tools and structured output."""

    max_retries: int = Field(default=3, description="Maximum number of retry attempts")
    delay: float = Field(default=0, description="Delay in seconds between retries")
    errors_to_retry: list[str] = Field(
        default_factory=lambda: ["Exception"],
        description="Names of exception types to retry on",
    )

    def should_retry(self, attempt: int, error: Exception | None = None) -> bool:
        """Determine if a retry should be attempted."""
        # Check attempt count
        if attempt >= self.max_retries:
            return False

        # If no error specified, allow retry
        if error is None:
            return True

        # Check if error type is in allowed list
        error_type = error.__class__.__name__
        return error_type in self.errors_to_retry

    def get_delay(self, attempt: int) -> float:
        """Get the delay before the next retry."""
        return self.delay


class ExponentialBackoffRetry(RetryPolicy):
    """Retry policy with exponential backoff."""

    base_delay: float = Field(default=1.0, description="Base delay in seconds")
    max_delay: float = Field(default=60.0, description="Maximum delay in seconds")
    backoff_factor: float = Field(default=2.0, description="Multiplier for each retry")

    def get_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay."""
        delay = self.base_delay * (self.backoff_factor ** (attempt - 1))
        return min(delay, self.max_delay)


class LinearBackoffRetry(RetryPolicy):
    """Retry policy with linear backoff."""

    base_delay: float = Field(default=1.0, description="Base delay in seconds")
    increment: float = Field(default=1.0, description="Increment for each retry")

    def get_delay(self, attempt: int) -> float:
        """Calculate linear backoff delay."""
        return self.base_delay + (self.increment * (attempt - 1))


def execute_with_retry(
    func: callable,
    *args,
    retry_policy: RetryPolicy | None = None,
    fallback_result: Any | None = None,
    **kwargs
) -> Any:
    """Execute a function with retry logic.

    Args:
        func: Function to execute
        *args: Positional arguments for the function
        retry_policy: Retry policy to use
        fallback_result: Result to return if all retries fail
        **kwargs: Keyword arguments for the function

    Returns:
        Result of the function or fallback result
    """
    # Use default retry policy if none provided
    policy = retry_policy or RetryPolicy()

    attempt = 0
    last_error = None

    while attempt < policy.max_retries:
        try:
            # Attempt execution
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            attempt += 1

            # Check if we should retry
            if not policy.should_retry(attempt, e):
                break

            # Apply delay if not the last attempt
            if attempt < policy.max_retries:
                delay = policy.get_delay(attempt)
                if delay > 0:
                    time.sleep(delay)

    # All retries failed, return fallback or raise last error
    if fallback_result is not None:
        return fallback_result
    raise last_error


async def execute_with_retry_async(
    func: callable,
    *args,
    retry_policy: RetryPolicy | None = None,
    fallback_result: Any | None = None,
    **kwargs
) -> Any:
    """Execute an async function with retry logic.

    Args:
        func: Async function to execute
        *args: Positional arguments for the function
        retry_policy: Retry policy to use
        fallback_result: Result to return if all retries fail
        **kwargs: Keyword arguments for the function

    Returns:
        Result of the function or fallback result
    """
    import asyncio

    # Use default retry policy if none provided
    policy = retry_policy or RetryPolicy()

    attempt = 0
    last_error = None

    while attempt < policy.max_retries:
        try:
            # Attempt execution
            return await func(*args, **kwargs)
        except Exception as e:
            last_error = e
            attempt += 1

            # Check if we should retry
            if not policy.should_retry(attempt, e):
                break

            # Apply delay if not the last attempt
            if attempt < policy.max_retries:
                delay = policy.get_delay(attempt)
                if delay > 0:
                    await asyncio.sleep(delay)

    # All retries failed, return fallback or raise last error
    if fallback_result is not None:
        return fallback_result
    raise last_error


# Helper functions
def create_retry_policy(
    max_retries: int = 3, delay: float = 0, errors_to_retry: list[str] | None = None
) -> RetryPolicy:
    """Create a basic retry policy."""
    return RetryPolicy(
        max_retries=max_retries,
        delay=delay,
        errors_to_retry=errors_to_retry or ["Exception"],
    )


def create_exponential_backoff_policy(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    errors_to_retry: list[str] | None = None,
) -> ExponentialBackoffRetry:
    """Create an exponential backoff retry policy."""
    return ExponentialBackoffRetry(
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
        backoff_factor=backoff_factor,
        errors_to_retry=errors_to_retry or ["Exception"],
    )


def create_linear_backoff_policy(
    max_retries: int = 3,
    base_delay: float = 1.0,
    increment: float = 1.0,
    errors_to_retry: list[str] | None = None,
) -> LinearBackoffRetry:
    """Create a linear backoff retry policy."""
    return LinearBackoffRetry(
        max_retries=max_retries,
        base_delay=base_delay,
        increment=increment,
        errors_to_retry=errors_to_retry or ["Exception"],
    )
