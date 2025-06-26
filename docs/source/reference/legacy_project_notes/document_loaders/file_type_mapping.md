# File Type to Loader Mapping

This document provides a comprehensive mapping of file extensions to appropriate LangChain document loaders, organized by file category.

## Text Files

| Extension | Loader                     | Source Class           | Strategies          |
| --------- | -------------------------- | ---------------------- | ------------------- |
| .txt      | TextLoader                 | TextSource             | basic, unstructured |
| .text     | TextLoader                 | TextSource             | basic, unstructured |
| .md       | UnstructuredMarkdownLoader | MarkdownSource         | unstructured, text  |
| .markdown | UnstructuredMarkdownLoader | MarkdownSource         | unstructured, text  |
| .rst      | UnstructuredRSTLoader      | ReStructuredTextSource | unstructured        |
| .org      | UnstructuredOrgModeLoader  | OrgModeSource          | unstructured        |
| .log      | TextLoader                 | LogFileSource          | basic, tail         |
| .conf     | TextLoader                 | ConfigFileSource       | basic               |
| .cfg      | TextLoader                 | ConfigFileSource       | basic               |
| .ini      | TextLoader                 | ConfigFileSource       | basic               |

## Document Files

| Extension | Loader                         | Source Class       | Strategies                   |
| --------- | ------------------------------ | ------------------ | ---------------------------- |
| .pdf      | PyPDFLoader                    | PDFSource          | fast, ocr, tables, math, aws |
| .doc      | UnstructuredWordDocumentLoader | WordDocumentSource | unstructured                 |
| .docx     | Docx2txtLoader                 | WordDocumentSource | fast, unstructured           |
| .ppt      | UnstructuredPowerPointLoader   | PowerPointSource   | unstructured                 |
| .pptx     | UnstructuredPowerPointLoader   | PowerPointSource   | unstructured                 |
| .xls      | UnstructuredExcelLoader        | ExcelSource        | unstructured, pandas         |
| .xlsx     | UnstructuredExcelLoader        | ExcelSource        | unstructured, pandas         |
| .odt      | UnstructuredODTLoader          | OpenDocumentSource | unstructured                 |
| .ods      | UnstructuredExcelLoader        | OpenDocumentSource | unstructured                 |
| .odp      | UnstructuredPowerPointLoader   | OpenDocumentSource | unstructured                 |
| .rtf      | UnstructuredRTFLoader          | RTFSource          | unstructured                 |
| .epub     | UnstructuredEPubLoader         | EPubSource         | unstructured                 |
| .msg      | OutlookMessageLoader           | OutlookSource      | basic                        |

## Data Files

| Extension | Loader                | Source Class  | Strategies                  |
| --------- | --------------------- | ------------- | --------------------------- |
| .csv      | CSVLoader             | CSVSource     | basic, unstructured, pandas |
| .tsv      | UnstructuredTSVLoader | TSVSource     | unstructured, pandas        |
| .json     | JSONLoader            | JSONSource    | basic, unstructured, jq     |
| .jsonl    | JSONLoader            | JSONSource    | basic, lines                |
| .xml      | UnstructuredXMLLoader | XMLSource     | unstructured                |
| .yaml     | TextLoader            | YAMLSource    | basic                       |
| .yml      | TextLoader            | YAMLSource    | basic                       |
| .toml     | TomlLoader            | TomlSource    | basic                       |
| .parquet  | TextLoader            | ParquetSource | pandas, pyarrow             |
| .sqlite   | SQLDatabaseLoader     | SQLiteSource  | sql                         |
| .db       | SQLDatabaseLoader     | SQLiteSource  | sql                         |

## Code Files

