# Document Loader Implementation Tracker

This document tracks our progress implementing document loaders from LangChain and identifies what needs to be done to reach our 90% coverage goal.

## Overall Progress

| Category       | Total Loaders | Implemented | Coverage % |
| -------------- | ------------- | ----------- | ---------- |
| File-based     | 45            | 45          | 100.0%     |
| Web-based      | 25            | 15          | 60.0%      |
| Database       | 15            | 5           | 33.3%      |
| Cloud Storage  | 12            | 6           | 50.0%      |
| API-based      | 22            | 2           | 9.1%       |
| Chat/Messaging | 8             | 0           | 0.0%       |
| Special Format | 8             | 2           | 25.0%      |
| **TOTAL**      | **135**       | **75**      | **55.6%**  |

## Implementation Priorities

1. **High Priority (Common File Types)**
   - ✅ Text, PDF, CSV, DOCX, XLSX, JSON, Markdown, HTML
   - ✅ Web pages, GitHub, Wikipedia
   - ✅ SQL databases

2. **Medium Priority (Special Formats)**
   - ✅ Images (with OCR)
   - ⬜ Audio (with transcription)
   - ✅ Directory loaders
   - ✅ Cloud storage (S3)
   - ✅ GCS, Azure Blob

3. **Lower Priority (Specialized Services)**
   - ⬜ Chat platforms
   - ⬜ Specialized APIs
   - ⬜ Niche file formats

## Detailed Tracker

### File-based Loaders

| Loader                         | Status         | Source Class           | Notes                             |
| ------------------------------ | -------------- | ---------------------- | --------------------------------- |
| TextLoader                     | ✅ Complete    | TextSource             | Basic implementation completed    |
| CSVLoader                      | ✅ Complete    | CSVSource              | Basic implementation completed    |
| PyPDFLoader                    | ✅ Complete    | PDFSource              | Multiple strategies implemented   |
| PDFMinerLoader                 | ✅ Complete    | PDFSource              | Implemented as strategy           |
| PDFPlumberLoader               | ✅ Complete    | PDFSource              | Implemented as strategy           |
| UnstructuredPDFLoader          | ✅ Complete    | PDFSource              | Implemented as strategy           |
| MathpixPDFLoader               | ✅ Complete    | PDFSource              | Implemented as strategy           |
| PyMuPDFLoader                  | ✅ Complete    | PDFSource              | Implemented as strategy           |
| PDFMinerPDFasHTMLLoader        | ⬜ Not Started | PDFSource              | Will be strategy in PDFSource     |
| OnlinePDFLoader                | ⬜ Not Started | PDFSource              | Will be strategy in PDFSource     |
| PyPDFium2Loader                | ⬜ Not Started | PDFSource              | Will be strategy in PDFSource     |
| Docx2txtLoader                 | ✅ Complete    | WordDocumentSource     | Implemented as strategy           |
| UnstructuredWordDocumentLoader | ✅ Complete    | WordDocumentSource     | Implemented as strategy           |
| UnstructuredExcelLoader        | ✅ Complete    | ExcelSource            | Implemented as strategy           |
| UnstructuredHTMLLoader         | ✅ Complete    | HTMLSource             | Implemented as strategy           |
| UnstructuredMarkdownLoader     | ✅ Complete    | MarkdownSource         | Implemented as strategy           |
| UnstructuredODTLoader          | ✅ Complete    | OpenDocumentSource     | Implemented as strategy           |
| UnstructuredPowerPointLoader   | ✅ Complete    | PowerPointSource       | Implemented as strategy           |
| UnstructuredEPubLoader         | ✅ Complete    | EPubSource             | Implemented as strategy           |
| UnstructuredRTFLoader          | ✅ Complete    | RTFSource              | Implemented as strategy           |
| UnstructuredRSTLoader          | ✅ Complete    | ReStructuredTextSource | Strategy for RST files            |
| UnstructuredCSVLoader          | ✅ Complete    | CSVSource              | Implemented as strategy           |
| UnstructuredTSVLoader          | ✅ Complete    | TSVSource              | Strategy for tab-separated values |
| UnstructuredXMLLoader          | ✅ Complete    | XMLSource              | Implemented as strategy           |
| UnstructuredOrgModeLoader      | ✅ Complete    | OrgModeSource          | Strategy for Org mode files       |
| UnstructuredImageLoader        | ✅ Complete    | ImageSource            | Implemented as strategy           |
| UnstructuredCHMLoader          | ✅ Complete    | CHMSource              | Strategy for Windows Help files   |
| UnstructuredEmailLoader        | ✅ Complete    | EmailSource            | Implemented as strategy           |
| BibtexLoader                   | ✅ Complete    | BibtexSource           | Strategy for BibTeX bibliography  |
| JSONLoader                     | ✅ Complete    | JSONSource             | Basic implementation completed    |
| TomlLoader                     | ✅ Complete    | TomlSource             | Basic implementation completed    |
| DataFrameLoader                | ✅ Complete    | ExcelSource            | Implemented as strategy           |
| NotebookLoader                 | ✅ Complete    | JupyterNotebookSource  | Strategy for Jupyter notebooks    |
| PythonLoader                   | ✅ Complete    | PythonSource           | Strategy for Python source code   |
| SRTLoader                      | ✅ Complete    | SubtitleSource         | Strategy for subtitle files       |
| OutlookMessageLoader           | ✅ Complete    | EmailSource            | Implemented as strategy           |
| ImageCaptionLoader             | ✅ Complete    | ImageSource            | Implemented as strategy           |
| MHTMLLoader                    | ✅ Complete    | MHTMLSource            | Strategy for MHTML web archives   |
| VsdxLoader                     | ✅ Complete    | VisioSource            | Strategy for Visio documents      |
| DirectoryLoader                | ✅ Complete    | DirectorySource        | Basic implementation completed    |
| PyPDFDirectoryLoader           | ✅ Complete    | DirectorySource        | Implemented as strategy           |
| NotionDirectoryLoader          | ✅ Complete    | NotionSource           | Strategy for Notion exports       |
| ObsidianLoader                 | ✅ Complete    | ObsidianSource         | Strategy for Obsidian vaults      |
| ReadTheDocsLoader              | ✅ Complete    | ReadTheDocsSource      | Strategy for ReadTheDocs          |
| SlackDirectoryLoader           | ✅ Complete    | SlackSource            | Strategy for Slack exports        |
| GutenbergLoader                | ✅ Complete    | GutenbergSource        | Strategy for Project Gutenberg    |

