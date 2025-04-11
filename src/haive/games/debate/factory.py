# src/haive/games/debate/factory.py
from typing import List, Dict, Any, Optional
from src.haive.games.debate.agent import DebateAgent
from src.haive.games.debate.config import DebateAgentConfig
from src.haive.games.debate.models import Topic, Participant

class DebateFactory:
    """Factory for creating specialized debate formats."""
    
    @staticmethod
    def create_presidential_debate(candidates: List[Dict[str, Any]], moderator_name: str, topic: str) -> DebateAgent:
        """Create a presidential debate format.
        
        Args:
            candidates: List of candidate details
            moderator_name: Name of debate moderator
            topic: Debate topic
            
        Returns:
            DebateAgent: Configured presidential debate agent
        """
        # Create config
        config = DebateAgentConfig.presidential()
        
        # Setup initial state
        participant_list = [moderator_name] + [c.get("name") for c in candidates]
        
        # Create agent
        agent = DebateAgent(config)
        
        # Initialize with custom data
        topic_obj = {
            "title": topic,
            "description": f"Presidential debate on {topic}",
            "keywords": topic.split()
        }
        
        # Setup personas
        personas = {}
        for candidate in candidates:
            name = candidate.get("name")
            personas[name] = {
                "id": name,
                "name": name,
                "role": "debater",
                "position": candidate.get("position", "neutral"),
                "persona": candidate.get("persona", {}),
                "expertise": candidate.get("expertise", [])
            }
        
        # Add moderator
        personas[moderator_name] = {
            "id": moderator_name,
            "name": moderator_name,
            "role": "moderator"
        }
        
        init_data = {
            "topic": topic_obj,
            "participants": personas
        }
        
        return agent
    
    @staticmethod
    def create_legal_trial(case_details: Dict[str, Any], participants: Dict[str, str]) -> DebateAgent:
        """Create a legal trial format.
        
        Args:
            case_details: Details of the legal case
            participants: Dict mapping participant IDs to roles
            
        Returns:
            DebateAgent: Configured trial debate agent
        """
        # Create config
        config = DebateAgentConfig.trial()
        
        # Create agent
        agent = DebateAgent(config)
        
        # Create topic from case details
        topic_obj = {
            "title": case_details.get("title", "Legal Case"),
            "description": case_details.get("description", ""),
            "keywords": case_details.get("keywords", [])
        }
        
        # Setup initial state with roles
        init_data = {
            "topic": topic_obj,
            "participants": participants
        }
        
        return agent
    
    @staticmethod
    def create_panel_discussion(panel_topic: str, host_name: str, panelists: List[Dict[str, Any]]) -> DebateAgent:
        """Create a panel discussion format.
        
        Args:
            panel_topic: Topic of discussion
            host_name: Name of panel host/moderator
            panelists: List of panelist details
            
        Returns:
            DebateAgent: Configured panel discussion agent
        """
        # Create config
        config = DebateAgentConfig.panel_discussion()
        
        # Create agent
        agent = DebateAgent(config)
        
        # Create topic
        topic_obj = {
            "title": panel_topic,
            "description": f"Panel discussion on {panel_topic}",
            "keywords": panel_topic.split()
        }
        
        # Setup participants
        participants = {}
        
        # Add host
        participants[host_name] = {
            "id": host_name,
            "name": host_name,
            "role": "moderator"
        }
        
        # Add panelists
        for panelist in panelists:
            name = panelist.get("name")
            participants[name] = {
                "id": name,
                "name": name,
                "role": "debater",
                "position": panelist.get("position", "neutral"),
                "expertise": panelist.get("expertise", []),
                "persona": panelist.get("persona", {})
            }
        
        # Setup initial state
        init_data = {
            "topic": topic_obj,
            "participants": participants
        }
        
        return agent
    
    @staticmethod
    def create_prisoner_dilemma(prisoners: List[Dict[str, Any]], scenario: str) -> DebateAgent:
        """Create a prisoner's dilemma simulation.
        
        Args:
            prisoners: List of prisoner details
            scenario: Description of the dilemma scenario
            
        Returns:
            DebateAgent: Configured prisoner's dilemma agent
        """
        # Create custom config
        config = DebateAgentConfig(
            name="prisoner_dilemma",
            debate_format="dilemma",
            time_limit=300,
            max_statements=5,
            allow_interruptions=False,
            voting_enabled=True
        )
        
        # Create agent
        agent = DebateAgent(config)
        
        # Create topic
        topic_obj = {
            "title": "Prisoner's Dilemma",
            "description": scenario,
            "keywords": ["dilemma", "cooperation", "defection"]
        }
        
        # Setup participants
        participants = {}
        for prisoner in prisoners:
            name = prisoner.get("name")
            participants[name] = {
                "id": name,
                "name": name,
                "role": "prisoner",
                "persona": prisoner.get("persona", {})
            }
        
        # Add interrogator
        participants["Interrogator"] = {
            "id": "Interrogator",
            "name": "Interrogator",
            "role": "moderator"
        }
        
        # Setup initial state
        init_data = {
            "topic": topic_obj,
            "participants": participants
        }
        
        return agent