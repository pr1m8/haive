"""
Rate limiting mixin for LLM configurations.

This module provides a mixin class that adds rate limiting capabilities to LLM configurations,
allowing for controlled request rates to prevent API throttling and manage costs.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class RateLimitingMixin:
    """
    Mixin class that adds rate limiting configuration to LLM models.

    This mixin provides configuration for rate limiting when calling LLM APIs,
    including request limits, token limits, and time windows. It integrates with
    LangChain's ChatRateLimiter for actual enforcement.

    Attributes:
        requests_per_second: Maximum number of requests per second
        tokens_per_second: Maximum number of tokens per second (if supported)
        tokens_per_minute: Maximum number of tokens per minute (if supported)
        max_retries: Maximum number of retries for rate-limited requests
        retry_delay: Base delay between retries in seconds
        check_every_n_seconds: How often to check rate limits
        burst_size: Maximum burst size for rate limiting
    """

    # These attributes are expected to be defined in the class using this mixin
    # They will be added via Pydantic Field definitions in the concrete class
    requests_per_second: Optional[float]
    tokens_per_second: Optional[int]
    tokens_per_minute: Optional[int]
    max_retries: int
    retry_delay: float
    check_every_n_seconds: Optional[float]
    burst_size: Optional[int]

    def apply_rate_limiting(self, llm: Any) -> Any:
        """
        Apply rate limiting to an LLM instance.

        Args:
            llm: The LLM instance to apply rate limiting to

        Returns:
            The LLM instance wrapped with rate limiting, or original if rate limiting not configured
        """
        # Check if any rate limiting is configured
        if not any(
            [self.requests_per_second, self.tokens_per_second, self.tokens_per_minute]
        ):
            logger.debug("No rate limiting configured, returning original LLM")
            return llm

        try:
            from langchain_core.rate_limiters import InMemoryRateLimiter
            from langchain_core.runnables import RunnableWithMessageHistory

            # Build rate limiter configuration
            rate_limiter_config = {}

            if self.requests_per_second is not None:
                rate_limiter_config["requests_per_second"] = self.requests_per_second

            if self.tokens_per_second is not None:
                rate_limiter_config["tokens_per_second"] = self.tokens_per_second

            if self.tokens_per_minute is not None:
                rate_limiter_config["tokens_per_minute"] = self.tokens_per_minute

            if self.check_every_n_seconds is not None:
                rate_limiter_config["check_every_n_seconds"] = (
                    self.check_every_n_seconds
                )

            if self.burst_size is not None:
                rate_limiter_config["burst_size"] = self.burst_size

            # Create rate limiter
            rate_limiter = InMemoryRateLimiter(**rate_limiter_config)

            # Apply rate limiting to the LLM
            # If the LLM supports with_rate_limiter method, use it
            if hasattr(llm, "with_rate_limiter"):
                logger.debug(
                    f"Applying rate limiting with config: {rate_limiter_config}"
                )
                return llm.with_rate_limiter(rate_limiter)
            else:
                # Otherwise, wrap it manually
                logger.warning(
                    f"LLM {type(llm).__name__} does not support with_rate_limiter method. "
                    "Rate limiting may not work as expected."
                )
                return llm

        except ImportError as e:
            logger.warning(
                f"Failed to import rate limiting dependencies: {e}. "
                "Ensure langchain-core>=0.3.0 is installed."
            )
            return llm
        except Exception as e:
            logger.error(f"Failed to apply rate limiting: {e}")
            return llm

    def get_rate_limit_info(self) -> dict:
        """
        Get a dictionary of rate limiting configuration for debugging.

        Returns:
            Dictionary containing rate limiting configuration
        """
        return {
            "requests_per_second": self.requests_per_second,
            "tokens_per_second": self.tokens_per_second,
            "tokens_per_minute": self.tokens_per_minute,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay,
            "check_every_n_seconds": self.check_every_n_seconds,
            "burst_size": self.burst_size,
            "enabled": any(
                [
                    self.requests_per_second,
                    self.tokens_per_second,
                    self.tokens_per_minute,
                ]
            ),
        }
