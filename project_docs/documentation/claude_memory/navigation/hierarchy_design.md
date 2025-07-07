# Navigation Hierarchy Design 🗺️
**Status**: 🟡 In Progress  
**Last Updated**: January 7, 2025  
**Session ID**: navigation_restructure_20250107

## 🎯 **Core Design Philosophy**

**User Request**: "haive as root - package names next sub dir, then all other subdirs be module based and repeat the pattern"

**Implementation**: Hierarchical navigation with consistent pattern at every level

## 📐 **URL Structure**

### **Pattern**:
```
/api/haive/                          # Root level
├── {package}/                       # Package level (core, agents, tools)
│   ├── {module}/                    # Module level (engine, schema, simple)
│   │   ├── {submodule}.html         # Submodule level (base, aug_llm)
│   │   └── index.html               # Module overview
│   └── index.html                   # Package overview
└── index.html                       # Main API overview
```

### **Examples**:
```
✅ /api/haive/index.html                    # Main API hub
✅ /api/haive/core/index.html               # Core package overview  
✅ /api/haive/core/engine/index.html        # Engine module overview
✅ /api/haive/core/engine/base.html         # Base submodule docs
✅ /api/haive/agents/simple/structured.html # Agent implementation
```

## 🏗️ **Implementation Details**

### **Files Created**:
- `restructure_navigation.py` - Generates complete hierarchy  
- `api/haive/index.rst` - Main entry point with package grid
- `api/haive/core/` - Complete core package structure
- `api/haive/agents/` - Complete agents package structure
- All module and submodule index files

### **Grid Card System**:
```rst
.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: 🏗️ **Haive Core**
      :link: core/index
      :link-type: doc
      
      Core infrastructure and utilities
```

## ✅ **What's Working**

1. **Complete Hierarchy**: All packages, modules, submodules mapped
2. **Visual Navigation**: Grid cards at every level for easy browsing
3. **Import Paths**: Clear display of `haive.core.engine.base`
4. **Breadcrumbs**: Navigation context preserved
5. **Auto-generation**: Script can rebuild entire structure

## ⚠️ **Current Issues**

### **Sidebar Overwhelm**
- **Problem**: All 4 levels expanded by default
- **Impact**: Extremely long navigation tree
- **User Feedback**: "can't see the forest for the trees"

### **Content Depth**
- **Problem**: New structure focuses on navigation, loses API detail
- **User Preference**: "preferred the old UI for the schemas"
- **Missing**: Rich autosummary content with class/function listings

### **Build Integration**
- **Problem**: Competing with autosummary and legacy structures
- **Status**: 3 different API documentation systems active

## 🔧 **Planned Improvements**

### **Sidebar Configuration**:
```python
# Target configuration for better UX
html_theme_options = {
    "navigation_depth": 2,  # Only show 2 levels by default
    "auto_expand": False,   # Don't expand all sections
    "show_nav_level": 1,    # Focus on current level
}
```

### **Content Enhancement**:
- Integrate autosummary content into hierarchy
- Add class/function previews in module cards
- Maintain discovery AND reference functionality

## 📊 **Success Metrics**

- ✅ URL pattern implemented correctly
- ✅ Complete hierarchy generated
- ✅ Visual navigation working
- 🟡 Sidebar usability (needs improvement)
- 🟡 Content depth (needs autosummary integration)
- 🔴 Build stability (template errors blocking)

## 🎨 **Visual Design**

### **Current Grid Cards**:
- Clean, minimal styling
- Package icons (🏗️ Core, 🤖 Agents, 🔧 Tools)
- Module descriptions and submodule counts

### **Planned Enhancement**:
- Apply showcase CSS for gradient backgrounds
- Hover animations and glass morphism effects
- Better typography and spacing

## 🔗 **Related Memory Files**

- `../ui_design/showcase_css.md` - Visual enhancement plans
- `../build_system/critical_issues.md` - Blocking build problems
- `../troubleshooting/performance_issues.md` - Sidebar performance issues
- `../decisions/navigation_philosophy.md` - Why this approach was chosen

## 📝 **Key Implementation Files**

```
docs/source/api/haive/
├── index.rst                 # Main hub with package grid
├── core/
│   ├── index.rst            # Core package overview
│   ├── engine/
│   │   ├── index.rst        # Engine module overview
│   │   ├── base.rst         # Submodule documentation
│   │   └── aug_llm.rst      # Submodule documentation
│   └── schema/
│       ├── index.rst        # Schema module overview  
│       └── state_schema.rst # Submodule documentation
└── agents/
    ├── index.rst            # Agents package overview
    └── simple/
        ├── index.rst        # Simple module overview
        └── structured.rst   # Submodule documentation
```

---

**Next Steps**: 
1. Fix build system to enable testing
2. Apply showcase CSS for beautiful visuals
3. Integrate autosummary content for depth
4. Optimize sidebar navigation depth