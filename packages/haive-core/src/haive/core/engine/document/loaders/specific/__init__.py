"""Specific Loader Implementations.

This module contains specialized loader implementations for different source types.
"""

# Database sources - only import what exists
from haive.core.engine.document.loaders.specific.database import (
    MongoDBSource,
    PostgreSQLSource,
)

# Cloud sources - temporarily commented out until implemented
# from .cloud import (
#     S3Source,
#     GCSSource,
#     AzureBlobSource,
#     GoogleDriveSource,
#     OneDriveSource,
#     DropboxSource,
#     SharePointSource,
# )

# Web sources - temporarily commented out until verified
# from .web import (
#     GitHubSource,
#     ArXivSource,
#     WikipediaSource,
#     PlaywrightWebSource,
#     BasicWebSource,
#     SitemapSource,
#     SlackSource,
#     TelegramSource,
#     TwitterSource,
#     JiraSource,
#     ConfluenceSource,
#     NewsAPISource,
#     RSSFeedSource,
#     HuggingFaceDatasetSource,
#     PubMedSource,
#     FireCrawlSource,
#     CrawlerSource,
# )

# # Social media and community sources
# from .web_social import (
#     RedditSource,
#     HackerNewsSource,
#     TwitterSource as TwitterSocialSource,
#     DiscordSource,
#     MastodonSource,
#     WhatsAppSource,
#     FacebookChatSource,
#     IFixitSource,
#     IMSDbSource,
#     BiliBiliSource,
# )

# # Enhanced GitHub sources
# from .web_github_enhanced import (
#     GitHubDiscussionsSource,
#     GitHubGistsSource,
#     GitHubReleasesSource,
#     GitHubActionsSource,
#     GitHubWikiSource,
# )

# # Enhanced HuggingFace sources
# from .web_huggingface_enhanced import (
#     HuggingFacePapersSource,
#     HuggingFaceCollectionsSource,
#     HuggingFaceOrganizationsSource,
#     HuggingFaceExtendedDatasetSource,
#     HuggingFaceModelCardSource,
# )

# # API-based web sources
# from .web_api import (
#     BraveSearchSource,
#     GoogleSearchSource,
#     ApifyDatasetSource,
#     DiffbotSource,
#     ScrapingBeeSource,
#     ScrapflySource,
#     NewsAPISource as NewsAPISourceEnhanced,
#     AssemblyAITranscriptSource,
#     EtherscanSource,
# )

# # Service sources
# from .services import (
#     NotionDBSource,
#     ObsidianSource,
#     EvernoteSource,
#     OneNoteSource,
#     RoamSource,
#     TrelloSource,
#     AsanaSource,
#     AirtableSource,
# )

# # Office file sources
# from .files_office import (
#     WordDocumentSource,
#     ExcelSource,
#     PowerPointSource,
#     ODTSource,
#     ODSSource,
#     ODPSource,
#     RTFSource,
# )

# # Data file sources
# from .files_data import (
#     CSVSource,
#     TSVSource,
#     JSONSource,
#     XMLSource,
#     YAMLSource,
#     TOMLSource,
# )

# # Code file sources
# from .files_code import (
#     PythonCodeSource,
#     JupyterNotebookSource,
#     JavaScriptSource,
#     CppSource,
#     JavaSource,
#     GoSource,
#     RustSource,
#     RubySource,
#     ShellScriptSource,
# )

# # Text file sources
# from .files_text import (
#     TextFileSource,
#     MarkdownSource,
#     ReStructuredTextSource,
#     LaTeXSource,
#     OrgModeSource,
#     AsciiDocSource,
# )

# # Media file sources
# from .files_media import (
#     PDFSource,
#     ImageSource,
#     SubtitleSource,
#     EPubSource,
#     MHTMLSource,
#     HTMLSource,
#     CHMSource,
# )

# # Scientific file sources
# from .files_scientific import (
#     BibtexSource,
#     CONLLUSource,
#     MathMLSource,
#     FortranSource,
#     MatlabSource,
#     RSource,
# )

# Export only the sources that are actually implemented
__all__ = [
    # Database sources
    "MongoDBSource",
    "PostgreSQLSource",
]
