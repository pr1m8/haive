# Document Loader Migration - Comprehensive Memory Plan

## 🧠 Core Memory - Critical Knowledge to Retain

### Architecture Foundation

1. **Source-Loader-Registry Pattern**: Sources (data models) separate from Loaders (logic)
2. **Path Analysis**: Auto-detection from paths/URLs using PathAnalyzer
3. **Registry System**: Decorator-based registration with `@register_source`
4. **Preference System**: LoaderPreference.SPEED vs QUALITY vs BALANCED
5. **Credential Management**: SecureConfigMixin integration for API keys/auth
6. **Document State Schema**: Must integrate with existing haive schema

### Implementation Strategy

- **231 Total Loaders**: Categorized into 12 major types
- **Bulk/Directory Loaders**: 11 loaders with "scrape all" capabilities
- **Typed Source Hierarchy**: Base classes with proper inheritance
- **Easy Registration**: Simple decorators for quick loader addition

## 📊 Complete Loader Categorization (231 Loaders)

### 1. File-Based Loaders (51 loaders)

**Core Types**: PDF (12 variants), Office docs, Text formats, Code files
**Key Bulk Loaders**: DirectoryLoader, PyPDFDirectoryLoader
**Credentials**: None (local files)

### 2. Web-Based Loaders (19 loaders)

**Core Types**: Web scraping, recursive crawling, documentation sites
**Key Bulk Loaders**: RecursiveUrlLoader, SitemapLoader, FireCrawlLoader
**Credentials**: API keys for scraping services

### 3. Directory & Bulk Loaders (13 loaders)

**Core Types**: File system, cloud storage, concurrent processing
**Key Bulk Loaders**: ALL (this is the bulk category)
**Credentials**: Cloud storage credentials

### 4. Database Loaders (19 loaders)

**Core Types**: SQL, NoSQL, data warehouses, DataFrames
**Key Bulk Loaders**: All database loaders are inherently bulk
**Credentials**: Database connection strings

### 5. Cloud Storage & Services (15 loaders)

**Core Types**: AWS, GCP, Azure, other cloud providers
**Key Bulk Loaders**: S3DirectoryLoader, GCSDirectoryLoader
**Credentials**: Cloud provider credentials

### 6. Messaging & Communication (15 loaders)

**Core Types**: Chat platforms, social media, email
**Key Bulk Loaders**: SlackDirectoryLoader, chat exports
**Credentials**: OAuth tokens, API keys

### 7. CRM & Business Systems (14 loaders)

**Core Types**: Airbyte connectors, business tools
**Key Bulk Loaders**: Airbyte bulk data connectors
**Credentials**: Business platform API keys

### 8. Academic & Research (10 loaders)

**Core Types**: Research papers, educational platforms
**Key Bulk Loaders**: Dataset loaders (HuggingFace, TensorFlow)
**Credentials**: API keys for academic platforms

### 9. Note-Taking & Knowledge Management (9 loaders)

**Core Types**: Personal/team knowledge systems
**Key Bulk Loaders**: NotionDirectoryLoader, workspace exports
**Credentials**: Platform API keys

### 10. Media & Content (8 loaders)

**Core Types**: Video, audio, entertainment platforms
**Key Bulk Loaders**: YouTube channel loaders
**Credentials**: Platform API keys

### 11. Development & Version Control (5 loaders)

**Core Types**: Git, GitHub, documentation
**Key Bulk Loaders**: Git repository loaders
**Credentials**: Git tokens, SSH keys

### 12. Specialized & Domain-Specific (20 loaders)

**Core Types**: Blockchain, geographic, enterprise analytics
**Key Bulk Loaders**: Specialized bulk data processors
**Credentials**: Domain-specific API keys

## 🎯 Implementation Priority

### Phase 1: Core Foundation (Essential)

1. **File-Based Sources** (PDF, CSV, JSON, Text, Word, Excel)
2. **Web Sources** (URLs, HTML, recursive crawling)
3. **Directory Sources** (local directories, bulk processing)
4. **Database Sources** (SQL, PostgreSQL, MongoDB)

### Phase 2: Cloud & Enterprise (High Value)

1. **Cloud Storage** (S3, GCS, Azure Blob)
2. **Business Systems** (Slack, Confluence, Google Drive)
3. **Note-Taking** (Notion, Obsidian)
4. **Academic** (arXiv, Wikipedia)

### Phase 3: Specialized (Nice to Have)

1. **Social Media** (Twitter, Reddit)
2. **Media Platforms** (YouTube, audio)
3. **Development** (GitHub, Git)
4. **Domain-Specific** (blockchain, geographic)

## 🏗️ Technical Implementation Plan

### Source Type Hierarchy

```python
# Base source types
BaseSource
├── LocalSource (files, directories)
├── RemoteSource (URLs, APIs)
├── DatabaseSource (SQL, NoSQL)
├── CloudStorageSource (S3, GCS, Azure)
├── MessageSource (chat, email)
├── BusinessSource (CRM, productivity)
├── MediaSource (video, audio)
├── CodeSource (git, repositories)
└── SpecializedSource (domain-specific)
```

### Bulk Loading Capabilities

```python
# Distinguish bulk vs single loaders
class SourceCapabilities:
    is_bulk_loader: bool
    supports_recursive: bool
    supports_filtering: bool
    requires_credentials: bool
    credential_type: CredentialType
```

### Easy Registration System

```python
@register_source(
    name="pdf_advanced",
    category=SourceCategory.FILE_DOCUMENT,
    file_extensions=[".pdf"],
    capabilities=["bulk", "recursive", "quality_extraction"],
    loaders={
        "fast": "PyPDFLoader",
        "quality": "UnstructuredPDFLoader",
        "advanced": "MathpixPDFLoader"
    },
    credential_requirements=["mathpix_api_key"]
)
class AdvancedPDFSource(LocalSource):
    pass
```

## 🔧 Critical Implementation Details

### Document State Schema Integration

- Must use existing DocumentInput/DocumentOutput from haive schema
- State persistence with Supabase auto-detection
- Conversation thread tracking with document context

### Testing Strategy

```bash
# Test individual components
poetry run pytest packages/haive-core/tests/engines/document/test_sources/
poetry run pytest packages/haive-core/tests/engines/document/test_loaders/
poetry run pytest packages/haive-core/tests/engines/document/test_registry/

# Test integration
poetry run pytest packages/haive-core/tests/engines/document/test_integration/
```

### Memory Triggers for Context Switching

When I need to compact/summarize, remember:

1. **231 total loaders in 12 categories**
2. **Source-Loader-Registry pattern with decorators**
3. **Path analysis auto-detection is CRITICAL**
4. **11 bulk loaders for "scrape all" functionality**
5. **SecureConfigMixin for credentials**
6. **Integration with DocumentInput/DocumentOutput schema**

## 🚨 Critical Success Factors

1. **Auto-detection must work perfectly** - PathAnalyzer is key
2. **Easy registration** - Developers must be able to add loaders quickly
3. **Proper typing** - Full type safety for all source variations
4. **Credential security** - SecureConfigMixin integration
5. **Schema integration** - Document state schema compatibility
6. **Bulk processing** - Support for "fetch all" scenarios
7. **Testing coverage** - Comprehensive test suite

## 📝 Next Steps Tracking

- [ ] Create comprehensive source type system
- [ ] Implement Phase 1 loaders (20 essential loaders)
- [ ] Create bulk loading capabilities
- [ ] Integrate document state schema
- [ ] Comprehensive testing
- [ ] Performance optimization
- [ ] Documentation and examples
