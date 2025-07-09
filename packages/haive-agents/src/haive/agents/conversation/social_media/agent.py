import random
from typing import Any, Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.logging.rich_logger import LogLevel, get_logger
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from pydantic import Field

from haive.agents.conversation.base.agent import BaseConversationAgent
from haive.agents.conversation.social_media.models import (
    LikePostInput,
    ReplyPostInput,
    SharePostInput,
)
from haive.agents.conversation.social_media.state import SocialMediaState
from haive.agents.simple.agent import SimpleAgent

logger = get_logger(__name__)
logger.set_level(LogLevel.WARNING)


class SocialMediaConversation(BaseConversationAgent):
    """Social media style conversation with engagement mechanics.

    Features:
    - Likes and reactions
    - Replies and threads
    - Shares/retweets
    - Viral mechanics
    - Hashtag tracking
    """

    mode: Literal["social_media"] = Field(default="social_media")

    # Platform configuration
    platform_type: Literal["twitter", "instagram", "tiktok", "generic"] = Field(
        default="generic"
    )
    viral_threshold: int = Field(default=10)

    # Engagement settings
    enable_likes: bool = Field(default=True)
    enable_shares: bool = Field(default=True)
    enable_reactions: bool = Field(default=False)
    max_posts_per_round: int = Field(default=3)

    # Character limits by platform
    char_limits: dict[str, int] = Field(
        default_factory=lambda: {
            "twitter": 280,
            "instagram": 2200,
            "tiktok": 150,
            "generic": 500,
        }
    )

    def get_conversation_state_schema(self) -> type:
        """Use social media state schema."""
        return SocialMediaState

    def _create_orchestrator_engine(self) -> AugLLMConfig:
        """Create orchestrator with social media context."""
        return AugLLMConfig(
            name="social_orchestrator",
            system_message=(
                f"You are orchestrating a {self.platform_type} conversation. "
                f"Topic: {self.topic}. Encourage engagement and viral content."
            ),
        )

    def _compile_participants(self):
        """Compile participants with social media tools."""
        # First compile normally
        super()._compile_participants()

        # Then add social media tools to each agent
        if self.enable_likes or self.enable_shares:
            self._add_social_tools_to_agents()

    def _add_social_tools_to_agents(self):
        """Add social media interaction tools to agents."""
        # Create tools
        tools = []

        if self.enable_likes:
            like_tool = StructuredTool(
                name="like_post",
                description="Like another user's post",
                func=self._like_post_handler,
                args_schema=LikePostInput,
            )
            tools.append(like_tool)

        reply_tool = StructuredTool(
            name="reply_to_post",
            description="Reply to another user's post",
            func=self._reply_post_handler,
            args_schema=ReplyPostInput,
        )
        tools.append(reply_tool)

        if self.enable_shares:
            share_tool = StructuredTool(
                name="share_post",
                description="Share/retweet another user's post",
                func=self._share_post_handler,
                args_schema=SharePostInput,
            )
            tools.append(share_tool)

        # Add tools to each agent's engine
        for name, agent in self._compiled_agents.items():
            if hasattr(agent, "engine") and hasattr(agent.engine, "tools"):
                # Add tools to existing tools list
                if not agent.engine.tools:
                    agent.engine.tools = []
                agent.engine.tools.extend(tools)  # type: ignore

                # Force tool use for more engagement
                agent.engine.force_tool_use = False  # Let them choose
                agent.engine.tool_choice_mode = "auto"

    def _like_post_handler(self, post_author: str, reason: str | None = None) -> str:
        """Handler for like_post tool."""
        # This will be processed in process_response
        return f"Liked @{post_author}'s post" + (f" because {reason}" if reason else "")

    def _reply_post_handler(self, reply_to: str, content: str) -> str:
        """Handler for reply_to_post tool."""
        return f"@{reply_to} {content}"

    def _share_post_handler(
        self, original_author: str, comment: str | None = None
    ) -> str:
        """Handler for share_post tool."""
        if comment:
            return f"RT @{original_author}: {comment}"
        return f"RT @{original_author}"

    def _create_initial_message(self) -> BaseMessage:
        """Create platform-specific initial message."""
        emoji_map = {
            "twitter": "🐦",
            "instagram": "📸",
            "tiktok": "🎵",
            "generic": "💬",
        }

        emoji = emoji_map.get(self.platform_type, "💬")
        char_limit = self.char_limits.get(self.platform_type, 500)

        return HumanMessage(
            content=f"{emoji} New thread: {self.topic}\n"
            f"Platform: {self.platform_type} (max {char_limit} chars)\n"
            f"Share your thoughts! Go viral at {self.viral_threshold} likes 🔥"
        )

    def select_speaker(self, state: SocialMediaState) -> dict[str, Any]:
        """Select speakers based on engagement dynamics."""
        speakers = state.speakers

        # Calculate engagement scores
        engagement_scores = {}
        for speaker in speakers:
            likes = state.likes.get(speaker, 0)
            posts = state.posts_count.get(speaker, 1)  # Avoid division by zero
            engagement = likes / posts if posts > 0 else 0

            # Boost for recent engagement
            if speaker == state.current_speaker:
                engagement *= 0.8  # Slight penalty for just posting

            engagement_scores[speaker] = engagement

        # Weighted random selection based on engagement
        total_engagement = sum(engagement_scores.values()) or 1
        weights = [engagement_scores[s] / total_engagement for s in speakers]

        # Add base probability
        weights = [0.2 + 0.8 * w for w in weights]

        # Select multiple speakers who might post
        selected = []
        for speaker, weight in zip(speakers, weights, strict=False):
            if random.random() < weight:
                selected.append(speaker)

        # Ensure at least one speaker
        if not selected and speakers:
            selected = [random.choice(speakers)]

        # Limit to max posts per round
        selected = selected[: self.max_posts_per_round]

        if len(selected) > 1:
            return {"current_speaker": selected[0], "pending_speakers": selected[1:]}
        return {"current_speaker": selected[0] if selected else None}

    def _prepare_agent_input(
        self, state: SocialMediaState, agent_name: str
    ) -> dict[str, Any]:
        """Prepare input with social media context."""
        base_input = super()._prepare_agent_input(state, agent_name)

        # Add social media context
        likes = state.likes.get(agent_name, 0)
        followers = len(state.followers.get(agent_name, set()))
        trending = state.trending_topics[:3] if state.trending_topics else []

        context_msg = SystemMessage(
            content=f"""[@{agent_name}]
Stats: {likes} likes | {followers} followers
Trending: {', '.join(trending) if trending else 'Nothing trending'}
Keep it under {self.char_limits.get(state.platform_type, 500)} characters!"""
        )

        # Show recent posts in feed style
        recent_posts = []
        for msg in state.messages[-5:]:
            if isinstance(msg, AIMessage) and hasattr(msg, "name"):
                post_likes = state.likes.get(str(msg.name), 0)
                recent_posts.append(
                    f"@{msg.name}: {msg.content[:100]}... ({post_likes}❤️)"
                )

        if recent_posts:
            feed_msg = SystemMessage(
                content="Recent posts:\n" + "\n".join(recent_posts)
            )
            base_input["messages"] = [context_msg, feed_msg] + base_input.get(
                "messages", []
            )
        else:
            base_input["messages"] = [context_msg] + base_input.get("messages", [])

        return base_input

    def process_response(self, state: SocialMediaState) -> dict[str, Any]:
        """Process social media engagement."""
        update = {}

        if not state.current_speaker or not state.messages:
            return update

        # Get last message
        last_msg = state.messages[-1]
        if not isinstance(last_msg, AIMessage) or not hasattr(last_msg, "name"):
            return update

        speaker = last_msg.name
        content = last_msg.content

        # Update post count
        posts_count = dict(state.posts_count)
        posts_count[str(speaker)] = posts_count.get(str(speaker), 0) + 1
        update["posts_count"] = posts_count

        # Process tool calls if any
        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            likes = dict(state.likes)
            shares = dict(state.shares)

            for tool_call in last_msg.tool_calls:
                if tool_call["name"] == "like_post":
                    target = tool_call["args"].get("post_author")
                    if target and target != speaker:
                        likes[target] = likes.get(target, 0) + 1

                elif tool_call["name"] == "share_post":
                    target = tool_call["args"].get("original_author")
                    if target:
                        shares[target] = shares.get(target, 0) + 1
                        likes[target] = likes.get(target, 0) + 2  # Shares worth more

            update["likes"] = likes
            update["shares"] = shares

        # Simulate organic engagement
        likes = update.get("likes", dict(state.likes))

        # Random likes based on content
        if any(emoji in content for emoji in ["🔥", "💯", "🚀", "❤️"]):
            bonus_likes = random.randint(1, 3)
            likes[speaker] = likes.get(speaker, 0) + bonus_likes

        # Random chance of going viral
        if random.random() < 0.1:  # 10% chance
            viral_likes = random.randint(5, 15)
            likes[speaker] = likes.get(speaker, 0) + viral_likes

            # Add to viral posts
            viral_posts = list(state.viral_posts)
            viral_posts.append((str(speaker), str(content)[:100]))  # type: ignore
            update["viral_posts"] = viral_posts

        update["likes"] = likes

        # Extract hashtags
        hashtags = [word for word in str(content).split() if word.startswith("#")]
        if hashtags:
            hashtags_used = dict(state.hashtags_used)
            if speaker not in hashtags_used:
                hashtags_used[str(speaker)] = []
            hashtags_used[str(speaker)].extend(hashtags)
            update["hashtags_used"] = hashtags_used

            # Update trending
            all_hashtags = []
            for tags in hashtags_used.values():
                all_hashtags.extend(tags)

            # Count frequency
            hashtag_counts = {}
            for tag in all_hashtags:
                hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1

            # Get top trending
            trending = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
            update["trending_topics"] = [tag for tag, _ in trending[:5]]

        return update

    def _check_custom_end_conditions(
        self, state: SocialMediaState
    ) -> dict[str, Any] | None:
        """Check for viral threshold."""
        # Check if anyone went viral
        for speaker, like_count in state.likes.items():
            if like_count >= state.viral_threshold:
                viral_msg = SystemMessage(
                    content=f"🎉 @{speaker} went viral with {like_count} likes! Thread closed. 🔥"
                )
                return {"messages": [viral_msg], "conversation_ended": True}

        return None

    def _create_conclusion(
        self, state: SocialMediaState, reason: str
    ) -> dict[str, Any]:
        """Create social media style conclusion."""
        # Get top posts
        top_posts = sorted(state.likes.items(), key=lambda x: x[1], reverse=True)[:3]

        summary_parts = ["📊 Thread Summary:"]
        summary_parts.append(f"Topic: {self.topic}")
        summary_parts.append(f"Total posts: {sum(state.posts_count.values())}")

        if top_posts:
            summary_parts.append("\n🏆 Top Posts:")
            for i, (author, likes) in enumerate(top_posts, 1):
                summary_parts.append(f"{i}. @{author} - {likes} likes")

        if state.trending_topics:
            summary_parts.append(
                f"\n📈 Trending: {', '.join(state.trending_topics[:3])}"
            )

        conclusion_msg = SystemMessage(content="\n".join(summary_parts))

        return {"messages": [conclusion_msg], "conversation_ended": True}

    @classmethod
    def create_twitter_thread(
        cls, topic: str, personas: dict[str, str], viral_threshold: int = 10, **kwargs
    ):
        """Create a Twitter-style conversation thread.

        Args:
            topic: Thread topic
            personas: Dictionary mapping names to persona descriptions
            viral_threshold: Likes needed to go viral
            **kwargs: Additional configuration
        """
        agents = {}

        for name, persona in personas.items():
            engine = AugLLMConfig(
                name=f"{name.lower()}_engine",
                system_message=(
                    f"You are @{name}, {persona}. "
                    "Post in Twitter style: short, punchy, with emojis. "
                    "Use hashtags when relevant. Engage with others using @mentions. "
                    "You can like and retweet posts you find interesting."
                ),
                temperature=0.9,
                max_tokens=100,  # Keep responses short
            )
            agents[name] = SimpleAgent(name=f"{name}_agent", engine=engine)

        return cls(
            participant_agents=agents,
            topic=topic,
            platform_type="twitter",
            viral_threshold=viral_threshold,
            **kwargs,
        )
