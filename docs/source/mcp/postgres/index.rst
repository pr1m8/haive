.. title:: PostgreSQL MCP Server
.. _postgres-mcp:

🔀 PostgreSQL MCP Server
=========================

.. raw:: html

   <div class="agent-hero-section">
      <div class="hero-content">
         <h2>🔀 Database Operations via MCP</h2>
         <p class="hero-description">
            The PostgreSQL MCP server enables Claude Code to directly interact with your databases. 
            Query schemas, run SQL, analyze performance, and manage database operations seamlessly.
         </p>
      </div>
   </div>

Overview
--------

The PostgreSQL MCP (Model Context Protocol) server provides:

- **Direct SQL Execution**: Run queries and commands
- **Schema Exploration**: Browse tables, columns, and relationships
- **Performance Analysis**: Query optimization and analysis
- **Safe Operations**: Read-only mode and transaction support
- **Multi-Database**: Connect to multiple databases

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>✨ Key Features</h2>
      </div>
      <div class="api-grid">
         <div class="api-section">
            <h4>🔍 Query Operations</h4>
            <ul>
               <li>Execute SELECT queries</li>
               <li>Run INSERT/UPDATE/DELETE</li>
               <li>Transaction management</li>
               <li>Batch operations</li>
            </ul>
         </div>
         
         <div class="api-section">
            <h4>📃 Schema Management</h4>
            <ul>
               <li>List tables and views</li>
               <li>Describe columns</li>
               <li>View indexes</li>
               <li>Check constraints</li>
            </ul>
         </div>
         
         <div class="api-section">
            <h4>📊 Analysis Tools</h4>
            <ul>
               <li>Query EXPLAIN plans</li>
               <li>Performance metrics</li>
               <li>Table statistics</li>
               <li>Index usage</li>
            </ul>
         </div>
      </div>
   </div>

Installation
------------

.. raw:: html

   <div class="code-example-section">
      <h4>🚀 Quick Setup</h4>

.. code-block:: bash

   # Basic installation for local PostgreSQL
   claude mcp add postgres-local -s user -- \
     npx -y @modelcontextprotocol/server-postgres \
     "postgresql://localhost/mydatabase"

   # With authentication
   claude mcp add postgres-prod -s user -- \
     npx -y @modelcontextprotocol/server-postgres \
     "postgresql://username:password@host:5432/database"

   # With SSL (for production databases)
   claude mcp add postgres-ssl -s user -- \
     npx -y @modelcontextprotocol/server-postgres \
     "postgresql://user:pass@host:5432/db?sslmode=require"

   # Multiple databases
   claude mcp add postgres-multi -s user -- \
     npx -y @modelcontextprotocol/server-postgres \
     "postgresql://localhost/db1" \
     "postgresql://localhost/db2" \
     "postgresql://localhost/db3"

   # With environment variable
   claude mcp add postgres-env -s user -e DATABASE_URL=$DATABASE_URL -- \
     npx -y @modelcontextprotocol/server-postgres "${DATABASE_URL}"

.. raw:: html

   </div>

Configuration
-------------

.. raw:: html

   <div class="custom-section">
      <h3>⚙️ Advanced Configuration</h3>

.. code-block:: json

   {
     "mcpServers": {
       "postgres-haive": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-postgres",
           "postgresql://localhost/haive_dev"
         ],
         "env": {
           "PGPASSWORD": "your_password",
           "PGSSLMODE": "require",
           "PGCONNECT_TIMEOUT": "10"
         }
       },
       "postgres-readonly": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-postgres",
           "--readonly",
           "postgresql://readonly_user@localhost/production"
         ]
       }
     }
   }

.. raw:: html

   </div>

### Connection Options

.. code-block:: bash

   # Standard connection parameters
   postgresql://[user[:password]@][host][:port][/dbname][?param1=value1&...]

   # Common parameters:
   # - sslmode: disable, allow, prefer, require, verify-ca, verify-full
   # - connect_timeout: Connection timeout in seconds
   # - application_name: Set application name for pg_stat_activity
   # - options: Command-line options to send to the server

   # Examples:
   # Local with custom port
   postgresql://localhost:5433/mydb

   # Remote with SSL
   postgresql://user:pass@db.example.com/mydb?sslmode=require

   # With connection pooling
   postgresql://user:pass@pooler.example.com:6543/mydb?poolmode=transaction

   # Supabase connection
   postgresql://postgres.xxxxx:password@db.xxxxx.supabase.co:5432/postgres

Usage Examples
--------------

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>📝 Common Operations</h2>
      </div>

