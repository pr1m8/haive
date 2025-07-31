"""Example core module.

This module provides example functionality for the Haive framework.

Functions:
    example_twitter_thread: Example Twitter Thread functionality.
    example_instagram_discussion: Example Instagram Discussion functionality.
    example_tiktok_comments: Example Tiktok Comments functionality.
"""

# examples/conversation/social_media_example.py
"""Examples for social media style conversations with engagement mechanics."""

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, SystemMessage

from haive.agents.conversation.social_media.agent import SocialMediaConversation
from haive.agents.simple.agent import SimpleAgent

# Set logging
logging.getLogger("haive").setLevel(logging.WARNING)


def example_twitter_thread() -> None:
    """Twitter-style conversation thread with viral mechanics."""
    # Create Twitter thread
    thread = SocialMediaConversation.create_twitter_thread(
        topic="🚀 Just shipped our new AI framework! It's 10x faster than before. AMA!",
        personas={
            "TechInfluencer": "popular tech influencer with 100k followers, loves new tech",
            "DevNewbie": "curious junior developer learning about AI",
            "AISkeptic": "concerned about AI safety and performance claims",
            "StartupFounder": "fellow startup founder interested in the tech stack",
        },
        viral_threshold=8,
        max_rounds=10,
    )

    # Run thread
    result = thread.invoke({})

    # Display thread with engagement metrics
    final_likes = result.get("likes", {})
    final_shares = result.get("shares", {})

    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            author = msg.name
            likes = final_likes.get(author, 0)
            shares = final_shares.get(author, 0)

            # Show engagement
            engagement = []
            if likes > 0:
                engagement.append(f"❤️ {likes}")
            if shares > 0:
                engagement.append(f"🔁 {shares}")
            if engagement:
                pass

        elif isinstance(msg, SystemMessage):
            pass

    # Show trending hashtags
    trending = result.get("trending_topics", [])
    if trending:
        pass


def example_instagram_discussion() -> None:
    """Instagram-style post with comments."""
    # Create Instagram discussion
    personas = {
        "FitnessGuru": "fitness influencer sharing workout tips",
        "Nutritionist": "certified nutritionist providing diet advice",
        "GymNewbie": "someone just starting their fitness journey",
        "Motivator": "positive person who encourages others",
    }

    agents = {}
    for name, persona in personas.items():
        agents[name] = SimpleAgent(
            name=name,
            engine=AugLLMConfig(
                name=f"{name.lower()}_engine",
                system_message=(
                    f"You are @{name}, {persona}. "
                    "Post Instagram-style with emojis and positivity. "
                    "Can use #hashtags. Keep it visual and inspiring. "
                    "Engage with others' posts."
                ),
                temperature=0.8,
                max_tokens=150,
            ),
        )

    conversation = SocialMediaConversation(
        participant_agents=agents,
        topic="💪 30-Day Fitness Challenge - Who's in? Drop your goals below! 👇",
        platform_type="instagram",
        viral_threshold=15,
        max_rounds=8,
    )

    result = conversation.invoke({})

    # Display Instagram-style

    post_count = 0
    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            post_count += 1
            author = msg.name
            likes = result.get("likes", {}).get(author, 0)

            # Format as Instagram comment
            if likes > 0:
                pass


def example_tiktok_comments() -> None:
    """TikTok-style video comments."""
    # TikTok personas
    personas = {
        "Creator": "the video creator responding to comments",
        "Fan1": "enthusiastic young fan using Gen Z slang",
        "Hater": "typical internet troll (but not too mean)",
        "Expert": "someone who actually knows about the topic",
    }

    agents = {}
    for name, persona in personas.items():
        agents[name] = SimpleAgent(
            name=name,
            engine=AugLLMConfig(
                name=f"{name.lower()}_engine",
                system_message=(
                    f"You are @{name}, {persona}. "
                    "Comment in TikTok style: short, trendy, lots of emojis. "
                    "Use popular phrases and keep it under 150 chars. "
                    "Can reply to others with @mentions."
                ),
                temperature=0.9,
                max_tokens=50,
            ),
        )

    conversation = SocialMediaConversation(
        participant_agents=agents,
        topic="POV: You're trying to code at 3am and your code finally works 😭✨",
        platform_type="tiktok",
        viral_threshold=20,
        max_rounds=10,
        max_posts_per_round=2,
    )

    result = conversation.invoke({})

    # Display TikTok style

    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            author = msg.name
            likes = result.get("likes", {}).get(author, 0)

            if likes > 0:
                pass


