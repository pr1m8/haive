# Documentation Maintenance

Guidelines for keeping Haive documentation current, accurate, and useful over time.

## 🎯 Maintenance Philosophy

### 1. **Living Documentation**

Documentation should evolve with the codebase and user needs. Stale documentation is worse than no documentation.

### 2. **Ownership and Accountability**

Every piece of documentation should have a clear owner responsible for keeping it current.

### 3. **Automated Where Possible**

Use automation to reduce manual maintenance burden and catch issues early.

### 4. **User-Driven Updates**

Prioritize maintenance based on user feedback and usage patterns.

## 📅 Maintenance Schedule

### Daily Automated Checks

```bash
# Automated daily tasks
- Link validation across all documentation
- Spell check on new/modified content
- Code example syntax validation
- Image reference verification
- Search index updates
```

### Weekly Reviews

```
Monday: Review user feedback and issues
Wednesday: Check analytics for usage patterns
Friday: Update priority maintenance queue
```

### Monthly Deep Reviews

```
Week 1: Getting Started documentation
Week 2: User Guides and tutorials
Week 3: API Reference accuracy
Week 4: Examples and code samples
```

### Quarterly Comprehensive Audits

```
Q1: Content accuracy and completeness
Q2: Information architecture review
Q3: User experience and navigation
Q4: Performance and accessibility
```

## 🔧 Maintenance Triggers

### Code Changes

Documentation updates required for:

#### **API Changes**

```markdown
Trigger: Function signatures change
Action: Update API reference and examples
Owner: Developer making the change
Timeline: Same PR as code change
```

#### **Feature Additions**

```markdown
Trigger: New features merged
Action: Add user guides and examples
Owner: Feature developer + tech writer
Timeline: Within 1 week of feature release
```

#### **Deprecations**

```markdown
Trigger: Features marked deprecated
Action: Update docs with deprecation notices
Owner: Team lead + tech writer
Timeline: Immediate with deprecation
```

### User Feedback

Documentation updates triggered by:

#### **Support Questions**

```markdown
Trigger: Repeated questions on same topic
Action: Clarify or expand documentation
Owner: Support team + tech writer
Timeline: Within 2 weeks of pattern identification
```

#### **GitHub Issues**

```markdown
Trigger: Documentation-related issues
Action: Address reported problems
Owner: Issue assignee
Timeline: Based on issue priority
```

#### **User Surveys**

```markdown
Trigger: Quarterly user feedback
Action: Strategic documentation improvements
Owner: Product team + tech writer
Timeline: Quarterly planning cycle
```

## 📋 Maintenance Workflows

### Content Review Process

#### **Regular Content Audit**

```markdown
1. **Identify content to review**
   - Oldest content first
   - High-traffic pages priority
   - User-reported issues

2. **Review criteria**
   - Technical accuracy
   - Code examples work
   - Links are valid
   - Information is current
   - Style guide compliance

3. **Update process**
   - Make necessary changes
   - Test all examples
   - Validate all links
   - Update last-reviewed date

4. **Quality assurance**
   - Peer review changes
   - User testing if significant
   - Monitor for issues post-update
```

#### **Link Maintenance**

```bash
# Weekly link checking
find docs/ -name "*.md" -exec markdown-link-check {} \;

# Broken link report
markdown-link-check docs/**/*.md --reporter json > link-report.json

# Fix broken links
# - Update URLs that have moved
# - Remove links to deleted content
# - Archive or replace dead external links
```

### Version Management

#### **Version-Specific Content**

````markdown
<!-- Version annotations -->

> **Note**: This feature requires Haive v2.0 or later.

> **Deprecated**: This API is deprecated as of v1.5. Use [NewAPI](../new-api.md) instead.

<!-- Version-specific examples -->

```python
# Haive v2.0+
agent = SimpleAgent(name="helper", version="v2")

# Haive v1.x (deprecated)
agent = Agent.create(name="helper")
```
````

````

#### **Migration Guides**
For major version changes:
```markdown
# Migration Guide: v1.x to v2.0

## Breaking Changes
- [Change 1](./breaking-changes.md#change-1)
- [Change 2](./breaking-changes.md#change-2)

## Update Steps
1. [Update dependencies](./update-deps.md)
2. [Migrate configuration](./migrate-config.md)
3. [Update code](./update-code.md)
4. [Test changes](./test-migration.md)

## Compatibility
- [Backward compatibility](./compatibility.md)
- [Timeline for deprecations](./deprecation-timeline.md)
````

## 🤖 Automation Tools

### Automated Validation

#### **Content Validation**

```yaml
# .github/workflows/docs-validation.yml
name: Documentation Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Check links
        run: markdown-link-check docs/**/*.md

      - name: Spell check
        run: cspell "docs/**/*.md"

      - name: Validate code examples
        run: python scripts/validate-examples.py

      - name: Check formatting
        run: prettier --check "docs/**/*.md"