.. code-block:: sql

   -- In Claude Code, prefix with @postgres-local (or your server name)

   -- List all tables
   @postgres-local SELECT tablename FROM pg_tables WHERE schemaname = 'public';

   -- Describe a table
   @postgres-local \d agents

   -- Show table schema with details
   @postgres-local
   SELECT 
       column_name,
       data_type,
       character_maximum_length,
       is_nullable,
       column_default
   FROM information_schema.columns
   WHERE table_name = 'agents'
   ORDER BY ordinal_position;

   -- Query data
   @postgres-local
   SELECT 
       a.id,
       a.name,
       a.type,
       COUNT(c.id) as conversation_count,
       MAX(c.created_at) as last_active
   FROM agents a
   LEFT JOIN conversations c ON a.id = c.agent_id
   GROUP BY a.id, a.name, a.type
   ORDER BY last_active DESC
   LIMIT 10;

   -- Analyze query performance
   @postgres-local
   EXPLAIN ANALYZE
   SELECT * FROM large_table
   WHERE created_at > NOW() - INTERVAL '7 days'
   AND status = 'active';

   -- Check table statistics
   @postgres-local
   SELECT 
       schemaname,
       tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
       n_live_tup as row_count,
       n_dead_tup as dead_rows,
       last_vacuum,
       last_autovacuum
   FROM pg_stat_user_tables
   ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

.. raw:: html

   </div>

Database Management
-------------------

.. raw:: html

   <div class="custom-section">
      <h3>🔧 Administrative Tasks</h3>

.. code-block:: sql

   -- Check active connections
   @postgres-local
   SELECT 
       pid,
       usename,
       application_name,
       client_addr,
       state,
       query_start,
       state_change,
       LEFT(query, 100) as current_query
   FROM pg_stat_activity
   WHERE state != 'idle'
   ORDER BY query_start;

   -- Find slow queries
   @postgres-local
   SELECT 
       pid,
       now() - query_start as duration,
       query,
       state
   FROM pg_stat_activity
   WHERE (now() - query_start) > interval '5 minutes'
   AND state != 'idle';

   -- Kill a query
   @postgres-local SELECT pg_cancel_backend(12345);  -- Gentle cancel
   @postgres-local SELECT pg_terminate_backend(12345);  -- Force kill

   -- Database sizes
   @postgres-local
   SELECT 
       datname as database,
       pg_size_pretty(pg_database_size(datname)) as size
   FROM pg_database
   WHERE datistemplate = false
   ORDER BY pg_database_size(datname) DESC;

   -- Index usage
   @postgres-local
   SELECT 
       schemaname,
       tablename,
       indexname,
       idx_scan as index_scans,
       pg_size_pretty(pg_relation_size(indexrelid)) as index_size
   FROM pg_stat_user_indexes
   ORDER BY idx_scan DESC;

   -- Missing indexes suggestion
   @postgres-local
   SELECT 
       schemaname,
       tablename,
       attname as column_name,
       n_distinct,
       correlation
   FROM pg_stats
   WHERE schemaname = 'public'
   AND n_distinct > 100
   AND correlation < 0.1
   ORDER BY n_distinct DESC;

.. raw:: html

   </div>

Haive-Specific Queries
----------------------

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>🤖 Haive Database Queries</h2>
      </div>

.. code-block:: sql

   -- Agent performance metrics
   @postgres-local
   SELECT 
       a.name as agent_name,
       a.type as agent_type,
       COUNT(DISTINCT c.thread_id) as total_conversations,
       COUNT(m.id) as total_messages,
       AVG(m.token_count) as avg_tokens_per_message,
       AVG(m.response_time_ms) as avg_response_time_ms,
       MAX(c.updated_at) as last_active
   FROM agents a
   JOIN conversations c ON a.id = c.agent_id
   JOIN messages m ON c.id = m.conversation_id
   WHERE c.created_at > NOW() - INTERVAL '30 days'
   GROUP BY a.id, a.name, a.type
   ORDER BY total_conversations DESC;

   -- Tool usage analysis
   @postgres-local
   SELECT 
       t.name as tool_name,
       COUNT(*) as usage_count,
       AVG(tc.execution_time_ms) as avg_execution_time,
       COUNT(DISTINCT tc.agent_id) as unique_agents,
       SUM(CASE WHEN tc.success THEN 1 ELSE 0 END)::float / COUNT(*) as success_rate
   FROM tool_calls tc
   JOIN tools t ON tc.tool_id = t.id
   WHERE tc.created_at > NOW() - INTERVAL '7 days'
   GROUP BY t.id, t.name
   ORDER BY usage_count DESC;

   -- Conversation checkpoints
   @postgres-local
   SELECT 
       c.thread_id,
       c.agent_id,
       COUNT(cp.id) as checkpoint_count,
       pg_size_pretty(SUM(LENGTH(cp.state_data)::bigint)) as total_size,
       MAX(cp.created_at) as last_checkpoint
   FROM conversations c
   JOIN checkpoints cp ON c.id = cp.conversation_id
   GROUP BY c.thread_id, c.agent_id
   ORDER BY checkpoint_count DESC;

   -- Memory usage by agent
   @postgres-local
   SELECT 
       a.name,
       COUNT(DISTINCT m.conversation_id) as conversations_with_memory,
       pg_size_pretty(SUM(LENGTH(m.content)::bigint)) as total_memory_size,
       AVG(LENGTH(m.content)) as avg_memory_size
   FROM agents a
   JOIN conversations c ON a.id = c.agent_id
   JOIN memory_entries m ON c.id = m.conversation_id
   GROUP BY a.id, a.name
   ORDER BY total_memory_size DESC;

