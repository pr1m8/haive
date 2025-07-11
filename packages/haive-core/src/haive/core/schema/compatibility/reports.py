"""
Compatibility reporting and debugging tools.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union

from pydantic import BaseModel

from haive.core.schema.compatibility.compatibility import (
    FieldCompatibility,
    SchemaCompatibility,
)
from haive.core.schema.compatibility.types import (
    CompatibilityLevel,
    ConversionPath,
    FieldInfo,
    SchemaInfo,
)


@dataclass
class CompatibilityReport:
    """Comprehensive compatibility analysis report."""

    source_schema: SchemaInfo
    target_schema: SchemaInfo
    compatibility_result: SchemaCompatibility
    timestamp: datetime = field(default_factory=datetime.now)

    # Analysis results
    overall_compatible: bool = False
    compatibility_score: float = 0.0  # 0-100

    # Detailed findings
    field_analyses: Dict[str, FieldAnalysis] = field(default_factory=dict)
    conversion_paths: Dict[str, ConversionPath] = field(default_factory=dict)
    suggested_mappings: Dict[str, str] = field(default_factory=dict)

    # Issues and recommendations
    critical_issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    # Metadata
    analysis_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "source_schema": self.source_schema.name,
            "target_schema": self.target_schema.name,
            "overall_compatible": self.overall_compatible,
            "compatibility_score": self.compatibility_score,
            "compatibility_level": self.compatibility_result.level.value,
            "field_count": {
                "source": len(self.source_schema.fields),
                "target": len(self.target_schema.fields),
                "compatible": len(
                    [f for f in self.field_analyses.values() if f.is_compatible]
                ),
            },
            "critical_issues": self.critical_issues,
            "warnings": self.warnings,
            "recommendations": self.recommendations,
            "analysis_time_ms": self.analysis_time_ms,
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert report to JSON."""
        return json.dumps(self.to_dict(), indent=indent)

    def to_markdown(self) -> str:
        """Generate markdown report."""
        lines = [
            f"# Schema Compatibility Report",
            f"",
            f"**Generated**: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"## Summary",
            f"",
            f"- **Source Schema**: `{self.source_schema.name}`",
            f"- **Target Schema**: `{self.target_schema.name}`",
            f"- **Compatible**: {'✅ Yes' if self.overall_compatible else '❌ No'}",
            f"- **Compatibility Score**: {self.compatibility_score:.1f}/100",
            f"- **Compatibility Level**: {self.compatibility_result.level.value}",
            f"",
        ]

        # Field summary
        lines.extend(
            [
                f"## Field Analysis",
                f"",
                f"| Metric | Count |",
                f"|--------|-------|",
                f"| Source Fields | {len(self.source_schema.fields)} |",
                f"| Target Fields | {len(self.target_schema.fields)} |",
                f"| Compatible Fields | {len([f for f in self.field_analyses.values() if f.is_compatible])} |",
                f"| Missing Required | {len(self.compatibility_result.missing_required_fields)} |",
                f"| Extra Fields | {len(self.compatibility_result.extra_fields)} |",
                f"",
            ]
        )

        # Critical issues
        if self.critical_issues:
            lines.extend(
                [
                    f"## 🚨 Critical Issues",
                    f"",
                ]
            )
            for issue in self.critical_issues:
                lines.append(f"- {issue}")
            lines.append("")

        # Warnings
        if self.warnings:
            lines.extend(
                [
                    f"## ⚠️ Warnings",
                    f"",
                ]
            )
            for warning in self.warnings:
                lines.append(f"- {warning}")
            lines.append("")

        # Field details
        if self.field_analyses:
            lines.extend(
                [
                    f"## Field Compatibility Details",
                    f"",
                    f"| Field | Source Type | Target Type | Compatible | Notes |",
                    f"|-------|-------------|-------------|------------|-------|",
                ]
            )

            for field_name, analysis in self.field_analyses.items():
                compat_icon = "✅" if analysis.is_compatible else "❌"
                lines.append(
                    f"| {field_name} | "
                    f"{analysis.source_type or 'N/A'} | "
                    f"{analysis.target_type or 'N/A'} | "
                    f"{compat_icon} | "
                    f"{analysis.notes or '-'} |"
                )
            lines.append("")

        # Recommendations
        if self.recommendations:
            lines.extend(
                [
                    f"## 💡 Recommendations",
                    f"",
                ]
            )
            for i, rec in enumerate(self.recommendations, 1):
                lines.append(f"{i}. {rec}")
            lines.append("")

        # Performance
        lines.extend(
            [
                f"## Performance",
                f"",
                f"Analysis completed in {self.analysis_time_ms:.2f}ms",
            ]
        )

        return "\n".join(lines)