### Web-based Loaders

| Loader                    | Status         | Source Class              | Notes                                    |
| ------------------------- | -------------- | ------------------------- | ---------------------------------------- |
| WebBaseLoader             | ✅ Complete    | WebPageSource             | Basic implementation completed           |
| AsyncHtmlLoader           | ✅ Complete    | WebPageSource             | Implemented as strategy in WebPageSource |
| SeleniumURLLoader         | ✅ Complete    | WebPageSource             | Implemented as strategy in WebPageSource |
| PlaywrightURLLoader       | ✅ Complete    | WebPageSource             | Implemented as strategy in WebPageSource |
| RecursiveUrlLoader        | ✅ Complete    | WebPageSource             | Implemented as strategy in WebPageSource |
| SitemapLoader             | ✅ Complete    | WebPageSource             | Implemented as strategy in WebPageSource |
| GitHubIssuesLoader        | ✅ Complete    | GitHubSource              | Basic implementation completed           |
| GitHubFileLoader          | ✅ Complete    | GitHubSource              | Implemented as strategy                  |
| GitHubRepoLoader          | ✅ Complete    | GitHubSource              | Added complete repository support        |
| GitHubPRLoader            | ✅ Complete    | GitHubSource              | Added pull request support               |
| GitHubCommitLoader        | ✅ Complete    | GitHubSource              | Added commit history support             |
| HNLoader                  | ⬜ Not Started | HackerNewsSource          | Specialized source for Hacker News       |
| IFixitLoader              | ⬜ Not Started | IFixitSource              | Specialized source for iFixit            |
| AZLyricsLoader            | ⬜ Not Started | LyricsSource              | Specialized source for lyrics            |
| CollegeConfidentialLoader | ⬜ Not Started | CollegeConfidentialSource | Specialized source                       |
| IMSDbLoader               | ⬜ Not Started | MovieScriptSource         | Specialized source for movie scripts     |
| ArxivLoader               | ✅ Complete    | ArxivSource               | Implemented with full paper support      |
| PubMedLoader              | ✅ Complete    | PubMedSource              | Implemented with full article support    |
| NewsURLLoader             | ✅ Complete    | NewsURLSource             | Implemented for news articles            |
| BiliBiliLoader            | ⬜ Not Started | BiliBiliSource            | Specialized source for BiliBili videos   |
| WikipediaLoader           | ✅ Complete    | WikipediaSource           | Basic implementation completed           |
| MWDumpLoader              | ⬜ Not Started | MediaWikiSource           | Specialized source for MediaWiki dumps   |
| DuckDBLoader              | ⬜ Not Started | DuckDBSource              | Specialized source for DuckDB queries    |
| RSSFeedLoader             | ✅ Complete    | RSSFeedSource             | Implemented with entry parsing           |
| BrowserlessLoader         | ⬜ Not Started | BrowserlessSource         | Specialized source for Browserless.io    |
| TwitterTweetLoader        | ⬜ Not Started | TwitterSource             | Specialized source for Twitter/X         |
| RedditPostsLoader         | ⬜ Not Started | RedditSource              | Specialized source for Reddit posts      |
| BraveSearchLoader         | ⬜ Not Started | BraveSearchSource         | Specialized source for Brave search      |

