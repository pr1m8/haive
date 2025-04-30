    def test_pattern_enhanced_workflow(self, pattern_agent_config, test_pattern):
        """Test enhanced workflow with patterns."""
        # Create a standalone graph
        from haive.core.graph.dynamic_graph_builder import DynamicGraph
        graph = DynamicGraph(name="test_graph")
        logger.info(f"Created DynamicGraph: {graph}")
        logger.info(f"Graph type: {type(graph).__name__}")
        logger.info(f"Graph has attributes: {', '.join(dir(graph)[:20])}")
        
        # Get pattern information
        pattern_name = test_pattern.metadata.name
        logger.info(f"Test pattern: {test_pattern}")
        logger.info(f"Pattern name: {pattern_name}")
        logger.info(f"Pattern type: {type(test_pattern).__name__}")
        
        # Add an engine to the graph
        if pattern_agent_config.engine:
            logger.info(f"Adding engine: {pattern_agent_config.engine.name}")
            graph.engines = {"default": pattern_agent_config.engine}
            graph.components = [pattern_agent_config.engine]
        else:
            logger.warning("No engine in pattern_agent_config")
        
        # Apply pattern directly to the graph
        logger.info(f"Applying pattern to graph: {pattern_name}")
        result = test_pattern.apply(graph, node_name="integration_node")
        logger.info(f"Pattern apply result: {result}")
        
        # Debug graph state after pattern application
        logger.info(f"Graph nodes: {list(graph.nodes.keys())}")
        logger.info(f"Graph edges: {graph.edges}")
        
        # Verify node was created
        assert "integration_node" in graph.nodes, "Pattern node not found in graph"
        
        # Verify START edge exists
        from langgraph.graph import START
        logger.info(f"Looking for START edge ({START} -> integration_node)")
        
        start_edge_exists = False
        for edge in graph.edges:
            logger.info(f"Edge: {edge}")
            if (hasattr(edge, "source") and edge.source == START and
                hasattr(edge, "target") and edge.target == "integration_node"):
                start_edge_exists = True
                logger.info("Found START edge!")
                break
        
        assert start_edge_exists, "START edge not found in graph.edges"
        
        # Try to compile the graph
        logger.info("Compiling graph after pattern application")
        compiled = graph.compile()
        logger.info(f"Compiled app: {compiled}")
        assert compiled is not None, "Graph failed to compile"
        
        logger.info(f"Test successful: pattern {pattern_name} enhanced workflow") 