# Alternative Documentation Tools Evaluation

**Created**: 2025-01-27
**Purpose**: Evaluate alternatives to Sphinx for Haive's namespace monorepo

## Current Pain Points with Sphinx

1. **Namespace Package Issues**
   - AutoAPI struggles with PEP 420 namespaces
   - Path resolution includes 'src' in imports
   - Complex workarounds needed

2. **Monorepo Challenges**
   - Designed for single package documentation
   - No native monorepo support
   - Requires extensive configuration

3. **API Structure Problems**
   - Deeply nested directory structure
   - Confusing URLs
   - Poor navigation

4. **Build Complexity**
   - 6,802 errors currently
   - Slow builds
   - Difficult debugging

## Alternative Tools Analysis

### 1. MkDocs Material + mkdocstrings

**Pros**:

- ✅ **Native monorepo support** - Designed for complex projects
- ✅ **Modern UI** - Material Design, mobile-friendly
- ✅ **Markdown-first** - Easier to write and maintain
- ✅ **Better search** - Built-in advanced search
- ✅ **Fast builds** - Incremental builds by default
- ✅ **Easy configuration** - YAML-based, simple

**Cons**:

- ❌ Less mature than Sphinx
- ❌ Fewer extensions
- ❌ Different theming system

**Configuration Example**:

```yaml
# mkdocs.yml
site_name: Haive Documentation
theme:
  name: material
  features:
    - navigation.instant
    - navigation.sections
    - search.suggest

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [packages/haive-core/src, packages/haive-agents/src]
          options:
            show_source: true
            show_bases: true

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - API Reference:
      - Core: api/core.md
      - Agents: api/agents.md
```

**Handling Namespaces**:

```python
# mkdocstrings automatically handles namespace packages
::: haive.agents.simple
::: haive.core.engine
```

### 2. pdoc3

**Pros**:

- ✅ **Simple setup** - Works out of the box
- ✅ **Good namespace handling** - Understands PEP 420
- ✅ **Fast** - Minimal processing
- ✅ **Clean output** - Modern HTML

**Cons**:

- ❌ Limited customization
- ❌ No narrative documentation
- ❌ API-only focus

**Command**:

```bash
pdoc --html --output-dir docs/api \
  packages/haive-core/src/haive \
  packages/haive-agents/src/haive
```

### 3. Pydoctor

**Pros**:

- ✅ **Complex codebase support** - Built for Twisted
- ✅ **Good cross-referencing** - Understands relationships
- ✅ **Incremental builds** - Fast updates

**Cons**:

- ❌ Less popular
- ❌ Older UI design
- ❌ Limited themes

**Configuration**:

```ini
# pydoctor.ini
[pydoctor]
project-name = Haive
project-url = https://haive.ai
docformat = google
make-html = true
add-package = packages/haive-core/src/haive
add-package = packages/haive-agents/src/haive
```

### 4. Docusaurus

**Pros**:

- ✅ **Modern React-based** - Highly customizable
- ✅ **Great for mixed content** - Docs + blog + showcase
- ✅ **Versioning built-in** - Multiple versions
- ✅ **MDX support** - React components in docs

**Cons**:

- ❌ JavaScript/React knowledge needed
- ❌ No native Python API generation
- ❌ More complex setup

### 5. Read the Docs with Custom Build

**Pros**:

- ✅ **Hosting included** - Free for open source
- ✅ **Version management** - Automatic from Git
- ✅ **Search** - Built-in search
- ✅ **Analytics** - Usage statistics

**Cons**:

- ❌ Still using Sphinx underneath
- ❌ Same configuration challenges

## Comparison Matrix

| Feature           | Sphinx       | MkDocs Material | pdoc3        | Pydoctor    | Docusaurus   |
| ----------------- | ------------ | --------------- | ------------ | ----------- | ------------ |
| Namespace Support | ❌ Poor      | ✅ Good         | ✅ Good      | ✅ Good     | ⚠️ Manual    |
| Monorepo Support  | ❌ Poor      | ✅ Excellent    | ⚠️ Basic     | ⚠️ Basic    | ✅ Good      |
| Setup Complexity  | ❌ High      | ✅ Low          | ✅ Very Low  | ✅ Low      | ⚠️ Medium    |
| Customization     | ✅ Extensive | ✅ Good         | ❌ Limited   | ⚠️ Basic    | ✅ Extensive |
| Build Speed       | ❌ Slow      | ✅ Fast         | ✅ Very Fast | ✅ Fast     | ✅ Fast      |
| Modern UI         | ⚠️ Depends   | ✅ Excellent    | ✅ Good      | ❌ Dated    | ✅ Excellent |
| API Generation    | ✅ AutoAPI   | ✅ mkdocstrings | ✅ Built-in  | ✅ Built-in | ❌ Manual    |
| Learning Curve    | ❌ Steep     | ✅ Gentle       | ✅ Minimal   | ✅ Gentle   | ⚠️ Medium    |

## Recommendation for Haive

### Immediate (Fix Current Issues)

Continue with Sphinx but:

1. Implement phased approach
2. Use aggressive filtering
3. Consider simpler structure

### Short-term (3-6 months)

**Evaluate MkDocs Material** as primary alternative:

1. Set up proof of concept
2. Test with one package
3. Compare build times and output
4. Assess migration effort

### Long-term (6-12 months)

If MkDocs proves successful:

1. Migrate incrementally
2. Start with new documentation
3. Port existing content gradually
4. Maintain both during transition

## Migration Strategy to MkDocs

### Phase 1: Proof of Concept

```bash
# Install
pip install mkdocs-material mkdocstrings[python]

# Create structure
mkdocs new haive-docs
cd haive-docs

# Configure
# Edit mkdocs.yml as shown above

# Test
mkdocs serve
```

### Phase 2: Single Package

1. Document haive-core only
2. Compare with Sphinx output
3. Test cross-references
4. Measure build time

### Phase 3: Full Migration

1. Port all packages
2. Migrate narrative docs
3. Set up CI/CD
4. Deploy to production

## Cost-Benefit Analysis

### Staying with Sphinx

**Costs**:

- Continued configuration complexity
- Slow builds
- Poor namespace support
- High maintenance

**Benefits**:

- No migration needed
- Mature ecosystem
- Team knowledge

### Switching to MkDocs

**Costs**:

- Migration effort (est. 2-4 weeks)
- Learning curve
- Some features may differ

**Benefits**:

- Better monorepo support
- Faster builds
- Modern UI
- Easier maintenance
- Better developer experience

## Decision Criteria

Switch if:

- [ ] Current issues persist after fixes
- [ ] Build times remain > 2 minutes
- [ ] Navigation remains confusing
- [ ] Team spends > 20% time on doc builds

Stay if:

- [ ] Phased approach succeeds
- [ ] Build times become acceptable
- [ ] Team is satisfied with output
- [ ] Migration cost too high

## Next Steps

1. **Complete Sphinx fix attempt** (1-2 weeks)
2. **Create MkDocs PoC** (2-3 days)
3. **Compare outputs** (1 day)
4. **Make decision** (team discussion)
5. **Execute choice** (2-4 weeks)

## Resources

- [MkDocs Material Documentation](https://squidfunk.github.io/mkdocs-material/)
- [mkdocstrings](https://mkdocstrings.github.io/)
- [MkDocs Monorepo Plugin](https://github.com/backstage/mkdocs-monorepo-plugin)
- [pdoc3 Documentation](https://pdoc3.github.io/pdoc/)
- [Pydoctor](https://github.com/twisted/pydoctor)
