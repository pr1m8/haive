# Claude Memory System - Haive Project
**Purpose**: Organized knowledge base for Claude Code sessions  
**Maintained**: Continuously updated across conversations  
**Usage**: Reference for context, decisions, and solutions

## 📁 **Memory Organization Structure**

```
claude_memory/
├── README.md                    # This index file
├── navigation/                  # Documentation navigation & structure
│   ├── hierarchy_design.md     # New haive-root navigation system
│   ├── sidebar_issues.md       # Sidebar depth, contextual nav problems  
│   └── url_patterns.md         # URL structure decisions (/api/haive/*)
├── build_system/               # Sphinx, build configs, performance
│   ├── critical_issues.md      # Build failures, template errors
│   ├── conf_analysis.md        # Configuration problems & solutions
│   └── autobuild_setup.md      # Sphinx-autobuild configuration
├── ui_design/                  # Visual design, CSS, showcase styling
│   ├── showcase_css.md         # Beautiful gradient cards implementation
│   ├── old_vs_new_ui.md        # UI comparison and preferences
│   └── responsive_design.md    # Mobile, accessibility considerations
├── architecture/               # Code structure, patterns, decisions
│   ├── readme_conversion.md    # README → __init__.py docstring strategy
│   ├── api_structure.md        # Three-tier API documentation system
│   └── schema_patterns.md      # Documentation schema patterns
├── troubleshooting/            # Common problems and solutions
│   ├── build_failures.md       # Template errors, dependency issues
│   ├── performance_issues.md   # Slow builds, discovered_readmes bloat
│   └── quick_fixes.md          # Fast solutions for common problems
└── decisions/                  # Design decisions and rationale
    ├── navigation_philosophy.md # Why hierarchical over flat
    ├── css_approach.md         # Showcase vs custom styling decisions
    └── content_strategy.md     # Manual vs autosummary balance
```

## 🎯 **How This System Works**

### **For Claude**:
- **Context Retention**: Key decisions and patterns preserved across sessions
- **Problem Solving**: Reference previous solutions and avoid repeated work
- **Pattern Recognition**: Build on established patterns and architectures
- **Progress Tracking**: Understand what's been tried, what works, what doesn't

### **For User**:
- **Knowledge Base**: Complete documentation of system evolution
- **Decision History**: Why choices were made, alternatives considered
- **Troubleshooting Guide**: Quick reference for fixing common issues
- **Onboarding**: New team members can understand system quickly

## 📋 **Memory Update Protocol**

### **After Each Session**:
1. **Update relevant memory files** with new insights
2. **Create new memory files** for new problem areas  
3. **Cross-reference** related decisions and solutions
4. **Archive outdated** information to prevent confusion

### **Before Each Session**:
1. **Review relevant memory files** for context
2. **Check decision history** to understand constraints
3. **Reference troubleshooting** for known issues
4. **Update progress tracking** based on session goals

## 🔗 **Cross-References**

### **Current Active Areas**:
- **Navigation**: `navigation/hierarchy_design.md` ← Primary focus
- **Build Issues**: `build_system/critical_issues.md` ← Urgent fixes needed
- **UI Enhancement**: `ui_design/showcase_css.md` ← Ready to implement

### **Pending Work**:
- **README Conversion**: `architecture/readme_conversion.md` ← 289 files planned
- **Performance**: `troubleshooting/performance_issues.md` ← 4.9MB bloat to fix

## 💡 **Quick Access by Topic**

| Need | Memory File | Quick Description |
|------|-------------|-------------------|
| Fix broken build | `troubleshooting/build_failures.md` | Template errors, conf.py issues |
| Apply beautiful UI | `ui_design/showcase_css.md` | Gradient cards, animations |
| Understand nav structure | `navigation/hierarchy_design.md` | Haive-root pattern, URL design |
| See what was tried | `decisions/navigation_philosophy.md` | Why current approach chosen |
| Fix performance | `troubleshooting/performance_issues.md` | Discovered READMEs, build speed |

## 🎨 **Visual Status Indicators**

- 🟢 **Complete**: Fully implemented and working
- 🟡 **In Progress**: Partially implemented, needs completion  
- 🔴 **Blocked**: Issues preventing progress
- 🔵 **Planned**: Designed but not started
- ⚪ **Archived**: No longer relevant

---

**Last Updated**: January 7, 2025  
**Current Focus**: Build system fixes and navigation enhancement  
**Next Priority**: README conversion and performance optimization