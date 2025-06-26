# LangChain Document Loader Inventory

This document tracks all document loaders available in `langchain_community.document_loaders` and their integration status in the Haive Framework.

## Loader Categories

We'll categorize loaders by their primary source type:

1. **File-based Loaders**: Local file system documents
2. **Web-based Loaders**: Web pages, APIs, and online content
3. **Database Loaders**: Database connections
4. **Cloud Storage Loaders**: S3, Azure, GCS, etc.
5. **API-based Loaders**: Third-party services and APIs
6. **Application-based Loaders**: Chat apps, email, etc.
7. **Special Format Loaders**: Specific file format handlers

## Implementation Status

- ⬜ Not started
- 🟡 In progress
- ✅ Completed
- 🚫 Will not implement (with reason)

## Document Loaders Inventory

### File-based Loaders

| Loader                         | Status | Special Methods   | Required Dependencies                 | Environment Keys | Notes                    |
| ------------------------------ | ------ | ----------------- | ------------------------------------- | ---------------- | ------------------------ |
| TextLoader                     | ⬜     | -                 | -                                     | -                | Basic text file loader   |
| CSVLoader                      | ⬜     | -                 | pandas (optional)                     | -                | Loads CSV files          |
| PyPDFLoader                    | ⬜     | -                 | pypdf                                 | -                | Basic PDF loader         |
| PDFMinerLoader                 | ⬜     | -                 | pdfminer.six                          | -                | More advanced PDF loader |
| PDFPlumberLoader               | ⬜     | -                 | pdfplumber                            | -                | Good for tables in PDFs  |
| UnstructuredPDFLoader          | ⬜     | -                 | unstructured, pdf2image, pdfminer.six | -                | OCR capability           |
| MathpixPDFLoader               | ⬜     | -                 | mathpix-pdf-to-html                   | MATHPIX_API_KEY  | OCR with Mathpix         |
| PyMuPDFLoader                  | ⬜     | -                 | pymupdf                               | -                | Fast PDF loader          |
| PDFMinerPDFasHTMLLoader        | ⬜     | -                 | pdfminer.six                          | -                | Converts PDF to HTML     |
| OnlinePDFLoader                | ⬜     | -                 | pypdf, requests                       | -                | Downloads and loads PDF  |
| PyPDFium2Loader                | ⬜     | -                 | pypdfium2                             | -                | Uses Google's PDFium     |
| Docx2txtLoader                 | ⬜     | -                 | docx2txt                              | -                | Word documents           |
| UnstructuredWordDocumentLoader | ⬜     | -                 | unstructured                          | -                | Word with more features  |
| UnstructuredExcelLoader        | ⬜     | -                 | unstructured                          | -                | Excel files              |
| UnstructuredHTMLLoader         | ⬜     | -                 | unstructured                          | -                | HTML files               |
| UnstructuredMarkdownLoader     | ⬜     | -                 | unstructured                          | -                | Markdown files           |
| UnstructuredODTLoader          | ⬜     | -                 | unstructured                          | -                | OpenDocument Text        |
| UnstructuredPowerPointLoader   | ⬜     | -                 | unstructured                          | -                | PowerPoint files         |
| UnstructuredEPubLoader         | ⬜     | -                 | unstructured                          | -                | E-book format            |
| UnstructuredRTFLoader          | ⬜     | -                 | unstructured                          | -                | Rich Text Format         |
| UnstructuredRSTLoader          | ⬜     | -                 | unstructured                          | -                | reStructuredText         |
| UnstructuredCSVLoader          | ⬜     | -                 | unstructured                          | -                | CSV with unstructured    |
| UnstructuredTSVLoader          | ⬜     | -                 | unstructured                          | -                | TSV with unstructured    |
| UnstructuredXMLLoader          | ⬜     | -                 | unstructured                          | -                | XML files                |
| UnstructuredOrgModeLoader      | ⬜     | -                 | unstructured                          | -                | Org mode files           |
| UnstructuredImageLoader        | ⬜     | -                 | unstructured, pytesseract             | -                | OCR for images           |
| UnstructuredCHMLoader          | ⬜     | -                 | unstructured                          | -                | Windows Help files       |
| UnstructuredEmailLoader        | ⬜     | -                 | unstructured                          | -                | Email files              |
| BibtexLoader                   | ⬜     | -                 | pybtex                                | -                | BibTeX bibliography      |
| JSONLoader                     | ⬜     | `jq_schema` param | jq (optional)                         | -                | JSON with schema support |
| TomlLoader                     | ⬜     | -                 | toml                                  | -                | TOML config files        |
| DataFrameLoader                | ⬜     | -                 | pandas                                | -                | Pandas DataFrames        |
| NotebookLoader                 | ⬜     | -                 | nbformat                              | -                | Jupyter notebooks        |
| PythonLoader                   | ⬜     | -                 | ast                                   | -                | Python source code       |
| SRTLoader                      | ⬜     | -                 | -                                     | -                | Subtitle files           |
| OutlookMessageLoader           | ⬜     | -                 | extract-msg                           | -                | Outlook .msg files       |
| ImageCaptionLoader             | ⬜     | -                 | PIL, transformers                     | -                | Image captioning         |
| MHTMLLoader                    | ⬜     | -                 | beautifulsoup4                        | -                | MHTML web archives       |
| VsdxLoader                     | ⬜     | -                 | vsdx                                  | -                | Visio documents          |

