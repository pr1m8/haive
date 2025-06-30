# Navigation Strategy

Comprehensive guide for creating intuitive navigation and cross-references in Haive documentation.

## 🧭 Navigation Principles

### 1. **Multiple Pathways**
Users should be able to reach the same information through different routes:
- **Hierarchical navigation** - Follow the folder structure
- **Contextual links** - Jump between related topics
- **Search results** - Find content directly
- **Landing pages** - Curated entry points

### 2. **Breadcrumb Trail**
Users should always know where they are and how they got there:
```markdown
[Home](../../index.md) > [Guides](../index.md) > [Agents](./index.md) > Configuration
```

### 3. **Progressive Disclosure**
Navigation should reveal complexity gradually:
```
Overview → Basic Usage → Advanced Features → Complete Reference
```

### 4. **Contextual Relevance**
Links should be relevant to the current content and user goals.

## 🗺️ Navigation Structure

### Primary Navigation

#### **Main Menu Structure**
```
docs/source/
├── Getting Started          # New user entry point
├── User Guides             # Task-oriented content
├── API Reference           # Complete technical reference
├── Agent Showcase          # Live examples and demos
└── Examples               # Tutorials and recipes
```

#### **Landing Page Pattern**
Each major section should have a landing page:

```markdown
# Section Title

Brief overview of the section and what users will find here.

## What's in this section
- [Subsection 1](subsection-1/) - Brief description
- [Subsection 2](subsection-2/) - Brief description
- [Subsection 3](subsection-3/) - Brief description

## Quick links
- [Most common task](./common-task.md)
- [Getting help](./troubleshooting.md)

## Prerequisites
What users need to know before diving into this section.
```

### Secondary Navigation

#### **In-Page Navigation**
For longer pages, provide navigation aids:

```markdown
## On this page
- [Basic setup](#basic-setup)
- [Configuration options](#configuration-options)
- [Advanced usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

<!-- Page content -->

## What's next
- [Next logical step](./next-step.md)
- [Alternative approach](./alternative.md)
- [Related concept](../related/concept.md)
```

#### **Sidebar Navigation**
Auto-generated from folder structure:
```
Agents/
├── Overview
├── Getting Started
├── Configuration
├── Tool Integration
├── Advanced Features
└── Troubleshooting
```

## 🔗 Cross-Reference Strategy

### Link Types

#### **Contextual Links**
Embedded naturally in content:
```markdown
Agents use [tools](../tools/overview.md) to access external capabilities. 
The most common tools include [web search](../tools/web-search.md) and 
[calculators](../tools/calculator.md).
```

#### **Reference Links**
Explicit references to related content:
```markdown
## See also
- [Tool Configuration](../tools/configuration.md) - How to configure tools
- [Agent Types](./types.md) - Different types of agents available
- [Deployment Guide](../deployment/overview.md) - Production deployment
```

#### **Navigational Links**
Help users move through workflows:
```markdown
## Prerequisites
Before proceeding, ensure you have:
- [Installed the core package](../getting-started/installation.md)
- [Set up your API keys](../configuration/api-keys.md)

## Next steps
After completing this guide:
1. [Configure your first tool](../tools/first-tool.md)
2. [Test your agent](./testing.md)
3. [Deploy to production](../deployment/overview.md)
```

### Link Patterns

#### **Hierarchical References**
```markdown
<!-- Parent to child -->
For detailed configuration options, see [Agent Configuration](./configuration.md)

<!-- Child to parent -->
This builds on the concepts in [Agent Overview](../overview.md)

<!-- Sibling references -->
For tool-specific configuration, see [Tool Setup](../tools/setup.md)
```

#### **Cross-Domain References**
```markdown
<!-- Between major sections -->
For deployment considerations, see the [Deployment Guide](../../deployment/overview.md)

<!-- To external resources -->
Learn more about LangChain in the [official documentation](https://langchain-ai.github.io/langchain/)
```

## 📍 Location Indicators

### Breadcrumbs

#### **Format Standards**
```markdown
[Home](../../index.md) > [Section](../index.md) > [Subsection](./index.md) > Current Page
```

#### **Implementation**
Place breadcrumbs at the top of each page:
```markdown
---
breadcrumb: "Home > Guides > Agents > Configuration"
---

# Agent Configuration

Brief description of the page content.
```

### Page Context

#### **Section Identification**
Help users understand where they are:
```markdown
# Agent Configuration
*Part of the [User Guides](../index.md) section*

Configuration options for customizing agent behavior.
```

#### **Progress Indicators**
For multi-step processes:
```markdown
# Step 3: Configure Tools
*Step 3 of 5 in [Setting Up Your First Agent](./index.md)*

Now that you've created your agent, let's add some tools.
```