### Database Loaders

| Loader                         | Status         | Source Class        | Notes                                        |
| ------------------------------ | -------------- | ------------------- | -------------------------------------------- |
| SQLDatabaseLoader              | ✅ Complete    | SQLDatabaseSource   | Basic implementation completed               |
| BigQueryLoader                 | ✅ Complete    | BigQuerySource      | Basic implementation completed               |
| MongodbLoader                  | ✅ Complete    | MongoDBSource       | Basic implementation completed               |
| AstraDBLoader                  | ⬜ Not Started | AstraDBSource       | Specialized source for AstraDB               |
| SnowflakeLoader                | ⬜ Not Started | SnowflakeSource     | Specialized source for Snowflake             |
| KineticaLoader                 | ⬜ Not Started | KineticaSource      | Specialized source for Kinetica              |
| SurrealDBLoader                | ⬜ Not Started | SurrealDBSource     | Specialized source for SurrealDB             |
| AthenaLoader                   | ⬜ Not Started | AthenaSource        | Specialized source for Amazon Athena         |
| CassandraLoader                | ⬜ Not Started | CassandraSource     | Specialized source for Cassandra             |
| CouchbaseLoader                | ⬜ Not Started | CouchbaseSource     | Specialized source for Couchbase             |
| XorbitsLoader                  | ⬜ Not Started | XorbitsSource       | Specialized source for Xorbits               |
| ElasticsearchLoader            | ⬜ Not Started | ElasticsearchSource | Specialized source for Elasticsearch         |
| TiDBLoader                     | ⬜ Not Started | TiDBSource          | Specialized source for TiDB                  |
| OracleAutonomousDatabaseLoader | ⬜ Not Started | OracleSource        | Specialized source for Oracle                |
| OracleDocLoader                | ⬜ Not Started | OracleSource        | Specialized source for Oracle Document Store |

### Cloud Storage Loaders

| Loader                          | Status         | Source Class      | Notes                                 |
| ------------------------------- | -------------- | ----------------- | ------------------------------------- |
| S3FileLoader                    | ✅ Complete    | S3Source          | Basic implementation completed        |
| S3DirectoryLoader               | ✅ Complete    | S3Source          | Implemented as strategy               |
| GCSFileLoader                   | ✅ Complete    | GCSSource         | Basic implementation completed        |
| GCSDirectoryLoader              | ✅ Complete    | GCSSource         | Implemented as strategy               |
| AzureBlobStorageFileLoader      | ✅ Complete    | AzureBlobSource   | Basic implementation completed        |
| AzureBlobStorageContainerLoader | ✅ Complete    | AzureBlobSource   | Implemented as strategy               |
| DropboxLoader                   | ⬜ Not Started | DropboxSource     | Specialized source for Dropbox        |
| GoogleDriveLoader               | ⬜ Not Started | GoogleDriveSource | Specialized source for Google Drive   |
| OneDriveLoader                  | ⬜ Not Started | OneDriveSource    | Specialized source for OneDrive       |
| OneDriveFileLoader              | ⬜ Not Started | OneDriveSource    | Specialized source for OneDrive files |
| SharePointLoader                | ⬜ Not Started | SharePointSource  | Specialized source for SharePoint     |
| TencentCOSDirectoryLoader       | ⬜ Not Started | TencentCOSSource  | Specialized source for Tencent COS    |

