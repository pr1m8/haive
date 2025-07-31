# Claude Memory Documentation System 🧠

**Location**: `project_docs/documentation/claude_memory/`
**Purpose**: Persistent knowledge base for Claude Code sessions
**Access**: Always available across conversations for context and continuity

## 📂 **Memory Organization**

```
project_docs/documentation/claude_memory/
├── index.md                           # This memory system index
├── navigation/                        # Documentation navigation systems
│   ├── hierarchy_design.md           # Haive-root navigation structure
│   ├── sidebar_optimization.md       # Sidebar depth and UX issues
│   ├── url_patterns.md              # URL design patterns and decisions
│   └── contextual_navigation.md      # JavaScript navigation enhancements
├── build_system/                     # Sphinx build configuration and issues
│   ├── critical_issues.md           # Build failures and urgent fixes
│   ├── conf_analysis.md             # Configuration complexity and cleanup
│   ├── autobuild_management.md      # Sphinx-autobuild setup and monitoring
│   └── performance_optimization.md   # Build speed and resource issues
├── ui_design/                        # Visual design and styling
│   ├── showcase_css_implementation.md # Gradient cards and animations
│   ├── design_system.md             # Color schemes, typography, spacing
│   ├── responsive_behavior.md        # Mobile and accessibility
│   └── user_feedback.md             # UI preferences and iterations
├── architecture/                     # Code structure and patterns
│   ├── readme_conversion_strategy.md # 289 README → docstring conversion
│   ├── api_documentation_layers.md   # Three-tier doc system integration
│   ├── schema_composition.md         # Documentation schema patterns
│   └── package_organization.md       # Monorepo structure understanding
├── troubleshooting/                  # Problem diagnosis and solutions
│   ├── build_failures.md            # Template errors, dependency issues
│   ├── performance_bottlenecks.md    # Slow builds, discovered_readmes
│   ├── navigation_bugs.md            # Sidebar issues, link problems
│   └── quick_reference.md            # Fast fixes for common problems
└── decisions/                        # Design decisions and rationale
    ├── navigation_philosophy.md      # Why hierarchical over flat structure
    ├── css_strategy.md              # Showcase vs custom styling approach
    ├── content_organization.md       # Manual vs autosummary balance
    └── tool_choices.md              # Sphinx, Furo, extensions chosen
```

## 🎯 **Claude Usage Protocol**

### **Session Startup** (Auto-Reference):

1. 📖 **Read current session context** from relevant memory files
2. 🔍 **Check decision history** to understand constraints and past attempts
3. 📋 **Review troubleshooting** for known issues and solutions
4. 🎯 **Identify session focus** from user requests and current status

### **During Work** (Continuous Updates):

1. 🧠 **Mental note-taking**: Track new insights and patterns discovered
2. 🔄 **Cross-reference**: Link new work to existing memory files
3. ⚠️ **Problem documentation**: Record issues encountered and solutions attempted
4. 💡 **Decision logging**: Capture why choices were made over alternatives

### **Session End** (Memory Persistence):

1. 📝 **Update memory files** with new knowledge and insights
2. 🆕 **Create new files** for new problem areas or solutions discovered
3. 🔗 **Cross-link** related concepts and reference between files
4. 📊 **Status updates** on progress, blockers, and next steps

## 🔄 **Current Session Context**

### **Active Focus Areas**:

- **🔴 CRITICAL**: Build system failures (template errors, conf.py bloat)
- **🟡 IN PROGRESS**: Navigation hierarchy implementation
- **🔵 PLANNED**: Showcase UI application and README conversion

### **Session History**:

- **Previous**: Navigation restructure, URL pattern implementation
- **Current**: Build system diagnosis, critical issue identification
- **Next**: Template fixes, configuration cleanup, UI enhancement

### **Key Decisions Made**:

- ✅ Hierarchical navigation with haive as root
- ✅ Three-tier API documentation system
- ✅ Showcase CSS for gradient card styling
- 🟡 README → docstring conversion strategy (planned)

## 📊 **Memory File Status**

| Area            | Status      | Last Updated | Next Action             |
| --------------- | ----------- | ------------ | ----------------------- |
| Navigation      | 🟡 Partial  | 2025-01-07   | Fix build, apply UI     |
| Build System    | 🔴 Critical | 2025-01-07   | Template fix, cleanup   |
| UI Design       | 🔵 Ready    | 2025-01-07   | Apply showcase CSS      |
| Architecture    | 🔵 Planned  | 2025-01-07   | Start README conversion |
| Troubleshooting | 🟢 Active   | 2025-01-07   | Ongoing updates         |

---

**Memory System Version**: 1.0
**Initialized**: January 7, 2025
**Location**: `project_docs/documentation/claude_memory/`
**Access Pattern**: Always read relevant files at session start
