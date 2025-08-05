# Pyright Error Analysis Report

Generated: 2025-08-05 12:34:41

## Executive Summary

- **Total Errors**: 10,375
- **Total Warnings**: 1,429
- **Runtime Breaking Errors**: 2,596 (25.0%)
- **Files with Errors**: 1,625

## Severity Breakdown

| Severity | Count | Percentage | Description |
|----------|-------|------------|-------------|
| Critical | 2,596 | 25.0% | Will break at runtime |
| Medium | 7,730 | 74.5% | May cause runtime issues |
| Type-only | 49 | 0.5% | Type checking only |

## Error Categories

| Category | Count | Percentage | Typical Fix |
|----------|-------|------------|-------------|
| Import | 673 | 6.5% | Fix import paths or install packages |
| Type | 2,882 | 27.8% | Fix type annotations |
| Attribute | 3,139 | 30.3% | Check object types |
| Other | 3,681 | 35.5% | Various fixes needed |

## Package Distribution

| Package | Errors | Percentage |
|---------|--------|------------|
| haive-agents | 4,376 | 42.2% |
| haive-core | 2,961 | 28.5% |
| haive-games | 1,481 | 14.3% |
| haive-dataflow | 647 | 6.2% |
| haive-prebuilt | 537 | 5.2% |
| haive-tools | 137 | 1.3% |
| haive-mcp | 127 | 1.2% |

## Most Common Error Types

| Error Pattern | Occurrences |
|---------------|-------------|
| Cannot access attribute "" for class "" | 3,139 |
| Argument of type "" cannot be assigned to parameter "" of type "" in function "" | 1,468 |
| No parameter named "" | 987 |
| "" is not defined | 809 |
| "" is not a known attribute of "" | 802 |
| "" is unknown import symbol | 673 |
| Type "" is not assignable to return type "" | 411 |
| Cannot assign to attribute "" for class "" | 380 |
| Argument missing for parameter "" | 205 |
| Type "" is not assignable to declared type "" | 146 |
| "" method not defined on type "" | 142 |
| No overloads for "" match the provided arguments | 119 |
| Cannot instantiate abstract class "" | 80 |
| Expression of type "" cannot be assigned to parameter of type "" | 69 |
| Arguments missing for parameters "", "" | 57 |