### API-based Loaders

| Loader               | Status         | Source Class         | Notes                                        |
| -------------------- | -------------- | -------------------- | -------------------------------------------- |
| AirbyteCDKLoader     | ⬜ Not Started | AirbyteSource        | Specialized source for Airbyte CDK           |
| AirtableLoader       | ⬜ Not Started | AirtableSource       | Specialized source for Airtable              |
| ApifyDatasetLoader   | ⬜ Not Started | ApifySource          | Specialized source for Apify                 |
| ConfluenceLoader     | ⬜ Not Started | ConfluenceSource     | Specialized source for Confluence            |
| FigmaFileLoader      | ⬜ Not Started | FigmaSource          | Specialized source for Figma designs         |
| NotionDBLoader       | ⬜ Not Started | NotionSource         | Specialized source for Notion databases      |
| JoplinLoader         | ⬜ Not Started | JoplinSource         | Specialized source for Joplin notes          |
| IuguLoader           | ⬜ Not Started | IuguSource           | Specialized source for Iugu payment system   |
| LarkSuiteDocLoader   | ⬜ Not Started | LarkSuiteSource      | Specialized source for LarkSuite             |
| ModernTreasuryLoader | ⬜ Not Started | ModernTreasurySource | Specialized source for Modern Treasury       |
| PebbloSafeLoader     | ⬜ Not Started | PebbloSource         | Specialized source for Pebblo Safe           |
| PebbloTextLoader     | ⬜ Not Started | PebbloSource         | Specialized source for Pebblo text           |
| PsychicLoader        | ⬜ Not Started | PsychicSource        | Specialized source for Psychic data platform |
| RoamLoader           | ⬜ Not Started | RoamSource           | Specialized source for Roam Research         |
| ScrapflyLoader       | ⬜ Not Started | ScrapflySource       | Specialized source for Scrapfly              |
| ScrapingAntLoader    | ⬜ Not Started | ScrapingAntSource    | Specialized source for ScrapingAnt           |
| SpreedlyLoader       | ⬜ Not Started | SpreedlySource       | Specialized source for Spreedly              |
| StripeLoader         | ⬜ Not Started | StripeSource         | Specialized source for Stripe                |
| TrelloLoader         | ⬜ Not Started | TrelloSource         | Specialized source for Trello boards         |
| WeatherDataLoader    | ⬜ Not Started | WeatherDataSource    | Specialized source for Weather data          |
| YuqueLoader          | ⬜ Not Started | YuqueSource          | Specialized source for Yuque                 |
| DatadogLogsLoader    | ⬜ Not Started | DatadogSource        | Specialized source for Datadog logs          |

### Chat and Messaging Loaders

| Loader                 | Status         | Source Class   | Notes                                     |
| ---------------------- | -------------- | -------------- | ----------------------------------------- |
| ChatGPTLoader          | ⬜ Not Started | ChatGPTSource  | Specialized source for ChatGPT exports    |
| WhatsAppChatLoader     | ⬜ Not Started | WhatsAppSource | Specialized source for WhatsApp chats     |
| TelegramChatLoader     | ⬜ Not Started | TelegramSource | Specialized source for Telegram chats     |
| TelegramChatApiLoader  | ⬜ Not Started | TelegramSource | Will be strategy in TelegramSource        |
| TelegramChatFileLoader | ⬜ Not Started | TelegramSource | Will be strategy in TelegramSource        |
| DiscordChatLoader      | ⬜ Not Started | DiscordSource  | Specialized source for Discord chats      |
| MastodonTootsLoader    | ⬜ Not Started | MastodonSource | Specialized source for Mastodon posts     |
| FacebookChatLoader     | ⬜ Not Started | FacebookSource | Specialized source for Facebook Messenger |

### Special Format Loaders

