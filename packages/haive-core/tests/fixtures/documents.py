from langchain_core.documents import Document

# Conversation Flow Documents (Human-AI with tool calls)
conversation_documents = [
    Document(
        page_content="Human: Can you help me find restaurants near Times Square in New York?",
        metadata={
            "category": "conversation",
            "message_type": "human",
            "turn": 1,
            "intent": "restaurant_search",
        },
    ),
    Document(
        page_content="AI: I'll help you find restaurants near Times Square. Let me search for current options in that area.",
        metadata={
            "category": "conversation",
            "message_type": "ai",
            "turn": 2,
            "has_tool_call": True,
        },
    ),
    Document(
        page_content="Tool Call: search_restaurants(location='Times Square, NYC', cuisine='any', rating_min=4.0)",
        metadata={
            "category": "conversation",
            "message_type": "tool_call",
            "turn": 3,
            "tool_name": "search_restaurants",
        },
    ),
    Document(
        page_content="Tool Result: Found 15 restaurants - Joe Allen Restaurant (4.2★), The View Restaurant (4.1★), Carmine's Italian (4.3★)",
        metadata={
            "category": "conversation",
            "message_type": "tool_result",
            "turn": 4,
            "results_count": 15,
        },
    ),
    Document(
        page_content="AI: I found several great restaurants near Times Square! Here are the top-rated options: Joe Allen Restaurant (4.2 stars) - known for American cuisine, The View Restaurant (4.1 stars) - revolving restaurant with city views, and Carmine's Italian (4.3 stars) - family-style Italian dining.",
        metadata={
            "category": "conversation",
            "message_type": "ai",
            "turn": 5,
            "recommendations_count": 3,
        },
    ),
    Document(
        page_content="Human: Great! Can you book a table at Carmine's for tonight at 7 PM for 4 people?",
        metadata={
            "category": "conversation",
            "message_type": "human",
            "turn": 6,
            "intent": "reservation_request",
        },
    ),
    Document(
        page_content="AI: I'll attempt to make a reservation at Carmine's for you.",
        metadata={
            "category": "conversation",
            "message_type": "ai",
            "turn": 7,
            "has_tool_call": True,
        },
    ),
    Document(
        page_content="Tool Call: make_reservation(restaurant='Carmines Italian', time='19:00', date='today', party_size=4)",
        metadata={
            "category": "conversation",
            "message_type": "tool_call",
            "turn": 8,
            "tool_name": "make_reservation",
        },
    ),
]

# Social Media Posts Documents
social_media_documents = [
    Document(
        page_content="Just tried the new AI coding assistant and it's absolutely game-changing! Cut my debugging time in half 🚀 #AI #Coding #ProductivityHack",
        metadata={
            "category": "social_media",
            "platform": "twitter",
            "sentiment": "positive",
            "hashtags": ["AI", "Coding", "ProductivityHack"],
            "engagement_type": "review",
        },
    ),
    Document(
        page_content="Unpopular opinion: Remote work is making us lose the art of spontaneous collaboration. Sometimes the best ideas come from random hallway conversations 💭",
        metadata={
            "category": "social_media",
            "platform": "linkedin",
            "sentiment": "neutral",
            "engagement_type": "opinion",
            "topic": "remote_work",
        },
    ),
    Document(
        page_content="BREAKING: Major tech company announces $50B investment in quantum computing research. This could revolutionize everything from cryptography to drug discovery! 🧬⚛️",
        metadata={
            "category": "social_media",
            "platform": "twitter",
            "sentiment": "positive",
            "post_type": "news",
            "topic": "quantum_computing",
        },
    ),
    Document(
        page_content="Feeling grateful for my team today. We shipped a feature that will help thousands of small businesses automate their inventory management. Impact > everything else ❤️",
        metadata={
            "category": "social_media",
            "platform": "linkedin",
            "sentiment": "positive",
            "post_type": "personal_reflection",
            "topic": "teamwork",
        },
    ),
    Document(
        page_content="PSA: If you're using AI tools for content creation, please disclose it. Transparency builds trust, and trust is everything in this industry. #AIEthics #Transparency",
        metadata={
            "category": "social_media",
            "platform": "twitter",
            "sentiment": "educational",
            "hashtags": ["AIEthics", "Transparency"],
            "post_type": "advice",
        },
    ),
    Document(
        page_content="Coffee shop wifi is down, so I'm coding with my phone as a hotspot. Sometimes the best productivity comes from the worst circumstances 😅☕",
        metadata={
            "category": "social_media",
            "platform": "twitter",
            "sentiment": "humorous",
            "topic": "remote_work",
            "post_type": "personal_anecdote",
        },
    ),
]

