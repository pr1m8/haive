"""Token tracking component for memory operations.

Monitors token usage across memory operations and triggers
summarization or rewriting when approaching context limits.
"""

import logging
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class TokenUsageEntry(BaseModel):
    """Single token usage entry for tracking."""

    operation: str = Field(..., description="Operation name")
    tokens: int = Field(..., ge=0, description="Number of tokens used")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict[str, Any] = Field(default_factory=dict)


class TokenThresholds(BaseModel):
    """Token usage thresholds for different alert levels."""

    warning: float = Field(default=0.7, ge=0.0, le=1.0)
    critical: float = Field(default=0.85, ge=0.0, le=1.0)
    emergency: float = Field(default=0.95, ge=0.0, le=1.0)

    def get_status(self, usage_ratio: float) -> str:
        """Get status based on usage ratio."""
        if usage_ratio >= self.emergency:
            return "EMERGENCY"
        if usage_ratio >= self.critical:
            return "CRITICAL"
        if usage_ratio >= self.warning:
            return "WARNING"
        return "OK"


class TokenTracker(BaseModel):
    """Track token usage across memory operations with intelligent monitoring.

    Features:
    - Real-time token tracking by operation
    - Threshold monitoring with alerts
    - Usage pattern analysis
    - Recommendations for optimization
    """

    # Core tracking
    total_tokens: int = Field(default=0, ge=0)
    tokens_by_operation: dict[str, int] = Field(default_factory=dict)
    usage_history: list[TokenUsageEntry] = Field(default_factory=list)

    # Configuration
    max_context_tokens: int = Field(default=8000, ge=1000)
    thresholds: TokenThresholds = Field(default_factory=TokenThresholds)

    # Tracking window
    window_size: int = Field(default=100, description="Number of operations to track")

    # Analytics
    operation_averages: dict[str, float] = Field(default_factory=dict)
    peak_usage: int = Field(default=0, ge=0)

    def track(
        self, operation: str, tokens: int, metadata: dict[str, Any] | None = None
    ) -> None:
        """Track tokens for an operation.

        Args:
            operation: Name of the operation
            tokens: Number of tokens used
            metadata: Optional metadata about the operation
        """
        # Update totals
        self.total_tokens += tokens
        self.tokens_by_operation[operation] = (
            self.tokens_by_operation.get(operation, 0) + tokens
        )

        # Update peak
        self.peak_usage = max(self.peak_usage, self.total_tokens)

        # Add to history
        entry = TokenUsageEntry(
            operation=operation, tokens=tokens, metadata=metadata or {}
        )
        self.usage_history.append(entry)

        # Maintain window size
        if len(self.usage_history) > self.window_size:
            removed = self.usage_history.pop(0)
            # Adjust totals
            self.total_tokens -= removed.tokens
            self.tokens_by_operation[removed.operation] -= removed.tokens

        # Update averages
        self._update_averages(operation)

        # Log if approaching limits
        status = self.get_status()
        if status != "OK":
            logger.warning(
                f"Token usage {status}: {self.total_tokens}/{self.max_context_tokens} "
                f"({self.get_usage_ratio():.1%}) after {operation}"
            )

    def reset_tokens(self, keep_history: bool = True) -> None:
        """Reset token counts while optionally keeping history.

        Args:
            keep_history: Whether to keep usage history
        """
        self.total_tokens = 0
        self.tokens_by_operation.clear()

        if not keep_history:
            self.usage_history.clear()
            self.operation_averages.clear()

        logger.info("Token tracker reset")

    def get_usage_ratio(self) -> float:
        """Get current usage ratio (0.0 to 1.0)."""
        return (
            self.total_tokens / self.max_context_tokens
            if self.max_context_tokens > 0
            else 0.0
        )

    def get_status(self) -> str:
        """Get current status based on thresholds."""
        return self.thresholds.get_status(self.get_usage_ratio())

    def get_remaining_tokens(self) -> int:
        """Get number of tokens remaining before limit."""
        return max(0, self.max_context_tokens - self.total_tokens)

    def can_fit_operation(self, estimated_tokens: int) -> bool:
        """Check if an operation can fit within remaining tokens.

        Args:
            estimated_tokens: Estimated tokens for the operation

        Returns:
            True if operation can fit, False otherwise
        """
        return (self.total_tokens + estimated_tokens) <= self.max_context_tokens

    def get_recommendations(self) -> list[str]:
        """Get recommendations based on usage patterns.

        Returns:
            List of recommendation strings
        """
        recommendations = []
        self.get_usage_ratio()
        status = self.get_status()

        if status == "EMERGENCY":
            recommendations.append("URGENT: Immediate summarization required")
            recommendations.append("Consider aggressive memory compression")
        elif status == "CRITICAL":
            recommendations.append("Initiate memory summarization")
            recommendations.append("Prepare for memory rewriting")
        elif status == "WARNING":
            recommendations.append("Monitor token usage closely")
            recommendations.append("Consider selective summarization")

        # Analyze heavy operations
        if self.operation_averages:
            heavy_ops = sorted(
                self.operation_averages.items(), key=lambda x: x[1], reverse=True
            )[:3]

            for op, avg in heavy_ops:
                if avg > self.max_context_tokens * 0.1:  # >10% per operation
                    recommendations.append(
                        f"Optimize '{op}' operations (avg: {avg:.0f} tokens)"
                    )

        return recommendations

    def get_usage_summary(self) -> dict[str, Any]:
        """Get comprehensive usage summary.

        Returns:
            Dictionary with usage statistics and analysis
        """
        return {
            "total_tokens": self.total_tokens,
            "max_tokens": self.max_context_tokens,
            "usage_ratio": round(self.get_usage_ratio(), 3),
            "status": self.get_status(),
            "remaining_tokens": self.get_remaining_tokens(),
            "peak_usage": self.peak_usage,
            "operations": {
                "total": len(self.usage_history),
                "by_type": dict(self.tokens_by_operation),
                "averages": dict(self.operation_averages),
            },
            "recommendations": self.get_recommendations(),
        }

    def estimate_tokens_for_content(self, content: str) -> int:
        """Estimate tokens for given content.

        Simple estimation: ~4 characters per token (rough approximation).
        In production, would use proper tokenizer.

        Args:
            content: Text content to estimate

        Returns:
            Estimated token count
        """
        # Simple estimation - in production use tiktoken or model tokenizer
        return len(content) // 4

    def _update_averages(self, operation: str) -> None:
        """Update operation averages."""
        operation_entries = [
            entry for entry in self.usage_history if entry.operation == operation
        ]

        if operation_entries:
            total = sum(entry.tokens for entry in operation_entries)
            self.operation_averages[operation] = total / len(operation_entries)

    def suggest_compression_targets(
        self, target_reduction: float = 0.3
    ) -> list[tuple[str, int]]:
        """Suggest operations to target for compression.

        Args:
            target_reduction: Target reduction ratio (0.0 to 1.0)

        Returns:
            List of (operation, potential_savings) tuples
        """
        if not self.tokens_by_operation:
            return []

        # Sort operations by token usage
        sorted_ops = sorted(
            self.tokens_by_operation.items(), key=lambda x: x[1], reverse=True
        )

        suggestions = []
        target_tokens = int(self.total_tokens * target_reduction)
        accumulated = 0

        for op, tokens in sorted_ops:
            if accumulated >= target_tokens:
                break

            # Estimate 30% compression per operation
            potential_savings = int(tokens * 0.3)
            suggestions.append((op, potential_savings))
            accumulated += potential_savings

        return suggestions
