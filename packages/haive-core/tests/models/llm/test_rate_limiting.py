"""Tests for rate limiting mixin functionality.

This module tests the rate limiting mixin including:
- Rate limiter configuration
- Application to LLM instances
- Error handling
"""

from typing import Optional
from unittest.mock import Mock, patch

import pytest
from pydantic import BaseModel, Field

from haive.core.models.llm.rate_limiting_mixin import RateLimitingMixin


def create_rate_limited_class():
    """Create a test class with rate limiting mixin."""

    class TestClass(RateLimitingMixin, BaseModel):
        # Add the rate limiting fields with validation
        requests_per_second: Optional[float] = Field(default=None, ge=0)
        tokens_per_second: Optional[int] = Field(default=None, ge=0)
        tokens_per_minute: Optional[int] = Field(default=None, ge=0)
        max_retries: int = Field(default=3, ge=0)
        retry_delay: float = Field(default=1.0, ge=0)
        check_every_n_seconds: Optional[float] = Field(default=None, ge=0)
        burst_size: Optional[int] = Field(default=None, ge=1)

    return TestClass


class TestRateLimitingMixin:
    """Test RateLimitingMixin functionality."""

    def test_default_values(self):
        """Test default rate limiting values."""
        TestClass = create_rate_limited_class()
        obj = TestClass()

        assert obj.requests_per_second is None
        assert obj.tokens_per_second is None
        assert obj.tokens_per_minute is None
        assert obj.max_retries == 3
        assert obj.retry_delay == 1.0
        assert obj.check_every_n_seconds is None
        assert obj.burst_size is None

    def test_custom_values(self):
        """Test setting custom rate limiting values."""
        TestClass = create_rate_limited_class()

        obj = TestClass(
            requests_per_second=10.5,
            tokens_per_second=1000,
            tokens_per_minute=60000,
            max_retries=5,
            retry_delay=2.5,
            check_every_n_seconds=0.5,
            burst_size=20,
        )

        assert obj.requests_per_second == 10.5
        assert obj.tokens_per_second == 1000
        assert obj.tokens_per_minute == 60000
        assert obj.max_retries == 5
        assert obj.retry_delay == 2.5
        assert obj.check_every_n_seconds == 0.5
        assert obj.burst_size == 20

    def test_apply_rate_limiting_no_limits(self):
        """Test apply_rate_limiting when no limits are set."""
        TestClass = create_rate_limited_class()

        obj = TestClass()
        mock_llm = Mock()

        result = obj.apply_rate_limiting(mock_llm)

        # Should return original LLM
        assert result == mock_llm

    @patch("langchain_core.rate_limiters.InMemoryRateLimiter")
    def test_apply_rate_limiting_with_limits(self, mock_rate_limiter_class):
        """Test apply_rate_limiting with rate limits configured."""
        TestClass = create_rate_limited_class()

        obj = TestClass(requests_per_second=10, tokens_per_minute=100000)

        # Mock LLM with with_rate_limiter method
        mock_llm = Mock()
        mock_llm.with_rate_limiter = Mock(return_value="rate_limited_llm")

        # Mock rate limiter
        mock_rate_limiter = Mock()
        mock_rate_limiter_class.return_value = mock_rate_limiter

        result = obj.apply_rate_limiting(mock_llm)

        # Should create rate limiter with correct config
        mock_rate_limiter_class.assert_called_once_with(
            requests_per_second=10, tokens_per_minute=100000
        )

        # Should apply rate limiter to LLM
        mock_llm.with_rate_limiter.assert_called_once_with(mock_rate_limiter)
        assert result == "rate_limited_llm"

    @patch("langchain_core.rate_limiters.InMemoryRateLimiter")
    def test_apply_rate_limiting_all_params(self, mock_rate_limiter_class):
        """Test apply_rate_limiting with all parameters."""
        TestClass = create_rate_limited_class()

        obj = TestClass(
            requests_per_second=5,
            tokens_per_second=1000,
            tokens_per_minute=50000,
            check_every_n_seconds=0.1,
            burst_size=10,
        )

        mock_llm = Mock()
        mock_llm.with_rate_limiter = Mock(return_value="rate_limited_llm")
        mock_rate_limiter = Mock()
        mock_rate_limiter_class.return_value = mock_rate_limiter

        result = obj.apply_rate_limiting(mock_llm)

        # Should pass all params to rate limiter
        mock_rate_limiter_class.assert_called_once_with(
            requests_per_second=5,
            tokens_per_second=1000,
            tokens_per_minute=50000,
            check_every_n_seconds=0.1,
            burst_size=10,
        )

    def test_apply_rate_limiting_llm_without_support(self):
        """Test apply_rate_limiting when LLM doesn't support rate limiting."""
        TestClass = create_rate_limited_class()

        obj = TestClass(requests_per_second=10)

        # Mock LLM without with_rate_limiter method
        mock_llm = Mock(spec=[])  # No methods

        with patch("langchain_core.rate_limiters.InMemoryRateLimiter"):
            result = obj.apply_rate_limiting(mock_llm)

        # Should return original LLM and log warning
        assert result == mock_llm

    def test_apply_rate_limiting_import_error(self):
        """Test apply_rate_limiting when dependencies missing."""
        TestClass = create_rate_limited_class()

        obj = TestClass(requests_per_second=10)
        mock_llm = Mock()

        # Mock import error
        with patch(
            "langchain_core.rate_limiters.InMemoryRateLimiter",
            side_effect=ImportError("langchain-core not installed"),
        ):
            result = obj.apply_rate_limiting(mock_llm)

        # Should return original LLM
        assert result == mock_llm

    def test_apply_rate_limiting_general_error(self):
        """Test apply_rate_limiting with general error."""
        TestClass = create_rate_limited_class()

        obj = TestClass(requests_per_second=10)
        mock_llm = Mock()

        # Mock general error
        with patch(
            "langchain_core.rate_limiters.InMemoryRateLimiter",
            side_effect=Exception("Unexpected error"),
        ):
            result = obj.apply_rate_limiting(mock_llm)

        # Should return original LLM
        assert result == mock_llm

    def test_get_rate_limit_info_no_limits(self):
        """Test get_rate_limit_info with no limits."""
        TestClass = create_rate_limited_class()

        obj = TestClass()
        info = obj.get_rate_limit_info()

        assert info == {
            "requests_per_second": None,
            "tokens_per_second": None,
            "tokens_per_minute": None,
            "max_retries": 3,
            "retry_delay": 1.0,
            "check_every_n_seconds": None,
            "burst_size": None,
            "enabled": False,
        }

    def test_get_rate_limit_info_with_limits(self):
        """Test get_rate_limit_info with limits configured."""
        TestClass = create_rate_limited_class()

        obj = TestClass(requests_per_second=10, tokens_per_minute=100000, max_retries=5)
        info = obj.get_rate_limit_info()

        assert info["requests_per_second"] == 10
        assert info["tokens_per_minute"] == 100000
        assert info["max_retries"] == 5
        assert info["enabled"] is True

    def test_validation_constraints(self):
        """Test validation constraints on rate limit parameters."""
        TestClass = create_rate_limited_class()

        # Test negative values not allowed
        with pytest.raises(ValueError):
            TestClass(requests_per_second=-1)

        with pytest.raises(ValueError):
            TestClass(tokens_per_second=-100)

        with pytest.raises(ValueError):
            TestClass(max_retries=-1)

        with pytest.raises(ValueError):
            TestClass(retry_delay=-0.5)

        with pytest.raises(ValueError):
            TestClass(burst_size=0)  # Must be >= 1