### Directory Loaders

| Loader                | Status | Special Methods     | Required Dependencies    | Environment Keys | Notes                      |
| --------------------- | ------ | ------------------- | ------------------------ | ---------------- | -------------------------- |
| DirectoryLoader       | ⬜     | `glob`, `recursive` | -                        | -                | Loads files from directory |
| PyPDFDirectoryLoader  | ⬜     | -                   | pypdf                    | -                | Loads PDFs from directory  |
| NotionDirectoryLoader | ⬜     | -                   | -                        | -                | Loads Notion exports       |
| ObsidianLoader        | ⬜     | -                   | -                        | -                | Loads Obsidian vaults      |
| ReadTheDocsLoader     | ⬜     | -                   | beautifulsoup4           | -                | ReadTheDocs documentation  |
| SlackDirectoryLoader  | ⬜     | -                   | -                        | -                | Slack exports              |
| GutenbergLoader       | ⬜     | -                   | requests, beautifulsoup4 | -                | Project Gutenberg books    |

### Web-based Loaders

| Loader                    | Status | Special Methods             | Required Dependencies    | Environment Keys        | Notes                     |
| ------------------------- | ------ | --------------------------- | ------------------------ | ----------------------- | ------------------------- |
| WebBaseLoader             | ⬜     | -                           | requests, beautifulsoup4 | -                       | Basic web page loader     |
| AsyncHtmlLoader           | ⬜     | -                           | aiohttp, beautifulsoup4  | -                       | Async web loader          |
| SeleniumURLLoader         | ⬜     | -                           | selenium                 | -                       | JavaScript support        |
| PlaywrightURLLoader       | ⬜     | -                           | playwright               | -                       | Modern browser automation |
| RecursiveUrlLoader        | ⬜     | -                           | beautifulsoup4           | -                       | Follows links recursively |
| SitemapLoader             | ⬜     | -                           | beautifulsoup4           | -                       | Uses XML sitemaps         |
| GitHubIssuesLoader        | ⬜     | `load_all_available_issues` | -                        | GITHUB_TOKEN (optional) | Loads GitHub issues       |
| GitHubFileLoader          | ⬜     | -                           | -                        | GITHUB_TOKEN (optional) | Loads files from GitHub   |
| HNLoader                  | ⬜     | -                           | beautifulsoup4           | -                       | Hacker News               |
| IFixitLoader              | ⬜     | -                           | beautifulsoup4           | -                       | iFixit guides             |
| AZLyricsLoader            | ⬜     | -                           | beautifulsoup4           | -                       | Song lyrics               |
| CollegeConfidentialLoader | ⬜     | -                           | beautifulsoup4           | -                       | College discussion boards |
| IMSDbLoader               | ⬜     | -                           | beautifulsoup4           | -                       | Movie scripts             |
| ArxivLoader               | ⬜     | -                           | arxiv, pypdf             | -                       | Academic papers           |
| PubMedLoader              | ⬜     | -                           | biopython                | -                       | Medical papers            |
| NewsURLLoader             | ⬜     | -                           | newspaper3k              | -                       | News articles             |
| BiliBiliLoader            | ⬜     | -                           | requests                 | -                       | BiliBili videos           |
| WikipediaLoader           | ⬜     | -                           | wikipedia                | -                       | Wikipedia articles        |
| MWDumpLoader              | ⬜     | -                           | mwparserfromhell         | -                       | MediaWiki dumps           |
| DuckDBLoader              | ⬜     | -                           | duckdb                   | -                       | DuckDB queries            |
| RSSFeedLoader             | ⬜     | -                           | feedparser               | -                       | RSS feeds                 |
| BrowserlessLoader         | ⬜     | -                           | requests                 | BROWSERLESS_API_KEY     | Browserless.io API        |
| TwitterTweetLoader        | ⬜     | -                           | tweepy                   | TWITTER_API_KEY, etc.   | Twitter/X content         |
| RedditPostsLoader         | ⬜     | -                           | praw                     | REDDIT_CLIENT_ID, etc.  | Reddit posts              |
| BraveSearchLoader         | ⬜     | -                           | requests                 | BRAVE_SEARCH_API_KEY    | Brave search API          |
| GitLoader                 | ⬜     | -                           | GitPython                | -                       | Git repositories          |
| DocugamiLoader            | ⬜     | -                           | requests                 | DOCUGAMI_API_KEY, etc.  | Docugami API              |
| WebSearchLoader           | ⬜     | -                           | -                        | Various search API keys | Meta web search loader    |

