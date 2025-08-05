# Pyright Error Analysis Report

Generated: 2025-08-05 12:12:48

## Executive Summary

- **Total Errors**: 19,096
- **Total Warnings**: 1,567
- **Runtime Breaking Errors**: 3,920 (20.5%)
- **Files with Errors**: 2,374

## Severity Breakdown

| Severity | Count | Percentage | Description |
|----------|-------|------------|-------------|
| Critical | 3,920 | 20.5% | Will break at runtime |
| Medium | 15,141 | 79.3% | May cause runtime issues |
| Type-only | 35 | 0.2% | Type checking only |

## Error Categories

| Category | Count | Percentage | Typical Fix |
|----------|-------|------------|-------------|
| Import | 2,783 | 14.6% | Fix import paths or install packages |
| Type | 4,372 | 22.9% | Fix type annotations |
| Attribute | 5,596 | 29.3% | Check object types |
| Other | 6,345 | 33.2% | Various fixes needed |

## Package Distribution

| Package | Errors | Percentage |
|---------|--------|------------|
| haive-agents | 7,235 | 37.9% |
| haive-games | 5,264 | 27.6% |
| haive-core | 4,701 | 24.6% |
| haive-dataflow | 650 | 3.4% |
| haive-mcp | 573 | 3.0% |
| haive-prebuilt | 491 | 2.6% |
| haive-tools | 126 | 0.7% |

## Most Common Error Types

| Error Pattern | Occurrences |
|---------------|-------------|
| Cannot access attribute "" for class "" | 5,596 |
| "" is unknown import symbol | 2,783 |
| Argument of type "" cannot be assigned to parameter "" of type "" in function "" | 2,331 |
| No parameter named "" | 2,176 |
| "" is not a known attribute of "" | 1,183 |
| "" is not defined | 790 |
| Argument missing for parameter "" | 686 |
| Cannot assign to attribute "" for class "" | 533 |
| Type "" is not assignable to return type "" | 401 |
| Object of type "" is not subscriptable | 249 |
| No overloads for "" match the provided arguments | 207 |
| Cannot instantiate abstract class "" | 197 |
| Operator "" not supported for types "" and "" | 165 |
| "" method not defined on type "" | 165 |
| Arguments missing for parameters "", "" | 143 |