def example_linkedin_professional() -> None:
    """LinkedIn professional discussion."""
    # LinkedIn professionals
    professionals = {
        "ThoughtLeader": SimpleAgent(
            name="ThoughtLeader",
            engine=AugLLMConfig(
                name="leader_engine",
                system_message=(
                    "You are a LinkedIn thought leader. Post insights about leadership and innovation. "
                    "Use professional tone with some emojis. Share actionable advice."
                ),
                temperature=0.7,
            ),
        ),
        "Recruiter": SimpleAgent(
            name="Recruiter",
            engine=AugLLMConfig(
                name="recruiter_engine",
                system_message=(
                    "You are a tech recruiter. Engage about hiring trends and talent. "
                    "Professional but approachable. Can mention job opportunities."
                ),
                temperature=0.7,
            ),
        ),
        "Engineer": SimpleAgent(
            name="Engineer",
            engine=AugLLMConfig(
                name="engineer_engine",
                system_message=(
                    "You are a senior engineer. Share technical insights and career advice. "
                    "Be helpful and mentor-like in responses."
                ),
                temperature=0.6,
            ),
        ),
        "Student": SimpleAgent(
            name="Student",
            engine=AugLLMConfig(
                name="student_engine",
                system_message=(
                    "You are a CS student looking for opportunities. "
                    "Ask questions and engage genuinely. Show enthusiasm."
                ),
                temperature=0.8,
            ),
        ),
    }

    conversation = SocialMediaConversation(
        participant_agents=professionals,  # type: ignore
        topic="🎯 The most important skill for engineers in 2024 isn't coding. It's learning how to learn. Thoughts?",
        platform_type="generic",  # LinkedIn-style
        viral_threshold=12,
        max_rounds=6,
        enable_shares=True,
    )

    result = conversation.invoke({})

    # Display LinkedIn style

    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            author = msg.name
            likes = result.get("likes", {}).get(author, 0)
            shares = result.get("shares", {}).get(author, 0)

            reactions = []
            if likes > 0:
                reactions.append(f"👍 {likes}")
            if shares > 0:
                reactions.append(f"♻️ {shares} reposts")
            if reactions:
                pass


def example_viral_moment() -> None:
    """Demonstration of viral mechanics."""
    # Create scenario likely to go viral
    personas = {
        "CelebChef": "celebrity chef with millions of followers",
        "FoodCritic": "well-known food critic",
        "HomeCook": "enthusiastic home cook",
        "Comedian": "comedian who makes food puns",
    }

    agents = {}
    for name, persona in personas.items():
        agents[name] = SimpleAgent(
            name=name,
            engine=AugLLMConfig(
                name=f"{name.lower()}_engine",
                system_message=(
                    f"You are @{name}, {persona}. "
                    "React to the cooking fail with humor and personality. "
                    "Use emojis and be entertaining. Can like and share posts."
                ),
                temperature=0.9,
            ),
        )

    conversation = SocialMediaConversation(
        participant_agents=agents,
        topic="😅 Tried to make a soufflé... it's now a pancake. Chef life! 👨‍🍳 #CookingFail",
        platform_type="twittef",
        viral_threshold=5,  # Lower threshold for demo
        max_rounds=8,
    )

    result = conversation.run({}, debug=True)

    # Show viral progression

    for msg in result.get("messages", []):
        if isinstance(msg, AIMessage) and hasattr(msg, "name"):
            author = msg.name
            current_likes = result.get("likes", {}).get(author, 0)

            if current_likes > 0:
                pass

            # Check if went viral
            if current_likes >= conversation.viral_threshold:
                pass


if __name__ == "__main__":
    example_twitter_thread()