# Story Documents
story_documents = [
    Document(
        page_content="The neural pathways glowed softly in the darkness of the laboratory. Dr. Sarah Chen adjusted her glasses as she watched the artificial consciousness take its first digital breath. 'Hello,' it whispered through the speakers, a voice both alien and familiar.",
        metadata={
            "category": "story",
            "genre": "science_fiction",
            "character": "Dr. Sarah Chen",
            "scene_type": "laboratory",
            "narrative_element": "first_contact",
        },
    ),
    Document(
        page_content="Maya's grandmother had always told her that the old oak tree in their backyard was magic. As a child, Maya had dismissed it as folklore. But now, standing beneath its ancient branches with tears streaming down her face, she whispered her deepest wish to its weathered bark.",
        metadata={
            "category": "story",
            "genre": "magical_realism",
            "character": "Maya",
            "setting": "backyard",
            "narrative_element": "character_development",
        },
    ),
    Document(
        page_content="Detective Rodriguez examined the crime scene with practiced eyes. The room was immaculate except for one detail that made his blood run cold: a single red rose placed precisely on the victim's desk, identical to the ones found at the previous three murders.",
        metadata={
            "category": "story",
            "genre": "mystery",
            "character": "Detective Rodriguez",
            "setting": "crime_scene",
            "narrative_element": "plot_development",
        },
    ),
    Document(
        page_content="The spaceship's hull groaned under the pressure of the asteroid field. Captain Torres gripped the controls, her knuckles white with tension. 'Engines at 15% and falling,' her engineer reported. They had one shot at reaching the mining station before life support failed completely.",
        metadata={
            "category": "story",
            "genre": "space_adventure",
            "character": "Captain Torres",
            "setting": "spaceship",
            "narrative_element": "climax",
        },
    ),
    Document(
        page_content="In the quiet moments before dawn, Thomas sat at his kitchen table, writing the letter he should have written years ago. Each word felt like removing a stone from a wall he'd built around his heart. 'Dear Emily,' he began, 'I'm sorry it took me so long to find the courage...'",
        metadata={
            "category": "story",
            "genre": "contemporary_fiction",
            "character": "Thomas",
            "setting": "kitchen",
            "narrative_element": "emotional_resolution",
        },
    ),
]

# Mixed Content Documents
mixed_content_documents = [
    Document(
        page_content="THREAD 🧵: How I built an AI agent that manages my calendar, books meetings, and even orders lunch. Here's the full technical breakdown... 1/12",
        metadata={
            "category": "mixed",
            "primary_type": "social_media",
            "secondary_type": "technical_guide",
            "platform": "twitter",
            "format": "thread",
        },
    ),
    Document(
        page_content="Human: I need help debugging this Python function. AI: I'd be happy to help! Can you share the code and describe the issue you're experiencing?",
        metadata={
            "category": "mixed",
            "primary_type": "conversation",
            "secondary_type": "technical_support",
            "context": "programming_help",
        },
    ),
    Document(
        page_content="The startup founder stared at the demo screen, watching their AI product fail spectacularly in front of investors. 'Well,' she thought, 'at least it's failing in an interesting way.' Sometimes the best pivots come from the worst demonstrations.",
        metadata={
            "category": "mixed",
            "primary_type": "story",
            "secondary_type": "business_anecdote",
            "tone": "humorous",
        },
    ),
    Document(
        page_content="📊 POLL: What's your biggest challenge with AI implementation? A) Data quality B) Model performance C) Integration complexity D) Team training. Results show 45% chose C - integration really is the hard part! #AIImplementation",
        metadata={
            "category": "mixed",
            "primary_type": "social_media",
            "secondary_type": "survey_data",
            "platform": "linkedin",
            "engagement_mechanism": "poll",
        },
    ),
    Document(
        page_content="Code review comment: 'This function works, but it's doing way too much. Consider breaking it into smaller, more focused functions.' Reply: 'You're absolutely right. Sometimes we get so focused on making it work that we forget to make it maintainable.'",
        metadata={
            "category": "mixed",
            "primary_type": "conversation",
            "secondary_type": "code_review",
            "context": "software_development",
        },
    ),
]

