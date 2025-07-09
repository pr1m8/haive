#!/usr/bin/env python3
"""
Basic State Management Example for Base Conversation Agents

This example demonstrates the core state management capabilities of the base
conversation system, including automatic tracking, computed properties, and
reducer-based state updates.
"""

import asyncio
from typing import List

from haive.agents.conversation.base import (
    ConversationState,
    create_conversation_state,
    get_conversation_progress,
    validate_conversation_participants,
)
from haive.agents.simple import SimpleAgent


def demonstrate_basic_state_creation():
    """Demonstrate basic conversation state creation and properties."""
    print("=== Basic State Creation ===")
    
    # Create simple agents
    alice = SimpleAgent(name="Alice")
    bob = SimpleAgent(name="Bob") 
    charlie = SimpleAgent(name="Charlie")
    
    # Create conversation state
    state = create_conversation_state(
        participants=[alice, bob, charlie],
        topic="Future of Artificial Intelligence",
        max_rounds=5
    )
    
    print(f"Initial state:")
    print(f"  Speakers: {state.speakers}")
    print(f"  Topic: {state.topic}")
    print(f"  Max rounds: {state.max_rounds}")
    print(f"  Round number: {state.round_number}")
    print(f"  Turn count: {state.turn_count}")
    print(f"  Progress: {state.conversation_progress:.1%}")
    print()
    
    return state, [alice, bob, charlie]


def demonstrate_state_updates(state: ConversationState):
    """Demonstrate reducer-based state updates."""
    print("=== State Updates via Reducers ===")
    
    # Simulate first turn (Alice speaks)
    print("Alice takes first turn...")
    state = state.model_copy(update={
        "turn_count": 1,
        "speaker_history": ["Alice"],
        "current_speaker": "Alice"
    })
    
    print(f"After Alice's turn:")
    print(f"  Turn count: {state.turn_count}")
    print(f"  Speaker history: {state.speaker_history}")
    print(f"  Current speaker: {state.current_speaker}")
    print(f"  Round number: {state.round_number}")
    print(f"  Current round speakers: {state.current_round_speakers}")
    print(f"  Remaining speakers this round: {state.remaining_speakers_this_round}")
    print()
    
    # Simulate second turn (Bob speaks)
    print("Bob takes second turn...")
    state = state.model_copy(update={
        "turn_count": 1,  # This will be added to existing count (becomes 2)
        "speaker_history": ["Bob"],  # This will be appended to existing history
        "current_speaker": "Bob"
    })
    
    print(f"After Bob's turn:")
    print(f"  Turn count: {state.turn_count}")
    print(f"  Speaker history: {state.speaker_history}")
    print(f"  Current round speakers: {state.current_round_speakers}")
    print(f"  Remaining speakers this round: {state.remaining_speakers_this_round}")
    print()
    
    # Simulate third turn (Charlie speaks - completes round 1)
    print("Charlie takes third turn (completes round 1)...")
    state = state.model_copy(update={
        "turn_count": 1,
        "speaker_history": ["Charlie"],
        "current_speaker": "Charlie"
    })
    
    print(f"After Charlie's turn (end of round 1):")
    print(f"  Turn count: {state.turn_count}")
    print(f"  Round number: {state.round_number}")
    print(f"  Current round speakers: {state.current_round_speakers}")
    print(f"  Remaining speakers this round: {state.remaining_speakers_this_round}")
    print(f"  Progress: {state.conversation_progress:.1%}")
    print()
    
    return state


def demonstrate_computed_properties(state: ConversationState):
    """Demonstrate computed properties for conversation analysis."""
    print("=== Computed Properties ===")
    
    print(f"Conversation Analysis:")
    print(f"  Total turns: {state.turn_count}")
    print(f"  Current round: {state.round_number}")
    print(f"  Turns per round: {state.turns_per_round}")
    print(f"  Should end by rounds: {state.should_end_by_rounds}")
    print(f"  Overall progress: {state.conversation_progress:.2%}")
    print()
    
    # Simulate several more turns to show progress
    print("Simulating multiple rounds...")
    for round_num in range(2, 6):  # Rounds 2-5
        for speaker in state.speakers:
            state = state.model_copy(update={
                "turn_count": 1,
                "speaker_history": [speaker],
                "current_speaker": speaker
            })
            
        print(f"  End of round {round_num}: "
              f"{state.conversation_progress:.1%} complete, "
              f"should end: {state.should_end_by_rounds}")
    
    print()
    return state