```

#### **Example Testing**

````python
# scripts/validate-examples.py
"""Validate all code examples in documentation."""

import re
import ast
import subprocess
from pathlib import Path

def extract_python_code(markdown_file):
    """Extract Python code blocks from markdown."""
    content = markdown_file.read_text()
    python_blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
    return python_blocks

def validate_syntax(code):
    """Check if Python code has valid syntax."""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def test_examples():
    """Test all Python examples in documentation."""
    docs_dir = Path("docs")
    for md_file in docs_dir.rglob("*.md"):
        python_blocks = extract_python_code(md_file)
        for i, code in enumerate(python_blocks):
            if not validate_syntax(code):
                print(f"Syntax error in {md_file}:{i+1}")
                return False
    return True

if __name__ == "__main__":
    if test_examples():
        print("✅ All examples pass validation")
    else:
        print("❌ Some examples have issues")
        exit(1)
````

### Monitoring and Alerts

#### **Content Freshness**

```python
# scripts/content-freshness.py
"""Monitor documentation freshness."""

import os
from datetime import datetime, timedelta
from pathlib import Path

def check_freshness(max_age_days=90):
    """Check for documentation older than max_age_days."""
    cutoff = datetime.now() - timedelta(days=max_age_days)
    stale_files = []

    for md_file in Path("docs").rglob("*.md"):
        modified = datetime.fromtimestamp(md_file.stat().st_mtime)
        if modified < cutoff:
            age_days = (datetime.now() - modified).days
            stale_files.append((md_file, age_days))

    return stale_files

def generate_freshness_report():
    """Generate report of stale documentation."""
    stale_files = check_freshness()

    if stale_files:
        print("📅 Stale Documentation Report")
        print("=" * 40)
        for file_path, age in sorted(stale_files, key=lambda x: x[1], reverse=True):
            print(f"{file_path}: {age} days old")
    else:
        print("✅ All documentation is current")

if __name__ == "__main__":
    generate_freshness_report()
```

#### **Usage Analytics**

```javascript
// Track documentation usage
function trackPageView(page, section) {
  analytics.track("Documentation Page View", {
    page: page,
    section: section,
    timestamp: new Date().toISOString(),
  });
}

// Track search queries
function trackSearch(query, results_count) {
  analytics.track("Documentation Search", {
    query: query,
    results_count: results_count,
    timestamp: new Date().toISOString(),
  });
}

// Generate monthly reports
function generateUsageReport() {
  // Top viewed pages
  // Common search queries
  // User journey analysis
  // Exit points identification
}
```

## 📊 Quality Metrics

### Measurement Standards

#### **Content Quality Metrics**

```
- Link health rate (target: >99%)
- Content freshness (target: <90 days average age)
- Code example success rate (target: 100%)
- User satisfaction score (target: >4.0/5)
- Time to find information (target: <2 minutes)
```

#### **Usage Metrics**

```
- Page views per section
- Search success rate
- Bounce rate on landing pages
- Time spent on documentation
- User journey completion rates
```

### Reporting Dashboard

#### **Weekly Status Report**

```markdown
# Documentation Health Report - Week of [Date]

## 📊 Key Metrics

- Link health: 99.2% (↑ 0.3%)
- Content freshness: 45 days average (↓ 5 days)
- User satisfaction: 4.2/5 (→ no change)

## 🔧 Maintenance Activities

- Updated 12 code examples
- Fixed 3 broken links
- Refreshed 5 outdated guides

## 🎯 Focus Areas

- Getting started user journey optimization
- API reference completeness review
- Mobile navigation improvements

## 📈 Usage Highlights

- Most viewed: Agent Configuration Guide (1,247 views)
- Top search: "agent tools configuration" (89 searches)
- Support ticket reduction: 15% (↓ from doc improvements)
```

## 👥 Ownership and Responsibilities

### Role Definitions

#### **Documentation Owner**

- **Responsibility**: Overall documentation strategy and quality
- **Activities**: Planning, coordination, standards enforcement
- **Frequency**: Daily oversight, weekly planning

#### **Technical Writers**

- **Responsibility**: Content creation and major updates
- **Activities**: Writing, editing, user research
- **Frequency**: Daily writing, weekly reviews

#### **Developers**

- **Responsibility**: Code-related documentation updates
- **Activities**: API docs, code examples, technical accuracy
- **Frequency**: With each code change

#### **Community Managers**

- **Responsibility**: User feedback integration
- **Activities**: Issue triage, feedback collection, community input
- **Frequency**: Daily monitoring, weekly reports

### Escalation Process

#### **Issue Severity Levels**

```
Critical (1-4 hours): Broken getting started guide, major security info
High (1-2 days): Broken API references, incorrect examples
Medium (1 week): Minor inaccuracies, style inconsistencies
Low (1 month): Enhancement requests, nice-to-have improvements
```

## ✅ Maintenance Checklist

### Daily Tasks

- [ ] Review automated health checks
- [ ] Address critical documentation issues
- [ ] Monitor user feedback channels
- [ ] Update any code-dependent documentation

### Weekly Tasks

- [ ] Run comprehensive link validation
- [ ] Review and triage documentation issues
- [ ] Update content freshness report
- [ ] Plan upcoming maintenance activities

### Monthly Tasks

- [ ] Deep review of assigned content sections
- [ ] Analyze usage metrics and trends
- [ ] Update maintenance priorities
- [ ] Coordinate with development teams on upcoming changes

### Quarterly Tasks

- [ ] Comprehensive documentation audit
- [ ] User experience review and testing
- [ ] Information architecture assessment
- [ ] Maintenance process improvement review

---

**Remember**: Documentation maintenance is an investment in user success and team productivity. Consistent, proactive maintenance prevents the accumulation of technical debt in your documentation system.
