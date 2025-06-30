# Naming Conventions

Standardized naming rules for files, folders, and documentation elements in the Haive project.

## 📂 File and Folder Naming

### General Rules

#### **Case Style: kebab-case**
All files and folders use lowercase letters with hyphens:

```
✅ Good:
getting-started.md
api-reference/
configuration-guide.md
agent-showcase/

❌ Bad:
GettingStarted.md
API_Reference/
configurationGuide.md
Agent Showcase/
```

#### **Descriptive Names**
Names should clearly indicate content:

```
✅ Good:
installation-guide.md
troubleshooting-agents.md
deployment-checklist.md

❌ Bad:
guide.md
problems.md
deploy.md
```

#### **Length Guidelines**
- **Minimum**: 3 characters
- **Optimal**: 8-25 characters
- **Maximum**: 50 characters

### File Naming Patterns

#### **Documentation Files (.md)**
```
{topic}-{type}.md

Examples:
agent-overview.md
tool-configuration.md
api-reference.md
getting-started.md
```

#### **Index Files**
```
README.md          # Folder overview (preferred)
index.md           # Alternative index file
{topic}-index.md   # Specific index files
```

#### **Configuration Files**
```
.{tool}rc          # Tool configuration
{name}.config.js   # JavaScript config
{name}.yaml        # YAML configuration
```

### Folder Naming Patterns

#### **Content Categories**
```
getting-started/   # User journey stage
user-guides/       # Content type
api-reference/     # Content type
examples/          # Content type
```

#### **Domain Areas**
```
agents/           # Feature domain
tools/            # Feature domain
games/            # Module domain
deployment/       # Activity domain
```

#### **Support Folders**
```
images/           # Media assets
assets/           # Static resources
templates/        # Reusable templates
```

## 🏷️ Content Naming

### Page Titles

#### **Capitalization: Sentence case**
```
✅ Good:
# Getting started with agents
# API reference guide
# Troubleshooting common issues

❌ Bad:
# Getting Started With Agents
# API Reference Guide  
# Troubleshooting Common Issues
```

#### **Structure Patterns**
```
{Action} {Object}        # Creating agents
{Object} {Type}          # Agent configuration
{Process} guide          # Installation guide
{Topic} overview         # Tools overview
```

### Section Headers

#### **Descriptive Headers**
```
✅ Good:
## Installing the core package
## Configuring agent tools
## Handling authentication errors

❌ Bad:
## Installation
## Configuration
## Errors
```

#### **Parallel Structure**
Keep similar sections consistent:

```
✅ Good:
## Creating simple agents
## Creating complex agents
## Creating specialized agents

❌ Bad:
## Creating simple agents
## Complex agent creation
## How to make specialized agents
```

## 🔗 Link and Anchor Naming

### Internal Links

#### **Descriptive Link Text**
```
✅ Good:
[agent configuration guide](../guides/agent-config.md)
[tool installation instructions](./tool-setup.md)

❌ Bad:
[click here](../guides/agent-config.md)
[see this](./tool-setup.md)
```

#### **Relative Path Standards**
```
../              # Parent directory
./               # Current directory
../../           # Grandparent directory
/absolute/path   # Avoid absolute paths
```

### Anchor Links

#### **Header Anchors**
Generated automatically from headers:

```markdown
## Installing the Core Package
<!-- Anchor: #installing-the-core-package -->

## API Reference Guide
<!-- Anchor: #api-reference-guide -->
```

#### **Custom Anchors**
Use for non-header references:

```markdown
<a id="custom-anchor"></a>
[Link text](#custom-anchor)
```

## 🏗️ Code Element Naming

### Code Blocks

#### **Language Specification**
Always specify the language:

```markdown
✅ Good:
```python
def create_agent():
    pass
```

```bash
poetry install
```

❌ Bad:
```
def create_agent():
    pass
```
```

#### **Filename Annotations**
For complex examples:

```markdown
```python
# File: src/agents/simple.py
class SimpleAgent:
    pass
```
```

### Variable Examples

#### **Placeholder Naming**
Use descriptive placeholders:

```
✅ Good:
your_api_key
agent_name
config_file_path

❌ Bad:
xxx
placeholder
value
```

#### **Example Values**
Use realistic examples:

```
✅ Good:
api_key="sk-1234567890abcdef"
agent_name="research_assistant"
temperature=0.7

❌ Bad:
api_key="your_key_here"
agent_name="agent"
temperature=0.5
```

## 🎨 Asset Naming

### Images and Media

#### **Descriptive Names**
```
✅ Good:
agent-workflow-diagram.svg
tool-configuration-screenshot.png
api-response-example.json

❌ Bad:
image1.png
screenshot.png
example.json
```

#### **Naming Pattern**
```
{description}-{type}.{extension}

Examples:
agent-creation-flow.svg
error-message-example.png
configuration-yaml-sample.yaml
```

### Asset Organization
```
assets/
├── images/
│   ├── diagrams/
│   ├── screenshots/
│   └── icons/
├── examples/
│   ├── configuration/
│   └── code/
└── templates/
    ├── agents/
    └── tools/
```

## 🏷️ Taxonomy and Tags

### Category Names

#### **Standard Categories**
```
Getting Started
User Guides
API Reference
Examples
Troubleshooting
```

#### **Domain Categories**
```
Agents
Tools
Games
Core
Deployment
```

### Tag Conventions

#### **Format**
```
{category}:{subcategory}

Examples:
guide:installation
api:agents
example:simple
tutorial:beginner
```

#### **Common Tags**
```
difficulty:beginner
difficulty:intermediate
difficulty:advanced

type:tutorial
type:guide
type:reference
type:example

domain:agents
domain:tools
domain:games
```

## ✅ Validation Rules

### Naming Checklist
- [ ] Uses kebab-case for files and folders
- [ ] Descriptive and specific
- [ ] Consistent with existing patterns
- [ ] No spaces in file names
- [ ] No special characters except hyphens
- [ ] Reasonable length (8-25 characters)

### Content Checklist
- [ ] Sentence case for titles
- [ ] Descriptive section headers
- [ ] Parallel structure maintained
- [ ] Link text is descriptive
- [ ] Code blocks specify language
- [ ] Assets have meaningful names

### Quality Standards
- [ ] Names predict content accurately
- [ ] Similar content uses similar naming
- [ ] No abbreviations unless standard
- [ ] URLs are SEO-friendly
- [ ] File names work cross-platform

## 🔧 Tools and Automation

### Naming Validation
```bash
# Check file naming conventions
find . -name "* *" -type f  # Find files with spaces
find . -name "*[A-Z]*" -type f  # Find files with capitals

# Validate markdown headers
grep -r "^#.*[A-Z].*[A-Z]" *.md  # Find title case headers
```

### Renaming Scripts
```bash
# Convert spaces to hyphens
rename 's/ /-/g' *.md

# Convert to lowercase
rename 'y/A-Z/a-z/' *.md
```

### Link Validation
```bash
# Check for broken internal links
markdown-link-check *.md

# Validate anchor links
grep -n "\[.*\](#.*)" *.md
```

---

**Remember**: Consistent naming is invisible when done well and obvious when done poorly. Invest in getting it right from the start.