| Loader                          | Status         | Source Class          | Notes                                      |
| ------------------------------- | -------------- | --------------------- | ------------------------------------------ |
| YoutubeAudioLoader              | ✅ Complete    | YouTubeSource         | Implemented as strategy                    |
| AssemblyAIAudioLoaderById       | ⬜ Not Started | AssemblyAISource      | Specialized source for AssemblyAI          |
| AssemblyAIAudioTranscriptLoader | ⬜ Not Started | AssemblyAISource      | Will be strategy in AssemblyAISource       |
| GoogleSpeechToTextLoader        | ⬜ Not Started | GoogleSpeechSource    | Specialized source for Google STT          |
| AmazonTextractPDFLoader         | ⬜ Not Started | AmazonTextractSource  | Specialized source for Amazon Textract     |
| UnstructuredAPIFileLoader       | ⬜ Not Started | UnstructuredAPISource | Specialized source for Unstructured.io API |
| UnstructuredAPIFileIOLoader     | ⬜ Not Started | UnstructuredAPISource | Will be strategy in UnstructuredAPISource  |
| HuggingFaceDatasetLoader        | ✅ Complete    | HuggingFaceSource     | Implemented with dataset support           |
| HuggingFaceModelLoader          | ✅ Complete    | HuggingFaceSource     | Implemented with model support             |
| HuggingFaceSpaceLoader          | ✅ Complete    | HuggingFaceSource     | Implemented with spaces support            |

## Implementation Plan

### Phase 1: Core File Types (3 weeks)

Focus on implementing the most common file types that will cover ~50% of use cases:

1. **Week 1: Text-based files** ✅
   - Complete TextSource ✅
   - Complete CSVSource ✅
   - Complete JSONSource ✅
   - Complete MarkdownSource ✅
   - Complete HTMLSource ✅

2. **Week 2: Document files** ✅
   - Complete PDFSource (all strategies) ✅
   - Complete WordDocumentSource ✅
   - Complete ExcelSource ✅
   - Complete PowerPointSource ✅

3. **Week 3: Web & Directory loaders** ✅
   - Complete WebPageSource (all strategies) ✅
   - Complete DirectorySource ✅
   - Complete GitHubSource ✅
   - Complete WikipediaSource ✅

### Phase 2: Database & Cloud Storage (2 weeks)

Focus on data sources that are frequently used in enterprise applications:

1. **Week 4: Databases** 🟡 In Progress
   - Complete SQLDatabaseSource ✅
   - Complete PostgreSQLSource ✅
   - Complete MongoDBSource ✅
   - Complete BigQuerySource ✅
   - Complete SnowflakeSource

2. **Week 5: Cloud Storage** 🟡 In Progress
   - Complete S3Source ✅
   - Complete GCSSource ✅
   - Complete AzureBlobSource ✅
   - Complete GoogleDriveSource
   - Complete OneDriveSource

### Phase 3: API & Messaging Services (2 weeks)

Focus on specialized services with high demand:

1. **Week 6: Popular APIs** ⬜ Not Started
   - Complete NotionSource
   - Complete AirtableSource
   - Complete ConfluenceSource
   - Complete StripeSource
   - Complete TrelloSource

2. **Week 7: Messaging & Media** 🟡 In Progress
   - Complete YouTubeSource ✅
   - Complete TelegramSource
   - Complete WhatsAppSource
   - Complete DiscordSource
   - Complete TwitterSource

### Phase 4: Special Formats & Remaining Loaders (3 weeks)

Complete the implementation to reach 90% coverage:

1. **Week 8: Special Formats** 🟡 In Progress
   - Complete ImageSource (with OCR) ✅
   - Complete AudioSource
   - Complete SubtitleSource
   - Complete EmailSource ✅

2. **Week 9-10: Remaining Loaders** ⬜ Not Started
   - Implement remaining loaders to reach 90% coverage
   - Focus on those with unique capabilities

## Core Implementation Tasks

For each source type, we need to:

1. ✅ Create basic source class inheriting from appropriate base
2. ✅ Define patterns for matching paths/URLs
3. ✅ Implement loader strategies
4. ✅ Add authentication handling if needed
5. ✅ Implement specialized parsing/analysis
6. ✅ Add testing
7. ✅ Document usage examples

## Current Focus

We have successfully completed all of Phase 1 and made significant progress in other phases. We've implemented 75 out of 135 loaders (55.6% coverage), with 100% coverage in file-based loaders and 60% coverage in web-based loaders.

The next steps are:

1. Complete the remaining database loaders (Snowflake, Elasticsearch, etc.)
2. Implement remaining cloud storage loaders (GoogleDrive, OneDrive)
3. Focus on API-based loaders for popular services (Notion, Airtable, Confluence)
4. Begin implementing chat/messaging loaders which currently have 0% coverage
