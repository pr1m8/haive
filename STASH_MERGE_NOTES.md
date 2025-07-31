# 📋 STASH MERGE TRACKING NOTES
*Critical updates that tend to get overwritten*

## 🎯 STASH 12 - conf.py Documentation Build Fixes
**Status: PENDING**

### Changes to apply to docs/source/conf.py:

1. **Disable problematic sphinx_gallery:**
   ```python
   # "sphinx_gallery.gen_gallery",  # Temporarily disabled - needs configuration
   ```

2. **Disable problematic AutoAPI options:**
   ```python
   autoapi_options = [
       "members",
       "undoc-members",
       "show-inheritance",
       "show-module-summary",
       # "special-members",  # Disabled to reduce errors
       # "imported-members",  # Disabled to reduce errors
   ]
   ```

3. **Add error tolerance:**
   ```python
   # Configure AutoAPI to continue on errors
   autoapi_fail_on_warning = False
   ```

4. **Add suppress_warnings:**
   ```python
   suppress_warnings = [
       "autoapi.python_import_resolution",
       "autosummary",
       "ref.doc",
       "ref.ref",
   ]
   ```

5. **Update intersphinx mappings:**
   ```python
   intersphinx_mapping = {
       "python": ("https://docs.python.org/3", None),
       "langchain": ("https://api.python.langchain.com/en/latest/", None),
       "pydantic": ("https://docs.pydantic.dev/latest/", None),
   }
   ```

6. **Improve setup function:**
   ```python
   def setup(app):
       # Only connect autoapi events if autoapi is enabled
       if "autoapi.extension" in extensions:
           app.connect("autoapi-skip-member", autoapi_skip_member)
   ```

---

## 🎯 STASH 10 - Enhanced Documentation & Dependencies
**Status: PENDING**

### Changes to apply:

**pyproject.toml:**
- Update: `rich = "^14.1.0"` (from ^13.9.4)
- Add: `taskipy = "^1.14.0"`

**noxfile.py:**
- Enhanced documentation with integration notes
- Adds documentation quality tools integration
- Better session descriptions

**conf.py:**
- Add: `"sphinx.ext.doctest"` - Test code examples
- Add: `"sphinx.ext.coverage"` - Documentation coverage reports
- Add: `"sphinx.ext.todo"` - TODO list generation
- Fix: `"sphinx_tabs.tabs"` - Fixed import path (was "sphinx_tabs")

---

## 📝 TRACKING LOG
- [ ] Stash 12 conf.py changes
- [ ] Stash 10 changes (TBD)
- [ ] Stash 9 changes (TBD)
- [ ] Stash 8 changes (TBD)
- [ ] Stash 7 changes (TBD)
- [ ] Stash 6 changes (TBD)
- [ ] Stash 5 changes (TBD)
- [ ] Stash 3 changes (TBD)
- [ ] Stash 2 changes (TBD)
- [ ] Stash 1 changes (TBD)
- [ ] Stash 0 changes (TBD)

## ⚠️ CRITICAL NOTES
- conf.py gets overwritten frequently - check this file before making changes
- Always verify current state before applying patches
- Dependencies may need to be added via `poetry add` commands
