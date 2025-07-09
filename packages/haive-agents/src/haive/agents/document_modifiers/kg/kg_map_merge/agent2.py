from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.engine.aug_llm import compose_runnable
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j.graphs.graph_document import GraphDocument, Relationship
from langgraph.graph import END, START
from langgraph.types import Command, Send

from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer
from haive.agents.document_modifiers.kg.kg_map_merge.config import ParallelKGAgentConfig
from haive.agents.document_modifiers.kg.kg_map_merge.engines import (
    kg_extraction_engine,
    merge_analysis_engine,
    schema_extraction_engine,
)
from haive.agents.document_modifiers.kg.kg_map_merge.state import ParallelKGState


@register_agent(ParallelKGAgentConfig)
class StructuredKGAgent(Agent[ParallelKGAgentConfig]):
    """An agent that builds a knowledge graph using structured output models.

    This agent:
    1. Extracts schema (node types, relationship types) from content
    2. Processes documents in parallel to extract graph fragments
    3. Merges the graph fragments into a unified knowledge graph

    Uses structured Pydantic models for all extraction and merging steps.
    """

    def __init__(self, config: ParallelKGAgentConfig):
        """Initialize the knowledge graph agent with structured output processing."""
        super().__init__(config)

        # Initialize engines as runnables
        self.schema_extraction_chain = compose_runnable(
            config.engines.get("schema_extraction", schema_extraction_engine)
        )

        self.kg_extraction_chain = compose_runnable(
            config.engines.get("kg_extraction", kg_extraction_engine)
        )

        self.merge_analysis_chain = compose_runnable(
            config.engines.get("merge_analysis", merge_analysis_engine)
        )

        # Initialize the graph transformer as a fallback
        self.graph_transformer = GraphTransformer()

        # Also initialize LLMGraphTransformer if needed
        llm = config.llm_config.instantiate()
        self.llm_graph_transformer = LLMGraphTransformer(
            llm=llm,
            allowed_nodes=config.allowed_nodes,
            allowed_relationships=config.allowed_relationships,
            strict_mode=True,
            node_properties=config.node_properties,
            relationship_properties=config.relationship_properties,
        )

    def initialize_workflow(self, state: ParallelKGState):
        """Initial node that determines whether schema extraction is needed.
        Returns a Command directing to the appropriate next node.
        """
        # Check if schema is already defined
        if len(state.node_types) > 0 and len(state.relationship_types) > 0:
            return "distribute_documents"
        return "extract_schema"

    async def extract_schema(self, state: ParallelKGState):
        """Extracts node and relationship types from the content using structured output."""
        try:
            # Combine a sample of content for schema extraction
            content_sample = []
            for i, content_item in enumerate(state.contents):
                if isinstance(content_item, str):
                    content_sample.append(content_item)
                elif isinstance(content_item, Document):
                    content_sample.append(content_item.page_content)

                # Limit to first 5 items for efficiency
                if i >= 4:
                    break

            combined_content = "\n\n".join(content_sample)

            # Extract schema using LLM with structured output
            schema_result = await self.schema_extraction_chain.ainvoke(
                {"document_contents": combined_content}
            )

            # schema_result is directly a KGSchemaExtraction object
            # thanks to structured output parsing
            node_types = schema_result.node_types
            relationship_types = schema_result.relationship_types

            print(
                f"Extracted {len(node_types)} node types and {len(relationship_types)} relationship types"
            )
            print(f"Node types: {', '.join([nt.name for nt in node_types])}")
            print(
                f"Relationship types: {', '.join([rt.name for rt in relationship_types])}"
            )

            # Update state with extracted schema
            return Command(
                update={
                    "node_types": node_types,
                    "relationship_types": relationship_types,
                    # "node_types_str": node_types,
                    # "relationship_types_str": relationship_types
                },
                goto="distribute_documents",
            )

        except Exception as e:
            print(f"Error during schema extraction: {e}")
            # Fallback to empty schema
            return Command(
                update={"node_types": [], "relationship_types": []},
                goto="distribute_documents",
            )

    def distribute_documents(self, state: ParallelKGState):
        """Set up the state for parallel document processing."""
        print(f"Preparing to process {len(state.contents)} documents")

        # We don't need to update the state here, just proceed to map_documents
        return Command(goto=self.map_documents(state))

    def map_documents(self, state: ParallelKGState):
        """Map function that creates Send commands for each document to be processed.
        Returns a list of Send objects - one for each document.
        """
        # Create a Send object for each document - using DICTIONARY, not state object
        sends = []

        for i, content in enumerate(state.contents):
            sends.append(
                Send(
                    "process_document",
                    {
                        "content": content,
                        "node_types_str": state.node_types_str,
                        "relationship_types_str": state.relationship_types_str,
                        "index": i,  # Keep track of the document index
                    },
                )
            )

        print(f"Mapping {len(sends)} documents for parallel processing")
        if not sends:
            # If no documents to process, go to END
            return Command(goto=END)
        return sends

    async def process_document(self, state: dict):
        """Process a single document to extract a knowledge graph fragment.
        Uses structured output model to directly get KGExtraction object.
        """
        try:
            # Extract data from the state dict passed to this node
            content = state["content"]
            node_types_str = state["node_types_str"]
            relationship_types_str = state["relationship_types_str"]
            index = state["index"]

            # Convert to string if it's a Document
            if isinstance(content, Document):
                content_str = content.page_content
            else:
                content_str = content

            print(f"Processing document {index + 1}: {content_str[:50]}...")

            graph_doc = self.graph_transformer.transform_documents(
                documents=[content],
                allowed_nodes=node_types_str,
                allowed_relationships=relationship_types_str,
            )
            # Return results as a dictionary
            return {"graph_document": graph_doc, "index": index, "processed": True}

        except Exception as e:
            print(f"Error processing document {state.get('index', '?')}: {e}")
            return {"index": state.get("index"), "processed": True, "error": str(e)}

    def distribute_graph_document_pairs(self, state: ParallelKGState):
        """Collect results from the parallel document processing.
        Updates the main state with the processed graph documents.
        """
        # Check if we have a processed document result
        if "graph_document" in state:
            graph_documents = list(state.graph_documents)
            index = state.get("index", len(graph_documents))

            # Ensure list is long enough
            while len(graph_documents) <= index:
                graph_documents.append(None)

            # Store the graph document
            graph_documents[index] = state["graph_document"]

            # Check if all documents have been processed
            all_processed = all(
                g is not None for g in graph_documents[: len(state.contents)]
            ) and len(graph_documents) >= len(state.contents)

            update = {"graph_documents": graph_documents}

            if all_processed:
                update["processing_complete"] = True

                # Set up for merging if we have multiple graphs
                valid_graphs = [g for g in graph_documents if g is not None]

                if len(valid_graphs) > 1:
                    # Create pairs for merging
                    pairs = []
                    for i in range(0, len(valid_graphs), 2):
                        if i + 1 < len(valid_graphs):
                            pairs.append((i, i + 1))
                        else:
                            # For odd number, the last one goes alone
                            pairs.append((i, None))

                    update["pairs_to_merge"] = pairs
                    print(
                        f"All documents processed. Created {len(pairs)} pairs for merging."
                    )
                elif len(valid_graphs) == 1:
                    # If only one graph, set it as the final result
                    update["merged_graph"] = valid_graphs[0]
                    print("Only one graph was generated, no merging needed.")
                else:
                    print("No valid graphs were generated.")

            return Command(update=update)

        # If no graph_document but we have an error, just update the state
        if "error" in state:
            print(f"Document processing error: {state['error']}")
            return Command(update={"processing_errors": state["error"]})

        # No change
        # return Command()

    def route_after_collection(self, state: ParallelKGState):
        """Determine next steps after document collection.
        Returns the appropriate node name for routing.
        """
        if not state.processing_complete:
            # Keep collecting
            return "collect_documents"

        if state.merged_graph is not None:
            # We have a final result already
            return END

        # If we have multiple graphs to merge
        if len([g for g in state.graph_documents if g is not None]) > 1:
            return "map_merge_pairs"

        # No graphs or already have a merged result
        return END

    def map_merge_pairs(self, state: ParallelKGState):
        """Map function for merge pairs, creating Send commands for each pair.
        Returns a list of Send objects for parallel merging.
        """
        # Get valid graph documents
        valid_graphs = [g for g in state.graph_documents if g is not None]

        # Create Send commands for each pair to merge
        sends = []

        # Create pairs from state or generate new ones
        pairs = state.pairs_to_merge
        if not pairs:
            # Create pairs if not already in state
            pairs = []
            for i in range(0, len(valid_graphs), 2):
                if i + 1 < len(valid_graphs):
                    pairs.append((i, i + 1))
                else:
                    # For odd number, the last one goes alone
                    pairs.append((i, None))

            # Update state with the generated pairs
            update_cmd = Command(
                update={"pairs_to_merge": pairs},
                goto="map_merge_pairs",  # Continue to the same node after update
            )
            if not pairs:
                # If no pairs could be created
                if valid_graphs:
                    # If there's a single valid graph, set it as the merged result
                    update_cmd = Command(
                        update={
                            "merged_graph": valid_graphs[0],
                            "processing_complete": True,
                        },
                        goto="finalize_graph",
                    )
                else:
                    # No graphs to merge
                    update_cmd = Command(goto="finalize_graph")

                return update_cmd

        # Create Send objects for each pair
        for pair_index, (index1, index2) in enumerate(pairs):
            graph1 = valid_graphs[index1]

            if index2 is not None and index2 < len(valid_graphs):
                graph2 = valid_graphs[index2]
                sends.append(
                    Send(
                        "merge_pair",
                        {"graph1": graph1, "graph2": graph2, "pair_index": pair_index},
                    )
                )
            else:
                # If only one graph in the pair, pass it directly
                sends.append(
                    Send(
                        "collect_merged",
                        {"merged_graph": graph1, "pair_index": pair_index},
                    )
                )

        print(f"Created {len(sends)} merge pair tasks for round {state.merge_round}")

        if not sends:
            if valid_graphs:
                # If no pairs but we have graphs, use the first one
                return Command(
                    update={"merged_graph": valid_graphs[0]}, goto="finalize_graph"
                )
            # No valid graphs
            return Command(goto="finalize_graph")

        return sends

    async def merge_pair(self, state: dict):
        """Merge a pair of graph documents using structured output."""
        try:
            # Extract the graphs to merge
            graph1 = state["graph1"]
            graph2 = state["graph2"]
            pair_index = state["pair_index"]

            print(f"Merging pair {pair_index + 1}")

            # Format node and relationship information for the prompt
            existing_nodes = "\n".join(
                [
                    f"- {node.id} ({node.type}): {node.properties}"
                    for node in graph1.nodes
                ]
            )

            existing_relationships = "\n".join(
                [
                    f"- {rel.source.id} -{rel.type}-> {rel.target.id}: {rel.properties}"
                    for rel in graph1.relationships
                ]
            )

            new_nodes = "\n".join(
                [
                    f"- {node.id} ({node.type}): {node.properties}"
                    for node in graph2.nodes
                ]
            )

            new_relationships = "\n".join(
                [
                    f"- {rel.source.id} -{rel.type}-> {rel.target.id}: {rel.properties}"
                    for rel in graph2.relationships
                ]
            )

            # Use the merge analysis chain with structured output
            merge_result = await self.merge_analysis_chain.ainvoke(
                {
                    "existing_nodes": existing_nodes,
                    "existing_relationships": existing_relationships,
                    "new_nodes": new_nodes,
                    "new_relationships": new_relationships,
                }
            )

            # merge_result is directly a MergeAnalysis object

            # Create a node mapping dictionary
            node_mapping = {}
            for match in merge_result.node_matches:
                # Each match is a dict with new_id -> existing_id
                for new_id, existing_id in match.items():
                    node_mapping[new_id] = existing_id

            # Create a new merged graph starting with graph1
            merged_graph = GraphDocument(
                nodes=list(graph1.nodes),
                relationships=list(graph1.relationships),
                source=None,  # No specific source for merged graph
            )

            # Add new nodes from graph2 (excluding matched ones)
            for node in graph2.nodes:
                if node.id not in node_mapping:
                    merged_graph.nodes.append(node)

            # Add new relationships from graph2 (with node ID mapping)
            for rel in graph2.relationships:
                # Map source and target IDs if needed
                source_id = node_mapping.get(rel.source.id, rel.source.id)
                target_id = node_mapping.get(rel.target.id, rel.target.id)

                # Check if relationship already exists
                exists = any(
                    existing_rel.source.id == source_id
                    and existing_rel.target.id == target_id
                    and existing_rel.type == rel.type
                    for existing_rel in merged_graph.relationships
                )

                if not exists:
                    # Find the source and target nodes in the merged graph
                    source_node = next(
                        (n for n in merged_graph.nodes if n.id == source_id), None
                    )
                    target_node = next(
                        (n for n in merged_graph.nodes if n.id == target_id), None
                    )

                    if source_node and target_node:
                        # Create and add the relationship
                        new_rel = Relationship(
                            source=source_node,
                            target=target_node,
                            type=rel.type,
                            id=f"{source_id}-{rel.type}-{target_id}",
                            properties=rel.properties,
                        )
                        merged_graph.relationships.append(new_rel)

            return {"merged_graph": merged_graph, "pair_index": pair_index}

        except Exception as e:
            print(f"Error merging pair: {e}")
            # In case of error, return the first graph
            return {"merged_graph": state["graph1"], "pair_index": state["pair_index"]}

    def collect_merged(self, state: dict):
        """Collect a merged graph result.
        Updates the main state with the latest merge result.
        """
        # Extract the merged graph and pair index from the state dict
        if "merged_graph" not in state:
            return Command()

        merged_graph = state["merged_graph"]
        pair_index = state["pair_index"]

        # Update the main state with this merge result
        return Command(
            update={
                "latest_merge_result": merged_graph,
                "latest_merge_index": pair_index,
            }
        )

    def continue_merging(self, state: ParallelKGState):
        """Update merged results list with latest merge result.
        Decide whether to continue merging or finalize.
        """
        update = {}

        # Get existing merged results or initialize
        merged_results = list(state.merged_results)

        # Add the latest result if we have it
        if state.latest_merge_result is not None:
            pair_index = state.latest_merge_index

            # Make sure the list is long enough
            while len(merged_results) <= pair_index:
                merged_results.append(None)

            merged_results[pair_index] = state.latest_merge_result
            update["merged_results"] = merged_results

            # Clear the latest result
            update["latest_merge_result"] = None
            update["latest_merge_index"] = None

        # Check if all pairs have been merged
        pairs_to_merge = state.pairs_to_merge
        expected_results = len(pairs_to_merge) if pairs_to_merge else 0
        received_results = sum(1 for r in merged_results if r is not None)

        # If we have no pairs to merge, initialize them from graph_documents
        if not pairs_to_merge and state.graph_documents:
            valid_graphs = [g for g in state.graph_documents if g is not None]
            if len(valid_graphs) > 1:
                # Create pairs
                pairs = []
                for i in range(0, len(valid_graphs), 2):
                    if i + 1 < len(valid_graphs):
                        pairs.append((i, i + 1))
                    else:
                        # For odd number, the last one goes alone
                        pairs.append((i, None))

                update["pairs_to_merge"] = pairs
                print(
                    f"Created {len(pairs)} pairs for merging in round {state.merge_round}"
                )
                return Command(update=update, goto="map_merge_pairs")
            if len(valid_graphs) == 1:
                # Only one graph, no merging needed
                update["merged_graph"] = valid_graphs[0]
                return Command(update=update, goto="finalize_graph")
            # No graphs to merge
            return Command(goto="finalize_graph")

        if expected_results > 0 and received_results >= expected_results:
            # All expected results received
            # Filter out None values
            valid_results = [r for r in merged_results if r is not None]

            if len(valid_results) <= 1:
                # We're done merging
                if valid_results:
                    update["merged_graph"] = valid_results[0]
                    print(
                        f"Merging complete. Final graph has {len(valid_results[0].nodes)} nodes and {len(valid_results[0].relationships)} relationships"
                    )
                return Command(update=update, goto="finalize_graph")
            # More merging needed
            # Create new pairs
            pairs = []
            for i in range(0, len(valid_results), 2):
                if i + 1 < len(valid_results):
                    pairs.append((i, i + 1))
                else:
                    # For odd number, the last one goes alone
                    pairs.append((i, None))

            update["pairs_to_merge"] = pairs
            update["graph_documents"] = valid_results
            update["merged_results"] = []  # Reset for new round
            update["merge_round"] = state.merge_round + 1

            print(
                f"Starting merge round {state.merge_round + 1} with {len(pairs)} pairs"
            )
            return Command(update=update, goto="map_merge_pairs")

        # Not all pairs merged yet, continue collecting
        return Command(update=update, goto="collect_merged")

    def finalize_graph(self, state: ParallelKGState):
        """Finalize the merged graph and extract valuable statistics."""
        # Get the final merged graph
        final_graph = state.merged_graph

        if final_graph is None:
            # Try to get from merged_results or graph_documents
            if state.merged_results and any(state.merged_results):
                final_graph = next(
                    (g for g in state.merged_results if g is not None), None
                )
            elif state.graph_documents and any(state.graph_documents):
                final_graph = next(
                    (g for g in state.graph_documents if g is not None), None
                )

        if final_graph:
            # Extract schema statistics
            node_types = set()
            relationship_types = set()

            for node in final_graph.nodes:
                node_types.add(node.type)

            for rel in final_graph.relationships:
                relationship_types.add(rel.type)

            print(
                f"Final graph contains {len(final_graph.nodes)} nodes and {len(final_graph.relationships)} relationships"
            )
            print(f"Node types: {', '.join(sorted(node_types))}")
            print(f"Relationship types: {', '.join(sorted(relationship_types))}")

            return Command(
                update={
                    "merged_graph": final_graph,
                    "extracted_node_types": sorted(node_types),
                    "extracted_relationship_types": sorted(relationship_types),
                }
            )
        print("No graphs were generated")
        return Command(update={"merged_graph": None})

    def setup_workflow(self):
        """Set up the workflow for the structured knowledge graph agent."""
        # Add nodes to the graph
        self.graph.add_node("extract_schema", self.extract_schema)
        self.graph.add_node("distribute_documents", self.distribute_documents)
        # self.graph.add_node("map_documents", self.map_documents)
        self.graph.add_node("process_document", self.process_document)
        self.graph.add_node(
            "distribute_graph_document_pairs", self.distribute_graph_document_pairs
        )
        # self.graph.add_node("map_merge_pairs", self.map_merge_pairs)
        self.graph.add_node("merge_pair", self.merge_pair)
        self.graph.add_node("collect_merged", self.collect_merged)
        # self.graph.add_node("continue_merging", self.continue_merging)
        self.graph.add_node("finalize_graph", self.finalize_graph)

        # Set conditional entry point to match the diagram
        # self.graph.set_conditional_entry_point(
        #    self.initialize_workflow,
        #    {
        #          "extract_schema": "extract_schema",
        #        "distribute_documents": "distribute_documents"
        #    }
        # )

        # Core flow paths
        self.graph.add_edge("extract_schema", "distribute_documents")
        self.graph.add_conditional_edges(
            START,
            self.initialize_workflow,
            {
                "extract_schema": "extract_schema",
                "distribute_documents": "distribute_documents",
            },
        )
        # First map-reduce pattern for document processing
        # self.graph.add_edge("distribute_documents", "map_documents")
        # Note: map_documents returns Send objects to process_document
        # self.graph.add_edge("process_document", "collect_documents")
        self.graph.add_conditional_edges(
            "distribute_documents", self.map_documents, ["process_document"]
        )
        self.graph.add_conditional_edges(
            "distribute_graph_document_pairs", self.map_merge_pairs, ["merge_pair"]
        )
        # Document collection flow
        # self.graph.add_edge("collect_documents", "collect_documents")  # For collecting multiple documents
        # self.graph.add_conditional_edges("process_document",self.m,['collect_documents'])
        self.graph.add_conditional_edges(
            "process_document",
            lambda state: (
                "distribute_graph_document_pairs"
                if len(state.graph_documents) > 1
                else "finalize_graph"
            ),
            {
                "distribute_graph_document_pairs": "distribute_graph_document_pairs",
                "finalize_graph": "finalize_graph",
            },
        )

        # Second map-reduce pattern for merging graph fragments
        # Note: map_merge_pairs returns Send objects to merge_pair
        self.graph.add_edge("merge_pair", "collect_merged")
        # self.graph.add_edge("collect_merged", "continue_merging")

        # Merging flow management
        self.graph.add_conditional_edges(
            "collect_merged",
            lambda state: (
                "distribute_graph_document_pairs"
                if not state.merged_graph
                and len([g for g in state.merged_results if g]) > 1
                else "finalize_graph"
            ),
            {
                # "collect_merged": "collect_merged",    # More merges to collect
                "distribute_graph_document_pairs": "distribute_graph_document_pairs",  # Start another merge round
                "finalize_graph": "finalize_graph",  # Merging complete
            },
        )

        # Final paths
        self.graph.add_edge("finalize_graph", END)

        print("Workflow setup complete")