.. raw:: html

   </div>

Troubleshooting
---------------

.. raw:: html

   <div class="warning-section">
      <h3>⚠️ Common Issues</h3>

.. code-block:: bash

   # Connection refused
   # Check if PostgreSQL is running
   sudo systemctl status postgresql
   # or
   brew services list | grep postgresql

   # Authentication failed
   # Check pg_hba.conf for proper authentication method
   # Common fix for local development:
   # Change "peer" to "md5" or "trust" for local connections

   # SSL required
   # Add ?sslmode=require to connection string
   # For self-signed certs: ?sslmode=require&sslrootcert=server-ca.pem

   # Timeout errors
   # Increase timeout in connection string:
   # ?connect_timeout=30

   # Permission denied
   # Grant necessary permissions:
   @postgres-local GRANT SELECT ON ALL TABLES IN SCHEMA public TO your_user;

   # Too many connections
   # Check max_connections setting:
   @postgres-local SHOW max_connections;
   # Close idle connections:
   @postgres-local
   SELECT pg_terminate_backend(pid)
   FROM pg_stat_activity
   WHERE state = 'idle'
   AND state_change < NOW() - INTERVAL '10 minutes';

.. raw:: html

   </div>

Best Practices
--------------

.. raw:: html

   <div class="best-practices">
      <h3>💡 PostgreSQL MCP Best Practices</h3>
      <ul>
         <li><strong>Use Read-Only Connections</strong> for production databases</li>
         <li><strong>Limit Result Sets</strong> with LIMIT clause to avoid overwhelming Claude</li>
         <li><strong>Use Transactions</strong> for multiple related updates</li>
         <li><strong>Monitor Long Queries</strong> with pg_stat_activity</li>
         <li><strong>Create Indexes</strong> for frequently queried columns</li>
         <li><strong>Use EXPLAIN ANALYZE</strong> to optimize slow queries</li>
         <li><strong>Regular VACUUM</strong> for table maintenance</li>
         <li><strong>Connection Pooling</strong> for production use (pgBouncer)</li>
      </ul>
   </div>

Security Considerations
-----------------------

.. raw:: html

   <div class="custom-section">
      <h3>🔒 Security Guidelines</h3>

.. code-block:: bash

   # 1. Use environment variables for credentials
   export PGPASSWORD="your_secure_password"
   claude mcp add postgres -s user -e PGPASSWORD=$PGPASSWORD -- \
     npx -y @modelcontextprotocol/server-postgres \
     "postgresql://user@host/db"

   # 2. Create read-only user for MCP
   CREATE ROLE mcp_readonly WITH LOGIN PASSWORD 'secure_password';
   GRANT CONNECT ON DATABASE mydb TO mcp_readonly;
   GRANT USAGE ON SCHEMA public TO mcp_readonly;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_readonly;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO mcp_readonly;

   # 3. Use SSL for remote connections
   # Require SSL in pg_hba.conf:
   # hostssl all all 0.0.0.0/0 md5

   # 4. Restrict access by IP
   # In pg_hba.conf:
   # host mydb mcp_user 192.168.1.0/24 md5

   # 5. Audit MCP queries
   ALTER SYSTEM SET log_statement = 'all';
   ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log queries > 1s
   SELECT pg_reload_conf();

.. raw:: html

   </div>

Next Steps
----------

.. raw:: html

   <div class="showcase-section">
      <div class="showcase-header">
         <h2>🚀 Explore More MCP Servers</h2>
      </div>
      <div class="agent-showcase">
         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">📁</div>
               <div>
                  <h3 class="agent-title">Filesystem Server</h3>
                  <p class="agent-subtitle">Advanced file operations</p>
               </div>
            </div>
            <p class="agent-description">
               Browse, read, and manage files with the filesystem MCP server.
            </p>
            <a href="../filesystem/index.html" class="agent-link">Learn More</a>
         </div>

         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">🐙</div>
               <div>
                  <h3 class="agent-title">GitHub Server</h3>
                  <p class="agent-subtitle">Repository management</p>
               </div>
            </div>
            <p class="agent-description">
               Manage issues, PRs, and repository operations through MCP.
            </p>
            <a href="../github/index.html" class="agent-link">Learn More</a>
         </div>

         <div class="agent-card">
            <div class="agent-header">
               <div class="agent-emoji">🔍</div>
               <div>
                  <h3 class="agent-title">Search Server</h3>
                  <p class="agent-subtitle">Web search integration</p>
               </div>
            </div>
            <p class="agent-description">
               Search the web with Brave Search API through MCP.
            </p>
            <a href="../search/index.html" class="agent-link">Learn More</a>
         </div>
      </div>
   </div>

.. seealso::

   - :doc:`../index` - MCP overview and setup
   - :doc:`../../guides/mcp_integration` - Integration guide
   - `PostgreSQL Documentation <https://www.postgresql.org/docs/>`_