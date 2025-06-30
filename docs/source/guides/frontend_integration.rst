Frontend Integration Guide
==========================

This guide covers integrating Haive agents with frontend applications, including WebSocket communication, message streaming, and persistence.

Overview
--------

Haive provides a comprehensive backend infrastructure for agent-based applications with:

- 30+ pre-built agent types
- Real-time WebSocket streaming
- Multiple streaming modes and formats
- Supabase persistence for conversations
- JWT-based authentication

Architecture
------------

WebSocket Endpoint
~~~~~~~~~~~~~~~~~~

- **URL Pattern**: ``/api/ws/chat/{agent_name}``
- **Full URL**: ``ws://your-host:8000/api/ws/chat/{agent_name}?token={jwt_token}&config={json_config}``
- **Location**: ``packages/haive-dataflow/src/haive/dataflow/api/routes/agent_routes.py``

Authentication
~~~~~~~~~~~~~~

Haive uses JWT tokens from Supabase for authentication:

- **Header**: ``Authorization: Bearer YOUR_JWT_TOKEN``
- **User ID**: Extracted from JWT ``sub`` field
- **User isolation**: Automatic via RLS policies

Message Protocol
----------------

Backend Message Types
~~~~~~~~~~~~~~~~~~~~~

The WebSocket connection uses these message types:

- ``message`` - User input
- ``response`` - Agent response
- ``status`` - Status updates
- ``error`` - Error messages
- ``state`` - Intermediate state
- ``state_complete`` - Final state

Agent Output Structure
~~~~~~~~~~~~~~~~~~~~~~

Haive agents produce structured output with:

- **Messages**: LangChain message format (HumanMessage, AIMessage, etc.)
- **Graph Structure**: Multi-node execution (agent_node → validation → parse_output)
- **Structured Data**: Pydantic models for typed outputs
- **Tool Calls**: Native LangChain tool calling format

Streaming Configuration
-----------------------

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: typescript

   interface AgentStreamConfig {
     agent_name: string;      // Name of the agent
     provider: "azure" | "openai" | "anthropic";
     model: string;          // Model name (e.g., "gpt-4o")
     stream: boolean;        // Enable/disable streaming
     persistent: boolean;    // Save to Supabase
     
     // Enhanced streaming options:
     stream_mode: "messages" | "values" | "updates" | "debug" | "custom";
     stream_format: "auto" | "json" | "text" | "structured";
     progressive_updates: boolean;  // Send partial results
     buffer_chunks: boolean;        // Buffer multiple chunks
     chunk_size: number;           // Buffer size (if buffering enabled)
   }

Stream Modes
~~~~~~~~~~~~

1. **Messages Mode** (``stream_mode: "messages"``)
   
   - Best for: Chat interfaces
   - Returns: Individual message content
   - Format options: ``text`` or ``json``

2. **Values Mode** (``stream_mode: "values"``)
   
   - Best for: State-based applications
   - Returns: Complete state values
   - Format options: ``structured`` or ``json``

3. **Updates Mode** (``stream_mode: "updates"``)
   
   - Best for: Real-time progress tracking
   - Returns: Only changes/updates
   - Format options: ``structured``

4. **Debug Mode** (``stream_mode: "debug"``)
   
   - Best for: Development and debugging
   - Returns: Detailed execution information

Available Agents
----------------

Core Agents
~~~~~~~~~~~

- ``SimpleAgent`` - Basic structured output
- ``ReactAgent`` - Reasoning and action
- ``ConversationAgent`` - Multi-turn chat
- ``PlanningAgent`` - Task planning
- ``ResearchAgent`` - Information gathering

Specialized Agents
~~~~~~~~~~~~~~~~~~

- ``CodeExecutorAgent`` - Code generation and execution
- ``DataAnalysisAgent`` - Data processing and analysis
- ``DocumentAgent`` - Document processing
- ``RAGAgent`` - Retrieval-augmented generation
- 20+ more specialized agents

Database Integration
--------------------

Supabase Schema
~~~~~~~~~~~~~~~

Conversations are persisted in Supabase with:

.. code-block:: sql

   -- Conversation threads
   agent_state.threads (
     id, user_id, agent_name, created_at, metadata
   )
   
   -- Agent state snapshots
   agent_state.checkpoints (
     id, thread_id, checkpoint_data, created_at
   )
   
   -- Message history
   agent_state.conversations (
     id, thread_id, messages, created_at
   )
   
   -- Agent configurations
   agent_state.agent_configs (
     id, agent_name, config_data, created_at
   )

Frontend Implementation
-----------------------

WebSocket Connection
~~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   // Basic connection
   const ws = new WebSocket(
     `ws://localhost:8000/api/ws/chat/SimpleAgent?token=${jwtToken}`
   );
   
   // With configuration
   const config = {
     agent_name: "SimpleAgent",
     provider: "openai",
     model: "gpt-4",
     stream: true,
     persistent: true,
     stream_mode: "messages",
     stream_format: "json"
   };
   
   const ws = new WebSocket(
     `ws://localhost:8000/api/ws/chat/SimpleAgent?token=${jwtToken}&config=${encodeURIComponent(JSON.stringify(config))}`
   );