### Database Loaders

| Loader                         | Status | Special Methods | Required Dependencies      | Environment Keys            | Notes                      |
| ------------------------------ | ------ | --------------- | -------------------------- | --------------------------- | -------------------------- |
| SQLDatabaseLoader              | ⬜     | -               | sqlalchemy                 | -                           | SQL databases              |
| BigQueryLoader                 | ⬜     | -               | google-cloud-bigquery      | -                           | Google BigQuery            |
| MongodbLoader                  | ⬜     | -               | pymongo                    | -                           | MongoDB                    |
| AstraDBLoader                  | ⬜     | -               | astrapy                    | ASTRA_DB_ID, ASTRA_DB_TOKEN | DataStax Astra DB          |
| SnowflakeLoader                | ⬜     | -               | snowflake-connector-python | -                           | Snowflake DB               |
| KineticaLoader                 | ⬜     | -               | gpudb                      | -                           | Kinetica DB                |
| SurrealDBLoader                | ⬜     | -               | surreal-db                 | -                           | SurrealDB                  |
| AthenaLoader                   | ⬜     | -               | pyathena                   | -                           | Amazon Athena              |
| CassandraLoader                | ⬜     | -               | cassandra-driver           | -                           | Apache Cassandra           |
| CouchbaseLoader                | ⬜     | -               | couchbase                  | -                           | Couchbase                  |
| XorbitsLoader                  | ⬜     | -               | xorbits                    | -                           | Xorbits distributed system |
| ElasticsearchLoader            | ⬜     | -               | elasticsearch              | -                           | Elasticsearch              |
| TiDBLoader                     | ⬜     | -               | pymysql                    | -                           | TiDB                       |
| OracleAutonomousDatabaseLoader | ⬜     | -               | oracledb                   | -                           | Oracle Autonomous DB       |
| OracleDocLoader                | ⬜     | -               | oracledb                   | -                           | Oracle Document Store      |
| PySparkDataFrameLoader         | ⬜     | -               | pyspark                    | -                           | PySpark DataFrames         |
| GlueCatalogLoader              | ⬜     | -               | boto3                      | AWS credentials             | AWS Glue Catalog           |
| PolarsDataFrameLoader          | ⬜     | -               | polars                     | -                           | Polars DataFrames          |
| RocksetLoader                  | ⬜     | -               | rockset                    | ROCKSET_API_KEY             | Rockset database           |
| FaunaLoader                    | ⬜     | -               | fauna                      | FAUNA_SECRET                | Fauna database             |
| CubeSemanticLoader             | ⬜     | -               | requests                   | CUBE_API_URL, etc.          | Cube semantic layer        |

### Cloud Storage Loaders