@dataclass
class FieldAnalysis:
    """Detailed analysis of field compatibility."""

    field_name: str
    source_type: Optional[str] = None
    target_type: Optional[str] = None
    is_compatible: bool = False
    compatibility_level: Optional[CompatibilityLevel] = None
    conversion_needed: bool = False
    conversion_path: Optional[str] = None
    issues: List[str] = field(default_factory=list)
    notes: Optional[str] = None


class ReportGenerator:
    """Generate detailed compatibility reports."""

    def generate_report(
        self,
        source_schema: SchemaInfo,
        target_schema: SchemaInfo,
        compatibility_result: SchemaCompatibility,
        conversion_registry: Optional[Any] = None,
        analysis_time_ms: Optional[float] = None,
    ) -> CompatibilityReport:
        """Generate a comprehensive compatibility report."""
        report = CompatibilityReport(
            source_schema=source_schema,
            target_schema=target_schema,
            compatibility_result=compatibility_result,
            overall_compatible=compatibility_result.is_compatible,
            analysis_time_ms=analysis_time_ms or 0.0,
        )

        # Calculate compatibility score
        report.compatibility_score = self._calculate_score(compatibility_result)

        # Analyze each field
        self._analyze_fields(report, compatibility_result, conversion_registry)

        # Generate issues and recommendations
        self._generate_issues(report, compatibility_result)
        self._generate_recommendations(report, compatibility_result)

        return report

    def _calculate_score(self, result: SchemaCompatibility) -> float:
        """Calculate compatibility score (0-100)."""
        if result.level == CompatibilityLevel.EXACT:
            return 100.0

        total_fields = len(result.target_schema.fields)
        if total_fields == 0:
            return 100.0

        # Start with base score from compatibility level
        base_scores = {
            CompatibilityLevel.EXACT: 100,
            CompatibilityLevel.SUBTYPE: 90,
            CompatibilityLevel.CONVERTIBLE: 70,
            CompatibilityLevel.COERCIBLE: 50,
            CompatibilityLevel.PARTIAL: 30,
            CompatibilityLevel.INCOMPATIBLE: 0,
        }
        score = base_scores.get(result.level, 0)

        # Adjust for missing required fields
        missing_penalty = len(result.missing_required_fields) * 15
        score = max(0, score - missing_penalty)

        # Adjust for incompatible fields
        incompatible_count = len(result.get_incompatible_fields())
        incompatible_penalty = incompatible_count * 10
        score = max(0, score - incompatible_penalty)

        # Bonus for extra compatible fields
        compatible_fields = len(
            [r for r in result.field_results.values() if r.is_compatible]
        )
        if compatible_fields > 0:
            bonus = (compatible_fields / total_fields) * 10
            score = min(100, score + bonus)

        return score

    def _analyze_fields(
        self,
        report: CompatibilityReport,
        result: SchemaCompatibility,
        conversion_registry: Optional[Any],
    ) -> None:
        """Analyze individual fields."""
        # Analyze matched fields
        for field_name, field_result in result.field_results.items():
            analysis = FieldAnalysis(
                field_name=field_name,
                source_type=str(field_result.source_field.type_info.type_hint),
                target_type=str(field_result.target_field.type_info.type_hint),
                is_compatible=field_result.is_compatible,
                compatibility_level=field_result.level,
                conversion_needed=field_result.needs_conversion,
                conversion_path=field_result.conversion_path,
                issues=field_result.issues,
            )

            # Add notes
            if field_result.level == CompatibilityLevel.EXACT:
                analysis.notes = "Perfect match"
            elif field_result.level == CompatibilityLevel.SUBTYPE:
                analysis.notes = "Subtype compatible"
            elif field_result.needs_conversion:
                analysis.notes = f"Conversion available: {field_result.conversion_path}"

            report.field_analyses[field_name] = analysis

        # Analyze missing fields
        for field_name in result.missing_required_fields:
            analysis = FieldAnalysis(
                field_name=field_name,
                target_type=str(
                    result.target_schema.fields[field_name].type_info.type_hint
                ),
                is_compatible=False,
                notes="Missing in source",
            )
            report.field_analyses[field_name] = analysis

    def _generate_issues(
        self,
        report: CompatibilityReport,
        result: SchemaCompatibility,
    ) -> None:
        """Generate critical issues and warnings."""
        # Critical issues
        if result.missing_required_fields:
            report.critical_issues.append(
                f"Missing {len(result.missing_required_fields)} required fields: "
                f"{', '.join(sorted(result.missing_required_fields))}"
            )

        incompatible = result.get_incompatible_fields()
        if incompatible:
            report.critical_issues.append(
                f"{len(incompatible)} incompatible fields: "
                f"{', '.join(sorted(incompatible))}"
            )

        # Warnings
        if result.extra_fields:
            report.warnings.append(
                f"{len(result.extra_fields)} extra fields in source will be ignored: "
                f"{', '.join(sorted(result.extra_fields))}"
            )

        conversion_fields = result.get_conversion_fields()
        if conversion_fields:
            report.warnings.append(
                f"{len(conversion_fields)} fields require conversion: "
                f"{', '.join(sorted(conversion_fields))}"
            )

    def _generate_recommendations(
        self,
        report: CompatibilityReport,
        result: SchemaCompatibility,
    ) -> None:
        """Generate actionable recommendations."""
        if result.is_compatible:
            if result.level == CompatibilityLevel.EXACT:
                report.recommendations.append(
                    "Schemas are perfectly compatible. No changes needed."
                )
            elif result.requires_mapping:
                report.recommendations.append(
                    "Use field mapping to handle conversions and missing fields."
                )
        else:
            # Missing fields recommendations
            if result.missing_required_fields:
                report.recommendations.append(
                    "Add the missing required fields to the source schema, "
                    "or provide default values in the mapping configuration."
                )

            # Type conversion recommendations
            incompatible = result.get_incompatible_fields()
            if incompatible:
                report.recommendations.append(
                    "Implement custom converters for incompatible field types, "
                    "or modify the schemas to use compatible types."
                )

            # Schema evolution recommendation
            if report.compatibility_score < 50:
                report.recommendations.append(
                    "Consider creating an adapter layer or intermediate schema "
                    "to bridge the compatibility gap."
                )


