# src/haive/api/db.py
import logging
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database operations for the agent registry."""
    
    def __init__(self, connection_params: Dict[str, Any]):
        """
        Initialize the database manager.
        
        Args:
            connection_params: Database connection parameters
        """
        self.connection_params = connection_params
        self.connection = None
        self.schema_name = "ai"
    
    def connect(self) -> bool:
        """
        Connect to the database.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            logger.info("Connected to database")
            return True
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            return False
    
    def create_schema(self) -> bool:
        """
        Create the AI schema if it doesn't exist.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            with self.connection.cursor() as cursor:
                # Create schema if not exists
                cursor.execute(
                    sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                        sql.Identifier(self.schema_name)
                    )
                )
                self.connection.commit()
                logger.info(f"Schema '{self.schema_name}' created or already exists")
                return True
        except Exception as e:
            logger.error(f"Error creating schema: {e}")
            self.connection.rollback()
            return False
    
    def create_tables(self) -> bool:
        """
        Create the necessary tables in the AI schema.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            with self.connection.cursor() as cursor:
                # Create agent_types table
                cursor.execute(sql.SQL("""
                    CREATE TABLE IF NOT EXISTS {}.agent_types (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(50) UNIQUE NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """).format(sql.Identifier(self.schema_name)))
                
                # Create agent_configs table
                cursor.execute(sql.SQL("""
                    CREATE TABLE IF NOT EXISTS {}.agent_configs (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) UNIQUE NOT NULL,
                        class_name VARCHAR(100) NOT NULL,
                        module_path VARCHAR(255) NOT NULL,
                        agent_type_id INT REFERENCES {}.agent_types(id),
                        description TEXT,
                        config_schema JSONB,
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """).format(
                    sql.Identifier(self.schema_name),
                    sql.Identifier(self.schema_name)
                ))
                
                # Create agent_instances table (for tracking instantiated agents)
                cursor.execute(sql.SQL("""
                    CREATE TABLE IF NOT EXISTS {}.agent_instances (
                        id SERIAL PRIMARY KEY,
                        agent_config_id INT REFERENCES {}.agent_configs(id),
                        instance_id VARCHAR(100) NOT NULL,
                        config_params JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """).format(
                    sql.Identifier(self.schema_name),
                    sql.Identifier(self.schema_name)
                ))
                
                # Insert default agent types if they don't exist
                cursor.execute(sql.SQL("""
                    INSERT INTO {}.agent_types (name, description)
                    VALUES 
                        ('agent', 'Standard agent for general use'),
                        ('game', 'Game-specific agent')
                    ON CONFLICT (name) DO NOTHING
                """).format(sql.Identifier(self.schema_name)))
                
                self.connection.commit()
                logger.info(f"Tables created successfully in schema '{self.schema_name}'")
                return True
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            self.connection.rollback()
            return False
    
    def register_agent_config(self, name: str, class_obj: Any, agent_type: str = "agent") -> bool:
        """
        Register an agent configuration in the database.
        
        Args:
            name: Agent name
            class_obj: Agent configuration class
            agent_type: Type of agent (e.g., 'agent', 'game')
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            with self.connection.cursor() as cursor:
                # Get agent type ID
                cursor.execute(
                    sql.SQL("SELECT id FROM {}.agent_types WHERE name = %s").format(
                        sql.Identifier(self.schema_name)
                    ),
                    (agent_type,)
                )
                
                agent_type_id = cursor.fetchone()
                
                # If agent type doesn't exist, create it
                if not agent_type_id:
                    cursor.execute(
                        sql.SQL("INSERT INTO {}.agent_types (name) VALUES (%s) RETURNING id").format(
                            sql.Identifier(self.schema_name)
                        ),
                        (agent_type,)
                    )
                    agent_type_id = cursor.fetchone()
                
                # Get class info
                class_name = class_obj.__name__
                module_path = class_obj.__module__
                
                # Create a schema representation of the config class if possible
                config_schema = {}
                try:
                    from inspect import signature
                    sig = signature(class_obj.__init__)
                    for param_name, param in sig.parameters.items():
                        if param_name not in ['self', 'args', 'kwargs']:
                            config_schema[param_name] = {
                                'type': str(param.annotation),
                                'required': param.default == param.empty,
                                'default': None if param.default == param.empty else str(param.default)
                            }
                except Exception as e:
                    logger.warning(f"Could not extract schema for {name}: {e}")
                
                # Get description
                description = class_obj.__doc__ or ""
                
                # Insert or update agent config
                cursor.execute(
                    sql.SQL("""
                        INSERT INTO {}.agent_configs 
                            (name, class_name, module_path, agent_type_id, description, config_schema)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (name) DO UPDATE SET
                            class_name = EXCLUDED.class_name,
                            module_path = EXCLUDED.module_path,
                            agent_type_id = EXCLUDED.agent_type_id,
                            description = EXCLUDED.description,
                            config_schema = EXCLUDED.config_schema,
                            updated_at = CURRENT_TIMESTAMP
                    """).format(sql.Identifier(self.schema_name)),
                    (name, class_name, module_path, agent_type_id[0], description, 
                     psycopg2.extras.Json(config_schema))
                )
                
                self.connection.commit()
                logger.info(f"Agent configuration '{name}' registered in database")
                return True
        except Exception as e:
            logger.error(f"Error registering agent config in database: {e}")
            self.connection.rollback()
            return False
    
    def get_agent_configs(self, agent_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get agent configurations from the database.
        
        Args:
            agent_type: Optional agent type to filter by
            
        Returns:
            List of agent configuration dictionaries
        """
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cursor:
                if agent_type:
                    cursor.execute(
                        sql.SQL("""
                            SELECT ac.*, at.name as agent_type
                            FROM {}.agent_configs ac
                            JOIN {}.agent_types at ON ac.agent_type_id = at.id
                            WHERE at.name = %s
                            ORDER BY ac.name
                        """).format(
                            sql.Identifier(self.schema_name),
                            sql.Identifier(self.schema_name)
                        ),
                        (agent_type,)
                    )
                else:
                    cursor.execute(
                        sql.SQL("""
                            SELECT ac.*, at.name as agent_type
                            FROM {}.agent_configs ac
                            JOIN {}.agent_types at ON ac.agent_type_id = at.id
                            ORDER BY ac.name
                        """).format(
                            sql.Identifier(self.schema_name),
                            sql.Identifier(self.schema_name)
                        )
                    )
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting agent configs from database: {e}")
            return []
    
    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")