| Extension | Loader         | Source Class          | Strategies        |
| --------- | -------------- | --------------------- | ----------------- |
| .py       | PythonLoader   | PythonSource          | basic, ast        |
| .ipynb    | NotebookLoader | JupyterNotebookSource | basic             |
| .js       | TextLoader     | JavaScriptSource      | basic             |
| .ts       | TextLoader     | TypeScriptSource      | basic             |
| .html     | BSHTMLLoader   | HTMLSource            | bs4, unstructured |
| .htm      | BSHTMLLoader   | HTMLSource            | bs4, unstructured |
| .css      | TextLoader     | CSSSource             | basic             |
| .java     | TextLoader     | JavaSource            | basic             |
| .cpp      | TextLoader     | CPPSource             | basic             |
| .c        | TextLoader     | CSource               | basic             |
| .cs       | TextLoader     | CSharpSource          | basic             |
| .php      | TextLoader     | PHPSource             | basic             |
| .rb       | TextLoader     | RubySource            | basic             |
| .go       | TextLoader     | GoSource              | basic             |
| .rs       | TextLoader     | RustSource            | basic             |
| .swift    | TextLoader     | SwiftSource           | basic             |
| .kt       | TextLoader     | KotlinSource          | basic             |
| .sh       | TextLoader     | ShellScriptSource     | basic             |
| .bat      | TextLoader     | BatchFileSource       | basic             |
| .ps1      | TextLoader     | PowerShellSource      | basic             |
| .sql      | TextLoader     | SQLSource             | basic             |

## Media Files

| Extension | Loader                   | Source Class   | Strategies                  |
| --------- | ------------------------ | -------------- | --------------------------- |
| .jpg      | UnstructuredImageLoader  | ImageSource    | ocr, caption                |
| .jpeg     | UnstructuredImageLoader  | ImageSource    | ocr, caption                |
| .png      | UnstructuredImageLoader  | ImageSource    | ocr, caption                |
| .gif      | UnstructuredImageLoader  | ImageSource    | ocr, caption                |
| .tiff     | UnstructuredImageLoader  | ImageSource    | ocr, caption                |
| .bmp      | UnstructuredImageLoader  | ImageSource    | ocr, caption                |
| .webp     | UnstructuredImageLoader  | ImageSource    | ocr, caption                |
| .mp3      | AudioTranscriptionLoader | AudioSource    | whisper, assemblyai, google |
| .mp4      | VideoTranscriptionLoader | VideoSource    | extract_audio, caption      |
| .wav      | AudioTranscriptionLoader | AudioSource    | whisper, assemblyai, google |
| .avi      | VideoTranscriptionLoader | VideoSource    | extract_audio, caption      |
| .mov      | VideoTranscriptionLoader | VideoSource    | extract_audio, caption      |
| .flac     | AudioTranscriptionLoader | AudioSource    | whisper, assemblyai, google |
| .srt      | SRTLoader                | SubtitleSource | basic                       |
| .vtt      | SRTLoader                | SubtitleSource | basic                       |

## Archive Files

| Extension | Loader        | Source Class          | Strategies          |
| --------- | ------------- | --------------------- | ------------------- |
| .zip      | ArchiveLoader | ZipArchiveSource      | extract, iterate    |
| .tar      | ArchiveLoader | TarArchiveSource      | extract, iterate    |
| .gz       | ArchiveLoader | GzipArchiveSource     | extract, decompress |
| .7z       | ArchiveLoader | SevenZipArchiveSource | extract, iterate    |
| .rar      | ArchiveLoader | RarArchiveSource      | extract, iterate    |

## Special Format Files

| Extension | Loader                  | Source Class    | Strategies         |
| --------- | ----------------------- | --------------- | ------------------ |
| .eml      | UnstructuredEmailLoader | EmailSource     | unstructured       |
| .mbox     | UnstructuredEmailLoader | EmailSource     | unstructured, mbox |
| .mht      | MHTMLLoader             | MHTMLSource     | basic              |
| .mhtml    | MHTMLLoader             | MHTMLSource     | basic              |
| .chm      | UnstructuredCHMLoader   | CHMSource       | unstructured       |
| .bib      | BibtexLoader            | BibtexSource    | basic              |
| .tex      | TextLoader              | LaTeXSource     | basic              |
| .vsdx     | VsdxLoader              | VisioSource     | basic              |
| .psd      | UnstructuredImageLoader | PhotoshopSource | ocr, layers        |