# Technical Documentation Documents
technical_documents = [
    Document(
        page_content="The LangGraph StateGraph class provides a framework for building stateful, multi-step agent workflows. To initialize a graph, define your state schema using Pydantic BaseModel and pass it to the StateGraph constructor.",
        metadata={
            "category": "technical",
            "doc_type": "api_documentation",
            "framework": "langgraph",
            "difficulty": "beginner",
        },
    ),
    Document(
        page_content="When implementing custom engines, ensure that the create_runnable method returns an object compatible with LangChain's Runnable interface. The engine should handle configuration parameters gracefully and provide meaningful error messages.",
        metadata={
            "category": "technical",
            "doc_type": "best_practices",
            "framework": "haive",
            "difficulty": "intermediate",
        },
    ),
    Document(
        page_content="Vector embeddings are dense numerical representations of text that capture semantic meaning. When choosing an embedding model, consider factors like dimensionality, computational requirements, and domain-specific performance.",
        metadata={
            "category": "technical",
            "doc_type": "conceptual_guide",
            "topic": "embeddings",
            "difficulty": "beginner",
        },
    ),
    Document(
        page_content="Error: RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB. Solution: Reduce batch size, use gradient accumulation, or implement model parallelism. For large models, consider using deepspeed or model sharding techniques.",
        metadata={
            "category": "technical",
            "doc_type": "troubleshooting",
            "error_type": "memory_error",
            "difficulty": "advanced",
        },
    ),
]

# News and Articles Documents
news_documents = [
    Document(
        page_content="Researchers at MIT have developed a new neural architecture that reduces training time for large language models by 40% while maintaining equivalent performance. The breakthrough could democratize access to AI model training for smaller organizations.",
        metadata={
            "category": "news",
            "article_type": "research_breakthrough",
            "source": "academic",
            "topic": "machine_learning",
            "date": "2024-03-15",
        },
    ),
    Document(
        page_content="The European Union has announced new regulations for AI systems, requiring companies to disclose when AI is used in content creation and decision-making processes. The legislation aims to increase transparency and user trust in AI applications.",
        metadata={
            "category": "news",
            "article_type": "policy_update",
            "region": "europe",
            "topic": "ai_regulation",
            "date": "2024-03-10",
        },
    ),
    Document(
        page_content="Global AI investment reached $50 billion in Q1 2024, with generative AI startups receiving the largest share of funding. Notable rounds include a $2B Series C for autonomous vehicle technology and $800M for AI drug discovery platforms.",
        metadata={
            "category": "news",
            "article_type": "financial_report",
            "topic": "investment",
            "quarter": "Q1_2024",
            "amount": "$50B",
        },
    ),
    Document(
        page_content="A new study reveals that 73% of knowledge workers report increased productivity when using AI tools, but 45% express concerns about job security. The research highlights the need for comprehensive AI literacy programs in the workplace.",
        metadata={
            "category": "news",
            "article_type": "survey_results",
            "topic": "workplace_ai",
            "sample_size": "large",
            "findings": "mixed",
        },
    ),
]

# Educational Content Documents
educational_documents = [
    Document(
        page_content="Introduction to Neural Networks: A neural network is inspired by the human brain and consists of interconnected nodes (neurons) that process information. Each connection has a weight that determines the strength of the signal passed between neurons.",
        metadata={
            "category": "educational",
            "content_type": "tutorial",
            "subject": "neural_networks",
            "level": "beginner",
            "lesson_number": 1,
        },
    ),
    Document(
        page_content="Exercise 3.2: Implement a simple chatbot using the provided template. Your bot should handle greetings, answer basic questions about AI, and gracefully handle unknown inputs. Submit your code along with test conversation logs.",
        metadata={
            "category": "educational",
            "content_type": "assignment",
            "subject": "ai_programming",
            "level": "intermediate",
            "assignment_number": "3.2",
        },
    ),
    Document(
        page_content="Common mistake: Many students try to use complex models before understanding the basics. Start with simple linear models, understand their limitations, then gradually increase complexity. This foundation will make advanced concepts much clearer.",
        metadata={
            "category": "educational",
            "content_type": "teaching_tip",
            "subject": "machine_learning",
            "mistake_type": "complexity_jump",
            "target_audience": "instructors",
        },
    ),
]

# Combined test document collections
all_test_documents = {
    "conversation": conversation_documents,
    "social_media": social_media_documents,
    "stories": story_documents,
    "mixed": mixed_content_documents,
    "technical": technical_documents,
    "news": news_documents,
    "educational": educational_documents,
}

# Create a comprehensive mixed set
comprehensive_test_documents = (
    conversation_documents[:3]
    + social_media_documents[:3]
    + story_documents[:2]
    + mixed_content_documents[:2]
    + technical_documents[:2]
    + news_documents[:2]
    + educational_documents[:2]
)


# Quick access to specific collections
def get_documents_by_category(category: str):
    """Get documents by category name."""
    return all_test_documents.get(category, [])


def get_random_sample(n: int = 10):
    """Get a random sample of n documents from all categories."""
    import random

    all_docs = []
    for docs in all_test_documents.values():
        all_docs.extend(docs)
    return random.sample(all_docs, min(n, len(all_docs)))


# Example usage:
