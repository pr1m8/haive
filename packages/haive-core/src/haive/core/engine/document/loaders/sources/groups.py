from haive.core.engine.loaders.sources.types import SourceType


class SourceGroups:
    WEB = {
        SourceType.URL,
        SourceType.WEB,
        SourceType.SITEMAP,
        SourceType.RECURSIVE_URL,
        SourceType.READTHEDOCS,
        SourceType.RSS,
        SourceType.WIKIPEDIA,
        SourceType.PLAYWRIGHT,
        SourceType.SELENIUM,
        SourceType.BROWSERLESS,
        SourceType.BROWSERBASE,
        SourceType.BRAVE_SEARCH,
        SourceType.COLLEGE_CONFIDENTIAL,
        SourceType.HACKER_NEWS,
        SourceType.NEWS_URL,
        SourceType.FIRECRAWL,
        SourceType.SCRAPFLY,
        SourceType.SCRAPINGANT,
    }

    FILE = {
        SourceType.FILE,
        SourceType.DIRECTORY,
        SourceType.PDF,
        SourceType.PDF_PYMUPDF,
        SourceType.PDF_PDFMINER,
        SourceType.PDF_PDFPLUMBER,
        SourceType.PDF_UNSTRUCTURED,
        SourceType.PDF_PYPDFIUM2,
        SourceType.CSV,
        SourceType.DOCX,
        SourceType.EXCEL,
        SourceType.JSON,
        SourceType.HTML,
        SourceType.MARKDOWN,
        SourceType.XML,
        SourceType.SRT,
        SourceType.RTF,
        SourceType.EPUB,
        SourceType.RST,
        SourceType.ODT,
        SourceType.TOML,
        SourceType.PYTHON,
        SourceType.NOTEBOOK,
        SourceType.BIBTEX,
        SourceType.VSDX,
        SourceType.MHTML,
        SourceType.CHM,
    }

    REPO = {
        SourceType.GITHUB,
        SourceType.GITHUB_ISSUES,
        SourceType.GIT,
        SourceType.GITBOOK,
        SourceType.CONFLUENCE,
        SourceType.NOTION,
        SourceType.NOTION_DIRECTORY,
        SourceType.TRELLO,
        SourceType.AIRTABLE,
        SourceType.JOPLIN,
        SourceType.OBSIDIAN,
        SourceType.DOCUSAURUS,
        SourceType.QUIP,
        SourceType.ROAM,
        SourceType.LAKEFS,
    }

    MEDIA = {
        SourceType.IMAGE,
        SourceType.IMAGE_CAPTION,
        SourceType.AUDIO,
        SourceType.YOUTUBE,
        SourceType.YOUTUBE_AUDIO,
        SourceType.IMDB,
        SourceType.IFIXIT,
        SourceType.FIGMA,
        SourceType.BILIBILI,
    }

    DATABASE = {
        SourceType.DATABASE,
        SourceType.SQLITE,
        SourceType.MONGODB,
        SourceType.ASTRADB,
        SourceType.SNOWFLAKE,
        SourceType.BIGQUERY,
        SourceType.DUCKDB,
        SourceType.ATHENA,
        SourceType.CASSANDRA,
        SourceType.COUCHBASE,
        SourceType.ORACLE,
        SourceType.ORACLE_ADB,
        SourceType.ORACLE_AI,
        SourceType.POSTGRESQL,
        SourceType.TIDB,
        SourceType.ROCKSET,
        SourceType.MAXCOMPUTE,
        SourceType.FAUNA,
        SourceType.KINETICA,
        SourceType.SURREALDB,
        SourceType.GLUE_CATALOG,
        SourceType.DATAFRAME,
        SourceType.POLARS_DATAFRAME,
        SourceType.PYSPARK_DATAFRAME,
        SourceType.GEODATAFRAME,
        SourceType.XORBITS,
        SourceType.CUBE_SEMANTIC,
    }

    SOCIAL = {
        SourceType.EMAIL,
        SourceType.OUTLOOK,
        SourceType.SLACK,
        SourceType.TELEGRAM,
        SourceType.TELEGRAM_CHAT_API,
        SourceType.DISCORD,
        SourceType.FACEBOOK,
        SourceType.WHATSAPP,
        SourceType.TWITTER,
        SourceType.MASTODON,
        SourceType.REDDIT,
        SourceType.CHATGPT,
        SourceType.EVERNOTE,
        SourceType.ETHERSCAN,
        SourceType.SPREADLY,
        SourceType.STRIPE,
        SourceType.IUGU,
        SourceType.MODERN_TREASURY,
        SourceType.DATADOG_LOGS,
        SourceType.BLOCKCHAIN,
        SourceType.MINTBASE,
        SourceType.LARKSUITE_DOC,
        SourceType.PSYCHIC,
    }

    CLOUD = {
        SourceType.AZURE_BLOB,
        SourceType.S3,
        SourceType.GCS,
        SourceType.GOOGLE_DRIVE,
        SourceType.ONEDRIVE,
        SourceType.ONEDRIVE_FILE,
        SourceType.DROPBOX,
        SourceType.SHAREPOINT,
        SourceType.OBS_DIRECTORY,
        SourceType.OBS_FILE,
        SourceType.TENCENT_COS_DIRECTORY,
        SourceType.TENCENT_COS_FILE,
        SourceType.BAIDU_BOS_DIRECTORY,
        SourceType.BAIDU_BOS_FILE,
    }

    EDUCATION = {
        SourceType.BLACKBOARD,
        SourceType.ONENOTE,
    }

    LITERATURE = {
        SourceType.GUTENBERG,
        SourceType.MEDIAWIKI,
        SourceType.AZLYRICS,
    }

    RESEARCH_AI = {
        SourceType.PUBMED,
        SourceType.ARXIV,
        SourceType.HUGGINGFACE_MODEL,
        SourceType.HUGGINGFACE_DATASET,
        SourceType.TENSORFLOW_DATASET,
        SourceType.ARCGIS,
        SourceType.OPEN_CITY_DATA,
        SourceType.NEEDLE,
        SourceType.DOCUGAMI,
        SourceType.LLM_SHERPA,
    }

    OTHER = {
        SourceType.WEATHER,
        SourceType.API,
        SourceType.UNSTRUCTURED,
        SourceType.UNSTRUCTURED_API,
        SourceType.DEDOC,
        SourceType.DEDOC_API,
        SourceType.APIFY,
        SourceType.PEBBLO,
        SourceType.CONCURRENT,
        SourceType.DIFFBOT,
        SourceType.AZURE_AI_DATA,
        SourceType.AZURE_AI_DOCUMENT,
        SourceType.ACREOM,
        SourceType.SPIDER,
        SourceType.CONLLU,
        SourceType.MERGED_DATA,
        SourceType.GOOGLE_SPEECH_TO_TEXT,
        SourceType.ASSEMBLYAI_AUDIO,
        SourceType.TO_MARKDOWN,
        SourceType.YUQUE,
    }


# Optional: Reverse Mapping for quick lookup
SOURCE_TO_GROUP: Dict[SourceType, str] = {}
for group_name in dir(SourceGroups):
    if group_name.startswith("_"):
        continue
    group = getattr(SourceGroups, group_name)
    if isinstance(group, set):
        for source in group:
            SOURCE_TO_GROUP[source] = group_name