## Directory and Path Types

| Path Type      | Loader                | Source Class        | Strategies              |
| -------------- | --------------------- | ------------------- | ----------------------- |
| directory      | DirectoryLoader       | DirectorySource     | basic, recursive, glob  |
| pdf_directory  | PyPDFDirectoryLoader  | PDFDirectorySource  | basic, recursive        |
| git_repo       | GitLoader             | GitRepositorySource | basic, commits, history |
| obsidian_vault | ObsidianLoader        | ObsidianSource      | basic, recursive        |
| notion_export  | NotionDirectoryLoader | NotionExportSource  | basic, recursive        |
| slack_export   | SlackDirectoryLoader  | SlackExportSource   | basic, recursive        |

## URL Types

| URL Pattern           | Loader             | Source Class      | Strategies                   |
| --------------------- | ------------------ | ----------------- | ---------------------------- |
| http://_<br>https://_ | WebBaseLoader      | WebPageSource     | basic, javascript, recursive |
| github.com/\*         | GitHubFileLoader   | GitHubSource      | file, issues, repo           |
| arxiv.org/\*          | ArxivLoader        | ArxivSource       | basic, pdf                   |
| wikipedia.org/\*      | WikipediaLoader    | WikipediaSource   | basic, sections              |
| youtube.com/watch\*   | YoutubeLoader      | YouTubeSource     | transcript, audio            |
| youtu.be/\*           | YoutubeLoader      | YouTubeSource     | transcript, audio            |
| docs.google.com/\*    | GoogleDriveLoader  | GoogleDocsSource  | basic                        |
| drive.google.com/\*   | GoogleDriveLoader  | GoogleDriveSource | basic, recursive             |
| notion.so/\*          | NotionDBLoader     | NotionSource      | basic, database              |
| airtable.com/\*       | AirtableLoader     | AirtableSource    | basic, tables                |
| twitter.com/\*        | TwitterTweetLoader | TwitterSource     | basic, user, search          |
| reddit.com/r/\*       | RedditPostsLoader  | RedditSource      | posts, comments              |
| linkedin.com/\*       | LinkedInLoader     | LinkedInSource    | basic, profile               |
| confluence.\*         | ConfluenceLoader   | ConfluenceSource  | basic, space                 |
| jira.\*               | JiraLoader         | JiraSource        | basic, issues                |

## Database URIs

| URI Pattern        | Loader              | Source Class        | Strategies               |
| ------------------ | ------------------- | ------------------- | ------------------------ |
| postgresql://\*    | SQLDatabaseLoader   | PostgreSQLSource    | basic, tables, query     |
| mysql://\*         | SQLDatabaseLoader   | MySQLSource         | basic, tables, query     |
| sqlite://\*        | SQLDatabaseLoader   | SQLiteSource        | basic, tables, query     |
| mongodb://\*       | MongodbLoader       | MongoDBSource       | basic, collection, query |
| redis://\*         | RedisLoader         | RedisSource         | basic, keys              |
| snowflake://\*     | SnowflakeLoader     | SnowflakeSource     | basic, tables, query     |
| bigquery://\*      | BigQueryLoader      | BigQuerySource      | basic, tables, query     |
| oracle://\*        | OracleDocLoader     | OracleSource        | basic, tables, query     |
| elasticsearch://\* | ElasticsearchLoader | ElasticsearchSource | basic, index, query      |

## Cloud Storage URIs