| Loader                          | Status | Special Methods | Required Dependencies        | Environment Keys       | Notes                                  |
| ------------------------------- | ------ | --------------- | ---------------------------- | ---------------------- | -------------------------------------- |
| S3FileLoader                    | ⬜     | -               | boto3                        | AWS credentials        | Single S3 file                         |
| S3DirectoryLoader               | ⬜     | -               | boto3                        | AWS credentials        | S3 directory                           |
| GCSFileLoader                   | ⬜     | -               | google-cloud-storage         | GCP credentials        | GCS single file                        |
| GCSDirectoryLoader              | ⬜     | -               | google-cloud-storage         | GCP credentials        | GCS directory                          |
| AzureBlobStorageFileLoader      | ⬜     | -               | azure-storage-blob           | AZURE credentials      | Azure blob single file                 |
| AzureBlobStorageContainerLoader | ⬜     | -               | azure-storage-blob           | AZURE credentials      | Azure blob container                   |
| DropboxLoader                   | ⬜     | -               | dropbox                      | DROPBOX_ACCESS_TOKEN   | Dropbox files                          |
| GoogleDriveLoader               | ⬜     | -               | google-auth, googleapiclient | GOOGLE credentials     | Google Drive                           |
| OneDriveLoader                  | ⬜     | -               | o365                         | ONEDRIVE credentials   | OneDrive files                         |
| OneDriveFileLoader              | ⬜     | -               | o365                         | ONEDRIVE credentials   | OneDrive single file                   |
| SharePointLoader                | ⬜     | -               | shareplum                    | SHAREPOINT credentials | SharePoint                             |
| TencentCOSDirectoryLoader       | ⬜     | -               | cos-python-sdk-v5            | TENCENT credentials    | Tencent Cloud Object Storage directory |
| TencentCOSFileLoader            | ⬜     | -               | cos-python-sdk-v5            | TENCENT credentials    | Tencent Cloud Object Storage file      |
| AirbyteJSONLoader               | ⬜     | -               | -                            | -                      | Airbyte integration                    |
| AirbyteGongLoader               | ⬜     | -               | -                            | -                      | Airbyte Gong integration               |
| AirbyteHubspotLoader            | ⬜     | -               | -                            | -                      | Airbyte Hubspot integration            |
| AirbyteSalesforceLoader         | ⬜     | -               | -                            | -                      | Airbyte Salesforce integration         |
| AirbyteShopifyLoader            | ⬜     | -               | -                            | -                      | Airbyte Shopify integration            |
| AirbyteStripeLoader             | ⬜     | -               | -                            | -                      | Airbyte Stripe integration             |
| AirbyteTypeformLoader           | ⬜     | -               | -                            | -                      | Airbyte Typeform integration           |
| AirbyteZendeskSupportLoader     | ⬜     | -               | -                            | -                      | Airbyte Zendesk integration            |
| OBSFileLoader                   | ⬜     | -               | esdk-obs-python              | OBS credentials        | Huawei Cloud OBS file                  |
| OBSDirectoryLoader              | ⬜     | -               | esdk-obs-python              | OBS credentials        | Huawei Cloud OBS directory             |
| LakeFSLoader                    | ⬜     | -               | lakefs-client                | LAKEFS credentials     | LakeFS storage                         |
| AcreomLoader                    | ⬜     | -               | acryl-datahub                | ACREOM credentials     | Acreom knowledge base                  |

### Chat and Messaging Loaders

| Loader                 | Status | Special Methods | Required Dependencies | Environment Keys     | Notes                        |
| ---------------------- | ------ | --------------- | --------------------- | -------------------- | ---------------------------- |
| ChatGPTLoader          | ⬜     | -               | requests              | OPENAI_API_KEY       | ChatGPT conversation exports |
| WhatsAppChatLoader     | ⬜     | -               | -                     | -                    | WhatsApp chat exports        |
| TelegramChatLoader     | ⬜     | -               | -                     | -                    | Telegram chat exports        |
| TelegramChatApiLoader  | ⬜     | -               | requests              | TELEGRAM_BOT_TOKEN   | Telegram Bot API             |
| TelegramChatFileLoader | ⬜     | -               | -                     | -                    | Telegram exported files      |
| DiscordChatLoader      | ⬜     | -               | -                     | -                    | Discord chat exports         |
| MastodonTootsLoader    | ⬜     | -               | mastodon.py           | MASTODON credentials | Mastodon posts               |
| SlackDirectoryLoader   | ⬜     | -               | -                     | -                    | Slack exports                |
| FacebookChatLoader     | ⬜     | -               | -                     | -                    | Facebook Messenger exports   |

