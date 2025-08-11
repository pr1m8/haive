
haive.core.engine.document.loaders.sources.messaging_sources
============================================================

.. py:module:: haive.core.engine.document.loaders.sources.messaging_sources

.. autoapi-nested-parse::

   Messaging and social media source registrations.

   from typing import Any
   This module implements comprehensive messaging and social media loaders from
   langchain_community including Discord, Slack, Twitter, Reddit, WhatsApp,
   Telegram, email systems, and other communication platforms.






Functions
---------

   get_messaging_sources_statistics   validate_messaging_sources   detect_chat_platform
.. autofunction:: get_messaging_sources_statistics
.. autofunction:: validate_messaging_sources
.. autofunction:: detect_chat_platform

Classes
-------

* :py:class:`MessagingPlatform` - Messaging and social media platforms.* :py:class:`ContentType` - Types of content to extract from messaging platforms.* :py:class:`DateRange` - Predefined date ranges for content filtering.* :py:class:`MessagingSource` - Base class for messaging and social media sources.* :py:class:`DiscordSource` - Discord chat and server content source.* :py:class:`SlackSource` - Slack workspace and channel content source.* :py:class:`MicrosoftTeamsSource` - Microsoft Teams content source.* :py:class:`TwitterSource` - Twitter/X tweets and content source.* :py:class:`RedditSource` - Reddit posts and comments source.* :py:class:`MastodonSource` - Mastodon toots and content source.* :py:class:`IMAPEmailSource` - IMAP email server source.* :py:class:`GmailSource` - Gmail API source with OAuth.* :py:class:`WhatsAppSource` - WhatsApp chat export source.* :py:class:`TelegramSource` - Telegram chat export source.* :py:class:`MultiChatExportSource` - Bulk chat export processor.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/MessagingPlatform   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/ContentType   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/DateRange   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/MessagingSource   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/DiscordSource   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/SlackSource   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/MicrosoftTeamsSource   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/TwitterSource   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/RedditSource   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/MastodonSource   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/IMAPEmailSource   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/GmailSource   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/WhatsAppSource   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/TelegramSource   /api_clean/haive/core/engine/document/loaders/sources/messaging_sources/MultiChatExportSource

Package Contents
----------------