| URI Pattern                       | Loader                     | Source Class    | Strategies       |
| --------------------------------- | -------------------------- | --------------- | ---------------- |
| s3://\*                           | S3FileLoader               | S3Source        | file, directory  |
| gs://\*                           | GCSFileLoader              | GCSSource       | file, directory  |
| azure://\*                        | AzureBlobStorageFileLoader | AzureBlobSource | file, container  |
| https://_.blob.core.windows.net/_ | AzureBlobStorageFileLoader | AzureBlobSource | file, container  |
| https://storage.googleapis.com/*  | GCSFileLoader              | GCSSource       | file, directory  |
| dropbox://\*                      | DropboxLoader              | DropboxSource   | basic, recursive |
| onedrive://\*                     | OneDriveFileLoader         | OneDriveSource  | file, directory  |

## Implementation Notes

1. **Multiple Strategies**: Many source classes implement multiple loader strategies to handle different scenarios:
   - **Basic**: Fast, simple loading with minimal processing
   - **Unstructured**: Uses Unstructured.io for better parsing
   - **OCR**: Adds optical character recognition for images/scanned documents
   - **Tables**: Specialized handling for tabular data

2. **Fallback Logic**: When multiple loaders can handle a file type, we implement fallback logic:

   ```
   try:
       # Try primary loader
       return primary_strategy()
   except ImportError:
       # Fall back to secondary loader if dependencies missing
       return fallback_strategy()
   ```

3. **MIME Type Detection**: Beyond file extensions, we also detect content by MIME type:

   ```python
   def detect_mime_type(file_path):
       """Detect MIME type of file for better loader selection."""
       import mimetypes
       import magic  # python-magic library

       # Try file extension first
       mime_type, _ = mimetypes.guess_type(file_path)

       # If that fails, use libmagic
       if not mime_type:
           mime_type = magic.from_file(file_path, mime=True)

       return mime_type
   ```

4. **Loader Factory**: We'll implement a factory function for easy loader creation:

   ```python
   def create_document_loader(path, strategy=None, credentials=None):
       """
       Create the appropriate document loader for any path.

       Args:
           path: File path, URL, or URI to load
           strategy: Optional specific strategy to use
           credentials: Optional credentials for authenticated sources

       Returns:
           DocumentLoader instance
       """
       # 1. Analyze path
       analysis = analyze_path_comprehensive(path)

       # 2. Find matching source types
       matches = registry.find_matching_sources(analysis)

       # 3. Create source instance
       source = registry.create_source_instance(matches[0][0], analysis)

       # 4. Authenticate if needed
       if credentials:
           source.authenticate(credentials)

       # 5. Create loader with specified or default strategy
       return source.create_loader(strategy)
   ```

## Extension Points

Our implementation provides several extension points:

1. **Custom Source Types**: Users can define custom source types:

   ```python
   @auto_source(file_extensions=['.custom'])
   class CustomSource(LocalSource):
       """Custom file format source."""
       file_path: FilePath

       class Config:
           loader_strategies = {
               'basic': {
                   'class': 'CustomLoader',
                   'speed': 'fast',
                   'quality': 'high'
               }
           }

       def create_custom_loader(self):
           # Custom loader implementation
           from custom_module import CustomLoader
           return CustomLoader(self.file_path)
   ```

2. **Custom Analyzers**: Users can add custom path analyzers:

   ```python
   class CustomURIAnalyzer(BasePathAnalyzer):
       """Analyzer for custom URI scheme."""

       def can_analyze(self, path: str) -> bool:
           return path.startswith("custom://")

       def analyze(self, path: str, result: PathAnalysisResult) -> None:
           # Custom analysis implementation
   ```

3. **Custom Loader Strategies**: Users can add strategies to existing sources:

   ```python
   # Add a new strategy to PDFSource
   PDFSource.Config.loader_strategies['custom'] = {
       'class': 'CustomPDFLoader',
       'speed': 'medium',
       'quality': 'high',
       'best_for': ['special_pdfs']
   }

   # Implement the custom loader method
   def create_custom_pdf_loader(self):
       from custom_module import CustomPDFLoader
       return CustomPDFLoader(self.file_path)

   # Add the method to PDFSource
   PDFSource.create_custom_pdf_loader = create_custom_pdf_loader
   ```
