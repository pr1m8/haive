# Organization Standards

Guidelines for organizing and structuring documentation across the Haive project.

## 📁 Contents

- [hierarchy.md](hierarchy.md) - Documentation hierarchy and structure
- [naming-conventions.md](naming-conventions.md) - File and folder naming standards
- [navigation.md](navigation.md) - Cross-references and linking strategies
- [maintenance.md](maintenance.md) - Keeping documentation up-to-date

## 🎯 Core Principles

### 1. **Predictable Structure**
Users should be able to predict where information is located based on consistent organizational patterns.

### 2. **Logical Hierarchy**
Information should be organized from general to specific, with clear parent-child relationships.

### 3. **Findable Content**
Every piece of information should be discoverable through multiple paths - navigation, search, and cross-references.

### 4. **Maintainable Organization**
The structure should be sustainable as the project grows and evolves.

## 📋 Quick Reference

### Documentation Hierarchy
```
docs/
├── source/           # Sphinx-generated user documentation
├── project_docs/     # Developer and project documentation
└── packages/*/       # Package-specific documentation
```

### Naming Conventions
- **Files**: `kebab-case.md` (lowercase with hyphens)
- **Folders**: `kebab-case/` (lowercase with hyphens)
- **Assets**: `descriptive-name.png` (descriptive, lowercase)

### Cross-Reference Standards
- **Internal links**: Relative paths `../path/to/file.md`
- **Section links**: Anchor format `#section-header`
- **External links**: Full URLs with descriptive text

### Maintenance Guidelines
- **Review cycle**: Quarterly documentation review
- **Update triggers**: Code changes, feature additions, API changes
- **Ownership**: Clear responsibility for each documentation area

## 🔗 Related Resources

- [Writing Guidelines](../writing-guidelines/) - How to write documentation
- [Content Types](../content-types/) - Different documentation formats
- [Quality Assurance](../quality-assurance/) - Review and validation processes

---

**Remember**: Good organization makes information accessible. Poor organization makes even great content unusable.