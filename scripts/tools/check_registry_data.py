#!/usr/bin/env python
"""
Script to check if registry data was successfully stored in Supabase.
"""

import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv('.env')

# Try to import the Supabase client
try:
    from supabase import create_client

    # Get Supabase credentials from environment
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        logger.error("Supabase URL or KEY not set in environment. Check your .env file.")
        exit(1)

    # Initialize Supabase client
    supabase = create_client(supabase_url, supabase_key)
    logger.info(f"Connected to Supabase at {supabase_url}")

    # Check for agent registry data
    logger.info("Checking agent_registry table...")
    try:
        response = supabase.table("agent_registry").select("*").execute()
        if response.data:
            logger.info(f"Found {len(response.data)} agents in registry")
            # Display first agent if available
            if len(response.data) > 0:
                logger.info(f"First agent: {response.data[0]['name']}")
        else:
            logger.info("No agents found in registry")
    except Exception as e:
        logger.error(f"Error querying agent_registry: {e}")

    # Check for component schema data
    logger.info("Checking component_schemas table...")
    try:
        response = supabase.table("component_schemas").select("*").execute()
        if response.data:
            logger.info(f"Found {len(response.data)} component schemas")
            # Display first schema if available
            if len(response.data) > 0:
                logger.info(f"First schema type: {response.data[0]['schema_type']}")
        else:
            logger.info("No component schemas found")
    except Exception as e:
        logger.error(f"Error querying component_schemas: {e}")

    # Check for agent graph data
    logger.info("Checking agent_graphs table...")
    try:
        response = supabase.table("agent_graphs").select("*").execute()
        if response.data:
            logger.info(f"Found {len(response.data)} agent graphs")
            # Display first graph if available
            if len(response.data) > 0:
                logger.info(f"First graph has {len(response.data[0]['nodes'])} nodes and {len(response.data[0]['edges'])} edges")
        else:
            logger.info("No agent graphs found")
    except Exception as e:
        logger.error(f"Error querying agent_graphs: {e}")

except ImportError:
    logger.error("Supabase client not installed. Run: pip install supabase")
    exit(1)
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    exit(1)

logger.info("Verification complete!")