class VisualDiffer:
    """Generate visual diffs between schemas."""

    def generate_diff(
        self,
        source_schema: SchemaInfo,
        target_schema: SchemaInfo,
        result: SchemaCompatibility,
    ) -> str:
        """Generate a visual diff."""
        lines = []

        # Header
        lines.extend(
            [
                "Schema Diff",
                "===========",
                f"Source: {source_schema.name}",
                f"Target: {target_schema.name}",
                "",
            ]
        )

        # Collect all field names
        all_fields = set(source_schema.fields.keys()) | set(target_schema.fields.keys())

        for field_name in sorted(all_fields):
            source_field = source_schema.fields.get(field_name)
            target_field = target_schema.fields.get(field_name)

            if source_field and target_field:
                # Field exists in both
                if field_name in result.field_results:
                    compat = result.field_results[field_name]
                    if compat.is_compatible:
                        lines.append(f"  {field_name}: ✓ compatible")
                    else:
                        lines.append(f"- {field_name}: ✗ incompatible")
                        lines.append(f"    Source: {source_field.type_info.type_hint}")
                        lines.append(f"    Target: {target_field.type_info.type_hint}")
            elif source_field:
                # Only in source
                lines.append(f"+ {field_name}: (only in source)")
                lines.append(f"    Type: {source_field.type_info.type_hint}")
            else:
                # Only in target
                lines.append(f"- {field_name}: (only in target)")
                lines.append(f"    Type: {target_field.type_info.type_hint}")
                if target_field.is_required:
                    lines.append(f"    ⚠️  REQUIRED")

        return "\n".join(lines)


# Module-level convenience functions
def generate_report(
    source_schema: Union[Type[BaseModel], SchemaInfo],
    target_schema: Union[Type[BaseModel], SchemaInfo],
    mode: str = "subset",
) -> CompatibilityReport:
    """Generate a compatibility report between schemas."""
    from haive.core.schema.compatibility.analyzer import TypeAnalyzer
    from haive.core.schema.compatibility.compatibility import CompatibilityChecker

    analyzer = TypeAnalyzer()
    checker = CompatibilityChecker(analyzer=analyzer)

    # Convert to SchemaInfo if needed
    if isinstance(source_schema, type):
        source_schema = analyzer.analyze_schema(source_schema)
    if isinstance(target_schema, type):
        target_schema = analyzer.analyze_schema(target_schema)

    # Check compatibility
    import time

    start_time = time.time()
    compatibility_result = checker.check_schema_compatibility(
        source_schema, target_schema, mode
    )
    analysis_time = (time.time() - start_time) * 1000

    # Generate report
    generator = ReportGenerator()
    return generator.generate_report(
        source_schema,
        target_schema,
        compatibility_result,
        analysis_time_ms=analysis_time,
    )


def print_compatibility_report(
    source: Union[Type[BaseModel], SchemaInfo],
    target: Union[Type[BaseModel], SchemaInfo],
    format: str = "markdown",
) -> None:
    """Print a compatibility report to console."""
    report = generate_report(source, target)

    if format == "markdown":
        print(report.to_markdown())
    elif format == "json":
        print(report.to_json())
    elif format == "dict":
        import pprint

        pprint.pprint(report.to_dict())
    else:
        raise ValueError(f"Unknown format: {format}")