## 🔍 Search and Discovery

### Searchable Content

#### **Search-Friendly Headings**
Use descriptive headings that match search terms:
```markdown
✅ Good:
## Installing the Haive core package
## Configuring OpenAI API keys
## Troubleshooting connection errors

❌ Bad:
## Installation
## Configuration  
## Troubleshooting
```

#### **Keyword Integration**
Include relevant keywords naturally:
```markdown
To create a **SimpleAgent** in Haive, you'll use the **agent creation** 
process. This **agent setup** tutorial covers the **basic configuration** 
needed for **agent development**.
```

### Content Discovery

#### **Topic Clustering**
Group related content with hub pages:
```markdown
# Agent Development Hub

Everything you need to know about developing agents in Haive.

## Getting Started
- [Your first agent](./first-agent.md)
- [Basic configuration](./configuration.md)
- [Adding tools](./tools.md)

## Advanced Topics
- [Custom state schemas](./custom-state.md)
- [Error handling](./error-handling.md)
- [Performance optimization](./performance.md)

## Reference
- [Agent API](../../api/agents.md)
- [Configuration options](./config-reference.md)
- [Examples](../../examples/agents/)
```

#### **Cross-References Matrix**
Systematic linking between related topics:
```markdown
<!-- In agent configuration -->
Related: [Tool Configuration](../tools/config.md) | [Deployment](../deploy/config.md)

<!-- In tool configuration -->
Related: [Agent Configuration](../agents/config.md) | [Security](../security/tools.md)
```

## 🎯 User Journey Navigation

### Entry Points

#### **By User Type**
```markdown
# Welcome to Haive

Choose your path:

## 👋 New to Haive?
Start with our [Getting Started Guide](./getting-started/overview.md)

## 🔧 Developer?
Jump to [API Documentation](./api/overview.md)

## 🚀 Ready to Deploy?
See our [Deployment Guide](./deployment/overview.md)
```

#### **By Use Case**
```markdown
# Agent Use Cases

Find examples for your specific needs:

## 💬 Conversational Agents
- [Chat bots](./examples/chatbots.md)
- [Customer service](./examples/customer-service.md)

## 🔍 Research Agents  
- [Web research](./examples/web-research.md)
- [Data analysis](./examples/data-analysis.md)
```

### Flow Navigation

#### **Linear Workflows**
For step-by-step processes:
```markdown
---
# At the bottom of each step
## Navigation
[← Previous: Installation](./01-installation.md) | [Next: Configuration →](./03-configuration.md)

**Tutorial Progress:** 2 of 5 steps complete
```

#### **Non-Linear Exploration**
For reference material:
```markdown
## Explore this section
- **New to agents?** Start with [Agent Basics](./basics.md)
- **Need specific info?** Try [Quick Reference](./reference.md)  
- **Want examples?** See [Common Patterns](./patterns.md)
- **Having issues?** Check [Troubleshooting](./troubleshooting.md)
```

## 📱 Responsive Navigation

### Mobile Considerations

#### **Collapsible Menus**
Ensure navigation works on small screens:
```markdown
<!-- Use shorter link text for mobile -->
✅ Mobile-friendly:
- [Quick Start](./quick-start.md)
- [API Docs](./api.md)
- [Examples](./examples.md)

❌ Mobile-unfriendly:
- [Complete Getting Started Guide](./getting-started.md)
- [Comprehensive API Documentation](./api.md)
- [Real-World Usage Examples](./examples.md)
```

#### **Touch-Friendly Spacing**
Consider spacing in navigation elements:
```markdown
## Quick Navigation

[Getting Started](./start.md) • [Guides](./guides.md) • [API](./api.md) • [Examples](./examples.md)
```

## ✅ Navigation Quality Standards

### Usability Tests

#### **Navigation Scenarios**
Test common user paths:
- [ ] New user can find getting started
- [ ] Developer can find API reference
- [ ] User can find examples for their use case
- [ ] User can get back to where they started
- [ ] Search returns relevant results

#### **Link Quality**
Verify all navigation elements:
- [ ] All links work (no 404s)
- [ ] Link text describes destination
- [ ] Internal links use relative paths
- [ ] External links open appropriately
- [ ] Mobile navigation is usable

### Maintenance Standards

#### **Regular Reviews**
- **Monthly**: Check for broken links
- **Quarterly**: Review navigation paths
- **On releases**: Update version-specific links
- **On restructuring**: Update all affected navigation

#### **Analytics Integration**
Track navigation effectiveness:
- Most common paths
- Exit points
- Search queries
- Mobile usage patterns

---

**Remember**: Good navigation is invisible to users - they can find what they need without thinking about how to get there. Poor navigation makes every task harder.