def demonstrate_progress_tracking(state: ConversationState):
    """Demonstrate progress tracking utilities."""
    print("=== Progress Tracking Utilities ===")
    
    progress_info = get_conversation_progress(state)
    
    print("Progress Information:")
    for key, value in progress_info.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    print()


def demonstrate_participant_validation():
    """Demonstrate participant validation."""
    print("=== Participant Validation ===")
    
    # Valid participants
    alice = SimpleAgent(name="Alice")
    bob = SimpleAgent(name="Bob")
    charlie = SimpleAgent(name="Charlie")
    
    try:
        validate_conversation_participants([alice, bob, charlie])
        print("✓ Valid participants passed validation")
    except ValueError as e:
        print(f"✗ Validation failed: {e}")
    
    # Test with duplicate names
    duplicate_alice = SimpleAgent(name="Alice")  # Same name as alice
    
    try:
        validate_conversation_participants([alice, bob, duplicate_alice])
        print("✓ Duplicate names somehow passed (this shouldn't happen)")
    except ValueError as e:
        print(f"✓ Correctly caught duplicate names: {e}")
    
    # Test with insufficient participants
    try:
        validate_conversation_participants([alice])  # Only one participant
        print("✓ Single participant somehow passed (this shouldn't happen)")
    except ValueError as e:
        print(f"✓ Correctly caught insufficient participants: {e}")
    
    print()


def demonstrate_custom_state_fields():
    """Demonstrate extending ConversationState with custom fields."""
    print("=== Custom State Extension ===")
    
    from pydantic import Field
    from typing import Dict, Any
    import operator
    
    class ExtendedConversationState(ConversationState):
        """Extended conversation state with custom fields."""
        
        # Custom fields
        quality_scores: List[float] = Field(default_factory=list)
        engagement_metrics: Dict[str, float] = Field(default_factory=dict)
        
        # Custom reducers
        __reducer_fields__ = {
            **ConversationState.__reducer_fields__,
            "quality_scores": operator.add,  # Append quality scores
        }
        
        @property
        def average_quality(self) -> float:
            """Calculate average conversation quality."""
            if not self.quality_scores:
                return 0.0
            return sum(self.quality_scores) / len(self.quality_scores)
    
    # Create extended state
    alice = SimpleAgent(name="Alice")
    bob = SimpleAgent(name="Bob")
    
    extended_state = ExtendedConversationState(
        speakers=["Alice", "Bob"],
        topic="Quality conversation example",
        max_rounds=3
    )
    
    print("Extended state created with custom fields:")
    print(f"  Quality scores: {extended_state.quality_scores}")
    print(f"  Engagement metrics: {extended_state.engagement_metrics}")
    print(f"  Average quality: {extended_state.average_quality}")
    print()
    
    # Update with custom data
    extended_state = extended_state.model_copy(update={
        "quality_scores": [8.5, 7.2],  # Will be appended
        "engagement_metrics": {"participation": 0.85, "sentiment": 0.72}
    })
    
    print("After updates:")
    print(f"  Quality scores: {extended_state.quality_scores}")
    print(f"  Average quality: {extended_state.average_quality:.2f}")
    print(f"  Engagement metrics: {extended_state.engagement_metrics}")
    print()


async def main():
    """Run all state management demonstrations."""
    print("Base Conversation Agent - State Management Examples")
    print("=" * 60)
    print()
    
    # Basic state creation
    state, participants = demonstrate_basic_state_creation()
    
    # Demonstrate participant validation
    demonstrate_participant_validation()
    
    # State updates via reducers
    state = demonstrate_state_updates(state)
    
    # Computed properties
    state = demonstrate_computed_properties(state)
    
    # Progress tracking utilities
    demonstrate_progress_tracking(state)
    
    # Custom state extensions
    demonstrate_custom_state_fields()
    
    print("State management demonstration complete!")


if __name__ == "__main__":
    asyncio.run(main())