Message Handling
~~~~~~~~~~~~~~~~

.. code-block:: javascript

   ws.onmessage = (event) => {
     const data = JSON.parse(event.data);
     
     switch (data.type) {
       case 'response':
         // Handle agent response
         console.log('Agent:', data.content);
         break;
         
       case 'status':
         // Handle status updates
         console.log('Status:', data.status);
         break;
         
       case 'error':
         // Handle errors
         console.error('Error:', data.error);
         break;
         
       case 'state':
         // Handle intermediate state
         console.log('State update:', data.state);
         break;
         
       case 'state_complete':
         // Handle final state
         console.log('Final state:', data.state);
         break;
     }
   };

Sending Messages
~~~~~~~~~~~~~~~~

.. code-block:: javascript

   // Send user message
   ws.send(JSON.stringify({
     type: 'message',
     content: 'Hello, agent!'
   }));

React/Next.js Example
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: jsx

   import { useEffect, useState } from 'react';
   
   function AgentChat({ agentName, jwtToken }) {
     const [messages, setMessages] = useState([]);
     const [ws, setWs] = useState(null);
     
     useEffect(() => {
       const config = {
         agent_name: agentName,
         provider: "openai",
         model: "gpt-4",
         stream: true,
         persistent: true,
         stream_mode: "messages",
         stream_format: "json"
       };
       
       const websocket = new WebSocket(
         `ws://localhost:8000/api/ws/chat/${agentName}?token=${jwtToken}&config=${encodeURIComponent(JSON.stringify(config))}`
       );
       
       websocket.onmessage = (event) => {
         const data = JSON.parse(event.data);
         if (data.type === 'response') {
           setMessages(prev => [...prev, {
             role: 'assistant',
             content: data.content
           }]);
         }
       };
       
       setWs(websocket);
       
       return () => websocket.close();
     }, [agentName, jwtToken]);
     
     const sendMessage = (content) => {
       if (ws && ws.readyState === WebSocket.OPEN) {
         ws.send(JSON.stringify({
           type: 'message',
           content
         }));
         setMessages(prev => [...prev, {
           role: 'user',
           content
         }]);
       }
     };
     
     return (
       <div>
         {/* Render messages and input */}
       </div>
     );
   }

Error Handling
--------------

Connection Errors
~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   ws.onerror = (error) => {
     console.error('WebSocket error:', error);
   };
   
   ws.onclose = (event) => {
     if (event.code !== 1000) {
       console.error('WebSocket closed unexpectedly:', event);
       // Implement reconnection logic
     }
   };

Authentication Errors
~~~~~~~~~~~~~~~~~~~~~

- **401 Unauthorized**: Invalid or expired JWT token
- **403 Forbidden**: User doesn't have access to agent
- **404 Not Found**: Agent doesn't exist

Best Practices
--------------

1. **Connection Management**
   
   - Implement reconnection logic for dropped connections
   - Clean up WebSocket connections on component unmount
   - Handle connection state in your UI

2. **Message Buffering**
   
   - Queue messages when connection is unavailable
   - Implement retry logic for failed messages
   - Show connection status to users

3. **Performance**
   
   - Use appropriate stream modes for your use case
   - Enable chunk buffering for better performance
   - Implement virtual scrolling for long conversations

4. **Security**
   
   - Always validate JWT tokens
   - Implement rate limiting on the frontend
   - Sanitize user input before sending

Testing
-------

Local Development
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Start the backend
   cd packages/haive-dataflow
   poetry run python -m haive.dataflow.api
   
   # Test WebSocket connection
   wscat -c "ws://localhost:8000/api/ws/chat/SimpleAgent?token=YOUR_TOKEN"

Integration Testing
~~~~~~~~~~~~~~~~~~~

.. code-block:: javascript

   // Test utilities
   import { WebSocket } from 'ws';
   
   describe('Agent WebSocket', () => {
     it('should connect and receive messages', async () => {
       const ws = new WebSocket(
         `ws://localhost:8000/api/ws/chat/SimpleAgent?token=${testToken}`
       );
       
       await new Promise(resolve => ws.on('open', resolve));
       
       ws.send(JSON.stringify({
         type: 'message',
         content: 'Test message'
       }));
       
       const response = await new Promise(resolve => {
         ws.on('message', data => resolve(JSON.parse(data)));
       });
       
       expect(response.type).toBe('response');
       expect(response.content).toBeTruthy();
     });
   });

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

1. **Connection Refused**
   
   - Check if backend is running
   - Verify correct host and port
   - Check firewall settings

2. **Authentication Failed**
   
   - Verify JWT token is valid
   - Check token expiration
   - Ensure user has proper permissions

3. **No Response from Agent**
   
   - Check agent name is correct
   - Verify agent is properly configured
   - Check backend logs for errors

4. **Message Format Errors**
   
   - Ensure messages are properly JSON-encoded
   - Check required fields are present
   - Validate message types

Additional Resources
--------------------

- Agent Documentation: :doc:`/agents/index`
- API Reference: :doc:`/api/index`
- Example Applications: ``/examples/frontend/``
- WebSocket Testing: ``/tests/integration/websocket/``