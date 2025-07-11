"""Social Media and Community Web Loaders.

This module contains loaders for social media platforms, forums, and community sites.
"""

import logging
from typing import List, Optional, Sequence

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import WebSource

logger = logging.getLogger(__name__)


class RedditSource(WebSource):
    """Reddit posts and comments loader.

    Can load from:
    - Subreddits
    - User profiles
    - Individual posts
    - Search results
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        mode: str = "subreddit",
        subreddit: Optional[str] = None,
        username: Optional[str] = None,
        post_id: Optional[str] = None,
        search_query: Optional[str] = None,
        categories: List[str] = ["hot", "new", "top"],
        number_posts: int = 10,
        include_comments: bool = True,
        **kwargs,
    ):
        super().__init__(source_path=f"reddit://{mode}", requires_auth=True, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.mode = mode
        self.subreddit = subreddit
        self.username = username
        self.post_id = post_id
        self.search_query = search_query
        self.categories = categories
        self.number_posts = number_posts
        self.include_comments = include_comments

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Reddit loader."""
        try:
            from langchain_community.document_loaders import RedditPostsLoader

            loader_kwargs = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "user_agent": self.user_agent,
                "categories": self.categories,
                "number_posts": self.number_posts,
            }

            if self.mode == "subreddit" and self.subreddit:
                loader_kwargs["mode"] = "subreddit"
                loader_kwargs["search_queries"] = [self.subreddit]
            elif self.mode == "username" and self.username:
                loader_kwargs["mode"] = "username"
                loader_kwargs["search_queries"] = [self.username]
            elif self.mode == "search" and self.search_query:
                loader_kwargs["search_queries"] = [self.search_query]

            return RedditPostsLoader(**loader_kwargs)

        except ImportError:
            logger.warning(
                "RedditPostsLoader not available. Install with: pip install praw"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Reddit loader: {e}")
            return None


class HackerNewsSource(WebSource):
    """Hacker News posts and comments loader."""

    def __init__(
        self,
        mode: str = "top",  # top, new, best, ask, show, job
        limit: int = 10,
        include_comments: bool = True,
        **kwargs,
    ):
        super().__init__(source_path=f"https://news.ycombinator.com/{mode}", **kwargs)
        self.mode = mode
        self.limit = limit
        self.include_comments = include_comments

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Hacker News loader."""
        try:
            from langchain_community.document_loaders import HNLoader

            # HNLoader loads from specific HN URLs
            # We need to fetch the story IDs first
            web_path = f"https://news.ycombinator.com/{self.mode}"

            return HNLoader(
                web_path=web_path,
                load_comments=self.include_comments,
                load_max_comments=self.limit if self.include_comments else 0,
            )

        except ImportError:
            logger.warning("HNLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create HackerNews loader: {e}")
            return None


class TwitterSource(WebSource):
    """Twitter/X posts loader using Twitter API v2."""

    def __init__(
        self,
        bearer_token: str,
        mode: str = "user_timeline",  # user_timeline, search, tweet
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        tweet_id: Optional[str] = None,
        query: Optional[str] = None,
        max_tweets: int = 100,
        include_replies: bool = False,
        include_retweets: bool = True,
        **kwargs,
    ):
        super().__init__(source_path=f"twitter://{mode}", requires_auth=True, **kwargs)
        self.bearer_token = bearer_token
        self.mode = mode
        self.username = username
        self.user_id = user_id
        self.tweet_id = tweet_id
        self.query = query
        self.max_tweets = max_tweets
        self.include_replies = include_replies
        self.include_retweets = include_retweets

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Twitter loader."""
        try:
            from langchain_community.document_loaders import TwitterTweetLoader

            loader_kwargs = {
                "auth_handler": self.bearer_token,
                "number_tweets": self.max_tweets,
            }

            if self.mode == "user_timeline":
                if self.username:
                    return TwitterTweetLoader.from_username(
                        username=self.username, **loader_kwargs
                    )
                elif self.user_id:
                    loader_kwargs["twitter_users"] = [self.user_id]
                    return TwitterTweetLoader(**loader_kwargs)

            elif self.mode == "search" and self.query:
                # Note: TwitterTweetLoader may need customization for search
                logger.warning("Search mode may require custom implementation")
                return None

            elif self.mode == "tweet" and self.tweet_id:
                loader_kwargs["twitter_tweets"] = [self.tweet_id]
                return TwitterTweetLoader(**loader_kwargs)

            return None

        except ImportError:
            logger.warning(
                "TwitterTweetLoader not available. Install with: pip install tweepy"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Twitter loader: {e}")
            return None


class DiscordSource(WebSource):
    """Discord chat history loader."""

    def __init__(
        self,
        channel_id: str,
        token: Optional[str] = None,
        bot_token: Optional[bool] = False,
        limit: Optional[int] = None,
        oldest_first: bool = True,
        **kwargs,
    ):
        super().__init__(
            source_path=f"discord://channel/{channel_id}",
            requires_auth=bool(token),
            **kwargs,
        )
        self.channel_id = channel_id
        self.token = token
        self.bot_token = bot_token
        self.limit = limit
        self.oldest_first = oldest_first

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Discord loader."""
        try:
            from langchain_community.document_loaders import DiscordChatLoader

            return DiscordChatLoader(
                channel_id=self.channel_id,
                token=self.token,
                bot_token=self.bot_token,
                limit=self.limit,
                oldest_first=self.oldest_first,
            )

        except ImportError:
            logger.warning(
                "DiscordChatLoader not available. Install with: pip install discord.py"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Discord loader: {e}")
            return None


class MastodonSource(WebSource):
    """Mastodon toots loader."""

    def __init__(
        self,
        mastodon_accounts: Sequence[str],
        api_base_url: str = "https://mastodon.social",
        access_token: Optional[str] = None,
        number_toots: int = 100,
        exclude_replies: bool = True,
        exclude_reblogs: bool = True,
        **kwargs,
    ):
        super().__init__(
            source_path=api_base_url, requires_auth=bool(access_token), **kwargs
        )
        self.mastodon_accounts = mastodon_accounts
        self.api_base_url = api_base_url
        self.access_token = access_token
        self.number_toots = number_toots
        self.exclude_replies = exclude_replies
        self.exclude_reblogs = exclude_reblogs

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Mastodon loader."""
        try:
            from langchain_community.document_loaders import MastodonTootsLoader

            return MastodonTootsLoader(
                mastodon_accounts=self.mastodon_accounts,
                api_base_url=self.api_base_url,
                access_token=self.access_token,
                number_toots=self.number_toots,
                exclude_replies=self.exclude_replies,
                exclude_reblogs=self.exclude_reblogs,
            )

        except ImportError:
            logger.warning(
                "MastodonTootsLoader not available. Install with: pip install Mastodon.py"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Mastodon loader: {e}")
            return None


class WhatsAppSource(WebSource):
    """WhatsApp chat export loader."""

    def __init__(self, chat_file_path: str, **kwargs):
        super().__init__(source_path=f"file://{chat_file_path}", **kwargs)
        self.chat_file_path = chat_file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a WhatsApp loader."""
        try:
            from langchain_community.document_loaders import WhatsAppChatLoader

            return WhatsAppChatLoader(path=self.chat_file_path)

        except ImportError:
            logger.warning("WhatsAppChatLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create WhatsApp loader: {e}")
            return None


class FacebookChatSource(WebSource):
    """Facebook/Messenger chat export loader."""

    def __init__(self, chat_file_path: str, **kwargs):
        super().__init__(source_path=f"file://{chat_file_path}", **kwargs)
        self.chat_file_path = chat_file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Facebook chat loader."""
        try:
            from langchain_community.document_loaders import FacebookChatLoader

            return FacebookChatLoader(path=self.chat_file_path)

        except ImportError:
            logger.warning("FacebookChatLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create Facebook chat loader: {e}")
            return None


class IFixitSource(WebSource):
    """iFixit repair guides and manuals loader."""

    def __init__(
        self,
        web_path: str,
        mode: str = "devices",  # devices, guides, categories
        **kwargs,
    ):
        super().__init__(source_path=web_path, **kwargs)
        self.web_path = web_path
        self.mode = mode

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an iFixit loader."""
        try:
            from langchain_community.document_loaders import IFixitLoader

            return IFixitLoader(
                web_path=self.web_path,
                mode=self.mode,
            )

        except ImportError:
            logger.warning("IFixitLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create iFixit loader: {e}")
            return None


class IMSDbSource(WebSource):
    """Internet Movie Script Database loader."""

    def __init__(self, web_path: str, **kwargs):
        super().__init__(source_path=web_path, **kwargs)
        self.web_path = web_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an IMSDb loader."""
        try:
            from langchain_community.document_loaders import IMSDbLoader

            return IMSDbLoader(web_path=self.web_path)

        except ImportError:
            logger.warning("IMSDbLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create IMSDb loader: {e}")
            return None


class BiliBiliSource(WebSource):
    """BiliBili video transcripts loader."""

    def __init__(
        self,
        video_urls: List[str],
        sessdata: Optional[str] = None,
        bili_jct: Optional[str] = None,
        buvid3: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(source_path="https://www.bilibili.com", **kwargs)
        self.video_urls = video_urls
        self.sessdata = sessdata
        self.bili_jct = bili_jct
        self.buvid3 = buvid3

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a BiliBili loader."""
        try:
            from langchain_community.document_loaders import BiliBiliLoader

            # BiliBili requires cookies for some videos
            cookies = {}
            if self.sessdata:
                cookies["SESSDATA"] = self.sessdata
            if self.bili_jct:
                cookies["bili_jct"] = self.bili_jct
            if self.buvid3:
                cookies["buvid3"] = self.buvid3

            return BiliBiliLoader(
                video_urls=self.video_urls,
                cookies=cookies if cookies else None,
            )

        except ImportError:
            logger.warning(
                "BiliBiliLoader not available. Install with: pip install bilibili-api-python"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create BiliBili loader: {e}")
            return None


# Export social media sources
__all__ = [
    "RedditSource",
    "HackerNewsSource",
    "TwitterSource",
    "DiscordSource",
    "MastodonSource",
    "WhatsAppSource",
    "FacebookChatSource",
    "IFixitSource",
    "IMSDbSource",
    "BiliBiliSource",
]