### API and Service Loaders

| Loader                            | Status | Special Methods | Required Dependencies    | Environment Keys         | Notes                            |
| --------------------------------- | ------ | --------------- | ------------------------ | ------------------------ | -------------------------------- |
| AirbyteCDKLoader                  | ⬜     | -               | airbyte-cdk              | -                        | Airbyte CDK                      |
| AirtableLoader                    | ⬜     | -               | pyairtable               | AIRTABLE_API_KEY         | Airtable                         |
| ApifyDatasetLoader                | ⬜     | -               | apify-client             | APIFY_API_TOKEN          | Apify                            |
| ConfluenceLoader                  | ⬜     | -               | atlassian-python-api     | CONFLUENCE credentials   | Confluence                       |
| FigmaFileLoader                   | ⬜     | -               | requests                 | FIGMA_ACCESS_TOKEN, etc. | Figma designs                    |
| NotionDBLoader                    | ⬜     | -               | notion-client            | NOTION_TOKEN, etc.       | Notion databases                 |
| JoplinLoader                      | ⬜     | -               | requests                 | JOPLIN_TOKEN             | Joplin notes                     |
| IuguLoader                        | ⬜     | -               | requests                 | IUGU_API_KEY             | Iugu payment system              |
| LarkSuiteDocLoader                | ⬜     | -               | requests                 | LARKSUITE credentials    | LarkSuite documents              |
| ModernTreasuryLoader              | ⬜     | -               | requests                 | MODERN_TREASURY_API_KEY  | Modern Treasury                  |
| PebbloSafeLoader                  | ⬜     | -               | requests                 | PEBBLO_API_KEY           | Pebblo Safe platform             |
| PebbloTextLoader                  | ⬜     | -               | requests                 | PEBBLO_API_KEY           | Pebblo text content              |
| PsychicLoader                     | ⬜     | -               | psychicapi               | PSYCHIC_API_KEY          | Psychic data platform            |
| RoamLoader                        | ⬜     | -               | -                        | -                        | Roam Research                    |
| ScrapflyLoader                    | ⬜     | -               | scrapfly-sdk             | SCRAPFLY_KEY             | Scrapfly web scraping            |
| ScrapingAntLoader                 | ⬜     | -               | requests                 | SCRAPINGANT_API_KEY      | ScrapingAnt                      |
| SpreedlyLoader                    | ⬜     | -               | requests                 | SPREEDLY_API_KEY         | Spreedly payment system          |
| StripeLoader                      | ⬜     | -               | stripe                   | STRIPE_API_KEY           | Stripe payment system            |
| TrelloLoader                      | ⬜     | -               | requests                 | TRELLO_API_KEY, etc.     | Trello boards                    |
| WeatherDataLoader                 | ⬜     | -               | requests                 | WEATHER_API_KEY          | Weather data                     |
| YuqueLoader                       | ⬜     | -               | requests                 | YUQUE_TOKEN              | Yuque knowledge base             |
| DatadogLogsLoader                 | ⬜     | -               | datadog                  | DATADOG_API_KEY, etc.    | Datadog logs                     |
| EtherscanLoader                   | ⬜     | -               | requests                 | ETHERSCAN_API_KEY        | Ethereum blockchain              |
| EverNoteLoader                    | ⬜     | -               | requests                 | EVERNOTE credentials     | Evernote notes                   |
| FireCrawlLoader                   | ⬜     | -               | requests                 | FIRECRAWL_API_KEY        | FireCrawl web scraping           |
| GoogleApiYoutubeLoader            | ⬜     | -               | google-api-python-client | GOOGLE_API_KEY           | YouTube via Google API           |
| GoogleSpeechToTextLoader          | ⬜     | -               | google-cloud-speech      | GOOGLE credentials       | Google Speech-to-Text            |
| AssemblyAIAudioLoaderById         | ⬜     | -               | requests                 | ASSEMBLYAI_API_KEY       | AssemblyAI transcript by ID      |
| AssemblyAIAudioTranscriptLoader   | ⬜     | -               | requests                 | ASSEMBLYAI_API_KEY       | AssemblyAI audio transcript      |
| YoutubeAudioLoader                | ⬜     | -               | pytube                   | -                        | YouTube audio extraction         |
| DiffbotLoader                     | ⬜     | -               | diffbot                  | DIFFBOT_API_KEY          | Diffbot web extraction           |
| BlackboardLoader                  | ⬜     | -               | requests, beautifulsoup4 | BLACKBOARD credentials   | Blackboard LMS                   |
| OpenCityDataLoader                | ⬜     | -               | requests                 | -                        | Open city data APIs              |
| AmazonTextractPDFLoader           | ⬜     | -               | boto3                    | AWS credentials          | Amazon Textract PDF              |
| ArcGISLoader                      | ⬜     | -               | arcgis                   | ARCGIS credentials       | ArcGIS geospatial                |
| AzureAIDataLoader                 | ⬜     | -               | azure-ai-formrecognizer  | AZURE credentials        | Azure AI data extraction         |
| AzureAIDocumentIntelligenceLoader | ⬜     | -               | azure-ai-formrecognizer  | AZURE credentials        | Azure document intelligence      |
| CoNLLULoader                      | ⬜     | -               | conllu                   | -                        | CoNLL-U format                   |
| DedocAPIFileLoader                | ⬜     | -               | dedoc-python             | -                        | Dedoc document extraction API    |
| DedocFileLoader                   | ⬜     | -               | dedoc                    | -                        | Dedoc document extraction        |
| DedocPDFLoader                    | ⬜     | -               | dedoc                    | -                        | Dedoc PDF extraction             |
| LLMSherpaFileLoader               | ⬜     | -               | llmsherpa                | LLMSHERPA_API_KEY        | LLM Sherpa document extraction   |
| BlockchainDocumentLoader          | ⬜     | -               | web3                     | -                        | Blockchain documents             |
| MaxComputeLoader                  | ⬜     | -               | pyodps                   | MAXCOMPUTE credentials   | MaxCompute data                  |
| OracleTextSplitter                | ⬜     | -               | oracledb                 | -                        | Oracle text extraction           |
| GeoDataFrameLoader                | ⬜     | -               | geopandas                | -                        | Geospatial data                  |
| HuggingFaceDatasetLoader          | ⬜     | -               | datasets                 | -                        | HuggingFace datasets             |
| HuggingFaceModelLoader            | ⬜     | -               | transformers             | -                        | HuggingFace models               |
| TensorflowDatasetLoader           | ⬜     | -               | tensorflow               | -                        | TensorFlow datasets              |
| ToMarkdownLoader                  | ⬜     | -               | markdownify              | -                        | Converts HTML to Markdown        |
| UnstructuredAPIFileLoader         | ⬜     | -               | unstructured             | UNSTRUCTURED_API_KEY     | Unstructured.io API              |
| UnstructuredAPIFileIOLoader       | ⬜     | -               | unstructured             | UNSTRUCTURED_API_KEY     | Unstructured.io API with file IO |
| UnstructuredFileIOLoader          | ⬜     | -               | unstructured             | -                        | Unstructured with file IO        |
| UnstructuredFileLoader            | ⬜     | -               | unstructured             | -                        | Generic unstructured loader      |

## Implementation Approach

Based on the inventory above, we'll implement a system that:

1. Groups loaders by their source type categories
2. Creates base source classes for each category
3. Implements specialized source classes for specific file types or services
4. Dynamically registers and detects appropriate source types
5. Provides flexible loader strategy selection

## Base Source Classes

```python
class BaseSource(BaseModel):
    """Root base class for all sources."""

class LocalFileSource(BaseSource):
    """Base for local file sources."""

class LocalDirectorySource(BaseSource):
    """Base for directory sources."""

class WebSource(BaseSource):
    """Base for web-based sources."""

class DatabaseSource(BaseSource):
    """Base for database sources."""

class CloudStorageSource(BaseSource):
    """Base for cloud storage sources."""

class APISource(BaseSource):
    """Base for API-based sources."""

class MessagingSource(BaseSource):
    """Base for chat and messaging sources."""
```

## Next Steps

1. Begin implementation with the most common file-based loaders
2. Extend to web-based loaders
3. Add support for cloud storage and databases
4. Implement specialized API integrations
5. Add messaging and chat source support
