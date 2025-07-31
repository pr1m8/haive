# Documentation Hierarchy

Comprehensive guide to organizing documentation structure in the Haive project.

## 🏗️ Overall Architecture

The Haive documentation follows a three-tier hierarchy designed to serve different audiences and use cases:

```
Haive Documentation Ecosystem
├── 📖 User Documentation (/docs/source/)
│   ├── Getting Started
│   ├── User Guides
│   ├── API References
│   └── Agent Showcase
├── 🔧 Developer Documentation (/project_docs/)
│   ├── Architecture Decisions
│   ├── Development Guides
│   ├── Technical Notes
│   └── Documentation Standards
└── 📦 Package Documentation (/packages/*/README.md)
    ├── Package Overview
    ├── Installation Instructions
    └── Package-specific Examples
```

## 📖 User Documentation Structure

### Primary Hierarchy

```
docs/source/
├── index.rst                    # Main landing page
├── getting-started/
│   ├── installation.md
│   ├── quick-start.md
│   └── first-agent.md
├── guides/
│   ├── agents/
│   ├── tools/
│   ├── configuration/
│   └── deployment/
├── api/
│   ├── core/
│   ├── agents/
│   ├── tools/
│   └── games/
├── agents/
│   ├── showcase.md
│   ├── categories/
│   └── complete_index.md
└── examples/
    ├── tutorials/
    ├── recipes/
    └── integrations/
```

### Content Organization Principles

#### **By User Journey**

```
1. Getting Started → Quick success
2. User Guides → Common tasks
3. API Reference → Complete details
4. Examples → Real applications
```

#### **By Complexity**

```
Basic → Intermediate → Advanced → Expert
```

#### **By Domain**

```
Core Concepts → Agents → Tools → Games → Deployment
```

## 🔧 Developer Documentation Structure

### Project Documentation

```
project_docs/
├── README.md                    # Navigation hub
├── claude_documentation/        # CLAUDE-specific docs
├── docs/                       # This documentation system
├── agent_analysis/             # Agent implementation analysis
├── documentation_cleanup/      # Cleanup project records
└── human/                      # Human-readable project notes
```

### Technical Documentation

```
project_docs/docs/
├── writing-guidelines/         # How to write
├── organization-standards/     # How to organize
├── content-types/             # What to write
├── tools-and-automation/      # Documentation tooling
├── quality-assurance/         # Review processes
└── examples/                  # Templates and examples
```

## 📦 Package Documentation Structure

### Individual Package Structure

```
packages/haive-{name}/
├── README.md                   # Package overview
├── docs/
│   ├── api/                   # Package API reference
│   ├── examples/              # Package-specific examples
│   └── guides/                # Package usage guides
├── src/haive/{name}/
│   └── __init__.py            # Module docstrings
└── tests/
    └── docs/                  # Documentation tests
```

### README Template Structure

```markdown
# Package Name

Brief description and primary use case.

## Installation

Package-specific installation instructions.

## Quick Start

Minimal working example.

## Key Features

- Feature 1
- Feature 2
- Feature 3

## Documentation

Links to detailed documentation.

## Examples

Links to examples and tutorials.
```

## 🎯 Hierarchy Principles

### 1. **Progressive Disclosure**

Information should be layered from general to specific:

```
Topic Overview
├── Basic Concepts
├── Common Use Cases
├── Advanced Features
└── Complete Reference
```

### 2. **Multiple Entry Points**

Users should be able to enter the documentation at different levels:

- **Task-oriented**: "How do I...?"
- **Reference-oriented**: "What does...?"
- **Learning-oriented**: "Teach me about..."
- **Problem-oriented**: "Fix this issue..."

### 3. **Clear Relationships**

Related content should be connected:

```markdown
## See Also

- [Related Concept](../concepts/related.md)
- [Similar Tool](../tools/similar.md)
- [Advanced Usage](../advanced/usage.md)
```

### 4. **Consistent Depth**

Similar types of content should have similar depth:

```
All User Guides:
├── Overview
├── Basic Usage
├── Configuration
├── Advanced Features
└── Troubleshooting
```

## 📋 Folder Organization

### Naming Patterns

#### **By Function**

```
getting-started/     # Functional grouping
user-guides/        # User-oriented
api-reference/      # Type-based
```

#### **By Domain**

```
agents/             # Domain-specific
tools/              # Feature-specific
games/              # Module-specific
```

#### **By Audience**

```
beginners/          # Skill-level based
developers/         # Role-based
contributors/       # Activity-based
```

### Depth Guidelines

#### **Maximum Depth: 4 Levels**

```
docs/
├── guides/                     # Level 1
│   ├── agents/                 # Level 2
│   │   ├── configuration/      # Level 3
│   │   │   ├── basic.md       # Level 4
│   │   │   └── advanced.md    # Level 4
│   │   └── deployment/        # Level 3
│   └── tools/                 # Level 2
```

#### **Folder Size Guidelines**

- **5-15 items per folder** - Optimal for navigation
- **Max 20 items** - Before considering reorganization
- **Min 3 items** - Before considering consolidation

## 🔗 Cross-Reference Strategy

### Linking Patterns

#### **Hierarchical Links**

```markdown
<!-- Parent to child -->

For details, see [Agent Configuration](agents/configuration.md)

<!-- Child to parent -->

This extends the concepts in [Agent Overview](../overview.md)

<!-- Sibling links -->

See also [Tool Configuration](../tools/configuration.md)
```

#### **Contextual Links**

```markdown
<!-- Prerequisite -->

Before proceeding, complete [Installation](../getting-started/installation.md)

<!-- Follow-up -->

Next, try [Creating Your First Agent](../tutorials/first-agent.md)

<!-- Alternative -->

For a different approach, see [Configuration Files](./config-files.md)
```

### Navigation Aids

#### **Breadcrumbs**

```markdown
[Home](../../index.md) > [Guides](../index.md) > [Agents](./index.md) > Configuration
```

#### **Table of Contents**

```markdown
## On This Page

- [Basic Configuration](#basic-configuration)
- [Advanced Options](#advanced-options)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
```

#### **Related Content**

```markdown
## Related Pages

- [Agent Types](./types.md) - Different types of agents
- [Tool Integration](../tools/integration.md) - Adding tools to agents
- [Deployment Guide](../deployment/overview.md) - Production deployment
```

## ✅ Quality Standards

### Consistency Checks

- [ ] Naming conventions followed
- [ ] Depth limits respected
- [ ] Cross-references work
- [ ] Navigation is clear
- [ ] Content is in logical location

### Usability Tests

- [ ] New users can find getting started
- [ ] Existing users can find reference material
- [ ] Developers can find technical details
- [ ] Search finds relevant content
- [ ] Mobile navigation works

### Maintenance Requirements

- [ ] Clear ownership defined
- [ ] Update procedures documented
- [ ] Review schedule established
- [ ] Broken link monitoring
- [ ] Content freshness tracking

---

**Remember**: Good hierarchy serves the user's mental model, not the system's internal structure. Organize by how people think about and use the information.
