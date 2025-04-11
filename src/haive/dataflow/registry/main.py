# end_to_end_test.py
import uuid
from src.haive.dataflow.registry.core import registry_system
from src.haive.dataflow.registry.providers.agent_provider import agent_provider
from src.haive.dataflow.registry.models import EntityType

# Generate a session ID for tracking imports
session_id = str(uuid.uuid4())
print(f"Starting import session: {session_id}")

# Discover agents
agent_ids = agent_provider.discover()
print(f"Discovered {len(agent_ids)} agents")

# Get all agents
agents = registry_system.list_entities(EntityType.AGENT)
print(f"Retrieved {len(agents)} agents from registry")

# For each agent, print its dependencies and configurations
for agent in agents:
    print(f"\nAgent: {agent.name} (ID: {agent.id})")
    
    # Get dependencies
    deps = registry_system.get_dependencies(agent.id)
    print(f"  Dependencies: {len(deps)}")
    for dep in deps:
        dependent = registry_system.get_entity(dep.dependent_id)
        print(f"  - Depends on: {dependent.name} ({dependent.type}) via {dep.dependency_type}")
    
    # Get configurations
    configs = registry_system.get_configurations(agent.id)
    print(f"  Configurations: {len(configs)}")
    for config in configs:
        print(f"  - Config type: {config.config_type}")

# Check import logs
import_logs = registry_system._import_logs
print(f"\nImport logs for session {session_id}: {len(import_logs)}")
for log in import_logs:
    print(f"  - {log.entity_name}: {log.status}")