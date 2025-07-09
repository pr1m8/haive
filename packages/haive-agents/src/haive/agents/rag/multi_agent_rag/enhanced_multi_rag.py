"""Enhanced Multi-Agent RAG with Built-in Compatibility

This module demonstrates RAG systems using the compatibility-enhanced multi-agent base,
providing automatic compatibility checking and adaptation.
"""

from typing import Any

from haive.core.fixtures.documents import conversation_documents
from langchain_core.documents import Document

from haive.agents.multi.compatibility_enhanced_base import (
    CompatibilityEnhancedConditionalAgent,
    CompatibilityEnhancedMultiAgent,
    CompatibilityEnhancedParallelAgent,
    CompatibilityEnhancedSequentialAgent,
    CompatibilityMode,
    create_compatible_multi_agent,
)

from .agents import (
    SIMPLE_RAG_AGENT,
    SIMPLE_RAG_ANSWER_AGENT,
    DocumentGradingAgent,
    IterativeDocumentGradingAgent,
    SimpleRAGAgent,
    SimpleRAGAnswerAgent,
)
from .state import MultiAgentRAGState

# ============================================================================
# COMPATIBILITY-ENHANCED RAG SYSTEMS
# ============================================================================


class EnhancedRAGSequentialAgent(CompatibilityEnhancedSequentialAgent):
    """RAG sequential agent with built-in compatibility checking.

    This system automatically validates that retrieval -> grading -> generation
    agents are compatible and applies adapters if needed.
    """

    def __init__(
        self,
        retrieval_agent: SimpleRAGAgent | None = None,
        grading_agent: DocumentGradingAgent | None = None,
        answer_agent: SimpleRAGAnswerAgent | None = None,
        compatibility_mode: CompatibilityMode = CompatibilityMode.ADAPTIVE,
        **kwargs,
    ):
        # Set RAG-specific defaults
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = MultiAgentRAGState

        if "name" not in kwargs:
            kwargs["name"] = "Enhanced RAG Sequential System"

        # Initialize with empty agents list first
        super().__init__(agents=[], compatibility_mode=compatibility_mode, **kwargs)

        # Add agents with automatic compatibility checking
        if retrieval_agent:
            self.add_agent(retrieval_agent)
        else:
            self.add_agent(SIMPLE_RAG_AGENT)

        if grading_agent:
            self.add_agent(grading_agent)
        else:
            self.add_agent(DocumentGradingAgent(name="Auto-Added Grading Agent"))

        if answer_agent:
            self.add_agent(answer_agent)
        else:
            self.add_agent(SIMPLE_RAG_ANSWER_AGENT)

        print(f"✅ Created {self.name} with {len(self.agents)} compatible agents")


class EnhancedRAGConditionalAgent(CompatibilityEnhancedConditionalAgent):
    """RAG conditional agent with built-in compatibility checking and smart routing.

    This system checks compatibility at each routing decision and can adapt
    agents on-the-fly if compatibility issues are detected.
    """

    def __init__(
        self,
        retrieval_agent: SimpleRAGAgent | None = None,
        grading_agent: DocumentGradingAgent | None = None,
        answer_agent: SimpleRAGAnswerAgent | None = None,
        compatibility_mode: CompatibilityMode = CompatibilityMode.AUTO_FIX,
        **kwargs,
    ):
        # Set RAG-specific defaults
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = MultiAgentRAGState

        if "name" not in kwargs:
            kwargs["name"] = "Enhanced RAG Conditional System"

        # Initialize with empty agents list
        super().__init__(agents=[], compatibility_mode=compatibility_mode, **kwargs)

        # Store agent references for conditional routing
        self.retrieval_agent = retrieval_agent or SIMPLE_RAG_AGENT
        self.grading_agent = grading_agent or DocumentGradingAgent(
            name="Conditional Grading Agent"
        )
        self.answer_agent = answer_agent or SIMPLE_RAG_ANSWER_AGENT

        # Add agents with compatibility checking
        self.add_agent(self.retrieval_agent)
        self.add_agent(self.grading_agent)
        self.add_agent(self.answer_agent)

        # Set up conditional routing after all agents are added and validated
        self._setup_enhanced_conditional_routing()

        print(f"✅ Created {self.name} with compatibility-aware routing")

    def _setup_enhanced_conditional_routing(self):
        """Set up conditional routing with compatibility awareness."""

        def compatibility_aware_routing(state: MultiAgentRAGState) -> str:
            """Route based on both logic and compatibility."""
            # Standard RAG logic
            if not state.retrieved_documents:
                return self._get_agent_node_name(self.retrieval_agent)

            if not state.graded_documents:
                return self._get_agent_node_name(self.grading_agent)

            return self._get_agent_node_name(self.answer_agent)

        # Add conditional edges with compatibility checking
        self.add_conditional_edge(
            source_agent=self.retrieval_agent,
            condition=compatibility_aware_routing,
            destinations={
                self._get_agent_node_name(self.grading_agent): self.grading_agent,
                self._get_agent_node_name(self.answer_agent): self.answer_agent,
            },
            default=self.grading_agent,
        )


