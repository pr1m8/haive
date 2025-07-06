# Memory Management & Context Preservation Plan

## 🧠 **Critical Knowledge - Never Forget**

### **Core Architecture Pattern**

```
Source-Loader-Registry Pattern:
PathAnalyzer → EnhancedRegistry → SourceFactory → LangChainLoader → DocumentEngine
```

### **Essential Numbers & Progress**

- **231 Total Loaders**: All langchain_community loaders supported
- **60+ Implemented**: Current implementation count (Phases 1-4 complete)
- **11 Bulk Loaders**: "Scrape all" recursive processing capability
- **12 Categories**: Complete source categorization
- **10 Workers**: Maximum concurrent processing

### **Phases Completed**

- ✅ **Phase 1**: Essential Sources (13 loaders) - @20_PHASE1_ESSENTIAL
- ✅ **Phase 2**: File System (25+ loaders) - @21_PHASE2_FILE_SYSTEM
- ✅ **Phase 3**: Bulk Loading (12+ loaders) - @22_PHASE3_BULK_LOADING
- ✅ **Phase 4**: Web Loaders (11+ loaders) - @23_PHASE4_WEB_LOADERS
- ✅ **Phase 5**: Database Loaders (9+ loaders) - @24_PHASE5_DATABASES
- ✅ **Phase 6**: Messaging & Social (15+ loaders) - @25_PHASE6_MESSAGING

### **Key Implementation Files**

```
/packages/haive-core/src/haive/core/engine/document/loaders/
├── path_analyzer.py          # Auto-detection from paths
├── sources/
│   ├── source_types.py       # 23 typed source categories
│   ├── enhanced_registry.py  # Decorator registration system
│   ├── essential_sources.py  # Phase 1: Core 13 loaders
│   ├── file_sources.py       # Phase 2: File system 25+ loaders
│   ├── bulk_sources.py       # Phase 3: Bulk loading 12+ loaders
│   ├── web_sources.py        # Phase 4: Web loaders 11+ loaders
│   ├── database_sources.py   # Phase 5: Database loaders 9+ loaders
│   └── messaging_sources.py  # Phase 6: Messaging & social 15+ loaders
```

---

## 📋 **Context Switching Reminders**

### **Current Status: Phase 6 COMPLETE - Moving to Phase 7**

1. **Completed**: Messaging & Social Media Sources (15+ loaders from langchain_community)
2. **Focus**: Business & CRM integrations, productivity tools, enterprise platforms
3. **Testing**: Multi-platform integration and API authentication
4. **Schema**: Complete messaging metadata and content type tracking

### **Coding Style Compliance (Updated)**

- ✅ **Follow @/project_docs/CODING_STYLE_GUIDE.md**: PEP 8, 88-char lines, type hints
- ✅ **Module Size**: <500 lines per file (current largest: web_sources.py ~600 lines)
- ✅ **Documentation**: Google-style docstrings with Args/Returns/Examples
- ✅ **Error Handling**: Specific exceptions with context
- ✅ **Type Safety**: Full Pydantic validation everywhere

### **Architecture Decisions Made**

- ✅ Pydantic models with SecureConfigMixin for credentials
- ✅ Path analysis for auto-source detection
- ✅ Enhanced registry with capability indexing
- ✅ Document state schema integration
- ✅ Decorator-based easy registration
- ✅ Concurrent bulk processing up to 10 workers
- ✅ Legacy web loader integration (sitemap detection)

### **Implementation Patterns**

```python
@register_database_source(
    name="postgresql",
    database_type="postgresql",
    loaders={"sql": "SQLDatabaseLoader"},
    schemes=["postgresql", "postgres"],
    capabilities=[LoaderCapability.BULK_LOADING]
)
class PostgreSQLSource(DatabaseSource):
    connection_string: str
    table_name: Optional[str] = None
    query: Optional[str] = None
```

---

## 🎯 **Next Phases After Messaging**

### **Phase 7: Business & CRM** (14+ loaders) - NEXT

- Airbyte connectors, HubSpot, Salesforce, Shopify
- Productivity tools, business platform APIs, CRM systems
- Enterprise workflow and automation platforms

### **Phase 8: Specialized** (20+ loaders)

- Academic (arXiv, PubMed), Media (YouTube, audio)
- Development (GitHub, Git), Domain-specific systems
- Scientific data, research databases, specialized APIs

---

## 🔧 **Technical Context**

### **Import Issues Solution**

- Use direct module imports to avoid cascading dependencies
- Test modules in isolation using `import_module_from_file`
- Registry auto-registers sources on import

### **SecureConfigMixin Requirements**

- All remote sources need `provider` and `api_key` fields
- Add `Config.arbitrary_types_allowed = True` to avoid validation errors
- Database sources use `connection_string` instead of `api_key`

### **Document State Integration**

- Enhanced schema supports both documents and source_paths input
- Progress tracking with DocumentLoadingStatus enum
- Source metadata tracking with DocumentSourceInfo
- **NEW**: Database connection metadata and query tracking

---

## 🎯 **Database Loader Implementation Plan**

### **Connection String Auto-Detection**

```python
# Auto-detect database type from connection strings
connection_patterns = {
    "postgresql://": "postgresql",
    "mongodb://": "mongodb",
    "neo4j://": "neo4j",
    "cassandra://": "cassandra",
    "sqlite:///": "sqlite"
}
```

### **Graph Database Support**

- **Neo4j**: Cypher query support, relationship traversal
- **ArangoDB**: Multi-model graph capabilities
- **TigerGraph**: Enterprise graph analytics
- **Amazon Neptune**: Cloud graph database

### **Data Warehouse Integration**

- **BigQuery**: Google Cloud analytics
- **Snowflake**: Cloud data warehouse
- **Redshift**: AWS data warehouse
- **Databricks**: Unified analytics platform

---

_Reference: @00_DOCUMENT_LOADER_INDEX for navigation_  
_Current: Phase 5 Database Loaders implementation_  
_Next: @25_PHASE6_MESSAGING for messaging and social sources_