class EnhancedRAGParallelAgent(CompatibilityEnhancedParallelAgent):
    """RAG parallel agent with built-in compatibility checking for consensus building.

    This system runs multiple RAG workflows in parallel and ensures they can
    all work with the same state schema.
    """

    def __init__(
        self,
        rag_variants: list[EnhancedRAGSequentialAgent] | None = None,
        compatibility_mode: CompatibilityMode = CompatibilityMode.ADAPTIVE,
        **kwargs,
    ):
        # Set RAG-specific defaults
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = MultiAgentRAGState

        if "name" not in kwargs:
            kwargs["name"] = "Enhanced RAG Parallel System"

        # Create default RAG variants if none provided
        if not rag_variants:
            rag_variants = [
                EnhancedRAGSequentialAgent(
                    name="RAG Variant 1", compatibility_mode=compatibility_mode
                ),
                EnhancedRAGSequentialAgent(
                    name="RAG Variant 2", compatibility_mode=compatibility_mode
                ),
                EnhancedRAGSequentialAgent(
                    name="RAG Variant 3", compatibility_mode=compatibility_mode
                ),
            ]

        # Initialize with empty agents list
        super().__init__(agents=[], compatibility_mode=compatibility_mode, **kwargs)

        # Add each RAG variant with compatibility checking
        for variant in rag_variants:
            self.add_agent(variant)

        print(f"✅ Created {self.name} with {len(self.agents)} compatible RAG variants")


# ============================================================================
# SMART RAG FACTORY WITH COMPATIBILITY
# ============================================================================


class SmartRAGFactory:
    """Factory for creating RAG systems with automatic compatibility management.

    This factory analyzes the provided agents and creates the most appropriate
    multi-agent structure with optimal compatibility settings.
    """

    @staticmethod
    def create_optimal_rag_system(
        agents: list[Any],
        documents: list[Document] | None = None,
        preferred_mode: str | None = None,
        compatibility_mode: CompatibilityMode = CompatibilityMode.ADAPTIVE,
    ) -> CompatibilityEnhancedMultiAgent:
        """Create an optimal RAG system based on provided agents.

        Args:
            agents: List of agents to include
            documents: Optional documents for RAG agents
            preferred_mode: Preferred execution mode ("sequential", "conditional", "parallel")
            compatibility_mode: How to handle compatibility issues

        Returns:
            Optimally configured RAG system with compatibility checking
        """
        print(f"🔍 Analyzing {len(agents)} agents for optimal RAG system...")

        # Analyze agent types
        retrieval_agents = [a for a in agents if isinstance(a, SimpleRAGAgent)]
        grading_agents = [a for a in agents if isinstance(a, DocumentGradingAgent)]
        answer_agents = [a for a in agents if isinstance(a, SimpleRAGAnswerAgent)]

        print(
            f"   Found: {len(retrieval_agents)} retrieval, {len(grading_agents)} grading, {len(answer_agents)} answer agents"
        )

        # Determine optimal structure
        if preferred_mode == "parallel" or len(retrieval_agents) > 1:
            # Multiple retrieval agents suggest parallel processing
            system = EnhancedRAGParallelAgent(
                rag_variants=[
                    EnhancedRAGSequentialAgent(
                        retrieval_agent=ret_agent, compatibility_mode=compatibility_mode
                    )
                    for ret_agent in retrieval_agents[:3]  # Limit to 3 variants
                ],
                compatibility_mode=compatibility_mode,
                name="Smart Parallel RAG System",
            )

        elif preferred_mode == "conditional" or len(grading_agents) > 1:
            # Multiple grading options suggest conditional routing
            system = EnhancedRAGConditionalAgent(
                retrieval_agent=retrieval_agents[0] if retrieval_agents else None,
                grading_agent=grading_agents[0] if grading_agents else None,
                answer_agent=answer_agents[0] if answer_agents else None,
                compatibility_mode=compatibility_mode,
                name="Smart Conditional RAG System",
            )

        else:
            # Default to sequential
            system = EnhancedRAGSequentialAgent(
                retrieval_agent=retrieval_agents[0] if retrieval_agents else None,
                grading_agent=grading_agents[0] if grading_agents else None,
                answer_agent=answer_agents[0] if answer_agents else None,
                compatibility_mode=compatibility_mode,
                name="Smart Sequential RAG System",
            )

        # Add any remaining agents
        remaining_agents = [
            a
            for a in agents
            if not isinstance(
                a, (SimpleRAGAgent, DocumentGradingAgent, SimpleRAGAnswerAgent)
            )
        ]

        for agent in remaining_agents:
            try:
                system.add_agent(agent)
                print(f"   ✅ Added additional agent: {agent.name}")
            except Exception as e:
                print(f"   ⚠️  Could not add {agent.name}: {e!s}")

        # Generate compatibility report
        report = system.get_compatibility_report(detailed=True)
        print(f"✅ Created {system.name}")
        print(f"   Overall compatible: {report['overall_compatible']}")
        print(f"   Applied adapters: {report['applied_adapters']}")

        return system

    @staticmethod
    def create_safe_rag_system(
        documents: list[Document] | None = None,
        include_grading: bool = True,
        use_iterative_grading: bool = False,
        compatibility_mode: CompatibilityMode = CompatibilityMode.STRICT,
    ) -> EnhancedRAGSequentialAgent:
        """Create a safe RAG system with strict compatibility checking.

        This method creates a RAG system that is guaranteed to be compatible
        or will fail with clear error messages.
        """
        print("🛡️  Creating safe RAG system with strict compatibility...")

        try:
            # Create agents
            retrieval_agent = SimpleRAGAgent.from_documents(
                documents or conversation_documents, name="Safe Retrieval Agent"
            )

            if include_grading:
                if use_iterative_grading:
                    grading_agent = IterativeDocumentGradingAgent(
                        name="Safe Iterative Grading Agent"
                    )
                else:
                    grading_agent = DocumentGradingAgent(name="Safe Grading Agent")
            else:
                grading_agent = None

            answer_agent = SimpleRAGAnswerAgent(name="Safe Answer Agent")

            # Create system with strict compatibility
            system = EnhancedRAGSequentialAgent(
                retrieval_agent=retrieval_agent,
                grading_agent=grading_agent,
                answer_agent=answer_agent,
                compatibility_mode=compatibility_mode,
                name="Safe RAG System",
            )

            # Validate before returning
            report = system.get_compatibility_report()
            if not report["overall_compatible"]:
                raise ValueError(
                    f"Safe RAG system failed compatibility check: {report}"
                )

            print("✅ Safe RAG system created successfully")
            system.visualize_compatibility()

            return system

        except Exception as e:
            print(f"❌ Failed to create safe RAG system: {e!s}")
            raise


# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================


def demonstrate_enhanced_rag_compatibility():
    """Demonstrate the enhanced RAG system with built-in compatibility checking."""
    print("🚀 Demonstrating Enhanced RAG with Built-in Compatibility")
    print("=" * 60)

    # Example 1: Sequential RAG with automatic compatibility checking
    print("\n1. Creating Sequential RAG with Compatibility Checking")
    print("-" * 50)

    sequential_rag = EnhancedRAGSequentialAgent(
        compatibility_mode=CompatibilityMode.ADAPTIVE
    )

    sequential_rag.visualize_compatibility()

    # Example 2: Adding incompatible agent to demonstrate adaptation
    print("\n2. Testing Compatibility Adaptation")
    print("-" * 50)

    # Create a potentially incompatible agent
    custom_agent = SimpleRAGAgent(name="Custom Agent")

    try:
        sequential_rag.add_agent(custom_agent)
        print("✅ Agent added successfully (compatibility was handled automatically)")
    except Exception as e:
        print(f"❌ Agent incompatible: {e!s}")

    # Example 3: Smart factory creation
    print("\n3. Using Smart RAG Factory")
    print("-" * 50)

    test_agents = [
        SimpleRAGAgent(name="Agent 1"),
        DocumentGradingAgent(name="Grader 1"),
        SimpleRAGAnswerAgent(name="Answer 1"),
    ]

    SmartRAGFactory.create_optimal_rag_system(
        agents=test_agents, compatibility_mode=CompatibilityMode.AUTO_FIX
    )

    # Example 4: Safe RAG system
    print("\n4. Creating Safe RAG System")
    print("-" * 50)

    try:
        SmartRAGFactory.create_safe_rag_system(
            include_grading=True,
            use_iterative_grading=True,
            compatibility_mode=CompatibilityMode.STRICT,
        )

        print("✅ Safe RAG system created and validated")

    except Exception as e:
        print(f"❌ Safe RAG system creation failed: {e!s}")

    print("\n" + "=" * 60)
    print("🎉 Enhanced RAG Compatibility Demonstration Complete!")


# ============================================================================
# ENHANCED AGENT LIST (updated version with compatibility)
# ============================================================================

# Enhanced versions of the agents from the original prompt
enhanced_simple_rag_agent = SimpleRAGAgent.from_documents(
    conversation_documents, name="Enhanced Simple RAG Agent"
)

enhanced_simple_rag_answer_agent = SimpleRAGAnswerAgent(
    name="Enhanced Simple RAG Answer Agent"
)

# Enhanced base RAG agent with compatibility checking
enhanced_base_rag_agent = create_compatible_multi_agent(
    agents=[enhanced_simple_rag_agent, enhanced_simple_rag_answer_agent],
    execution_mode=CompatibilityMode.ADAPTIVE,
    name="Enhanced Base RAG Agent",
)

# Enhanced agent list for compatibility testing
enhanced_agent_list = [enhanced_simple_rag_agent, enhanced_simple_rag_answer_agent]


if __name__ == "__main__":
    demonstrate_enhanced_rag_compatibility()
