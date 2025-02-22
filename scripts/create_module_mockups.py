

"""
This script creates mockup module files with docstrings to help build documentation
even when the actual modules are not fully importable.

Run this from the project root:
python docs/scripts/create_module_mockups.py
"""

import os
import sys
import shutil
from pathlib import Path

# Define the mockup directory
MOCKUP_DIR = "docs/mockups"

# Define the structure and docstrings for the modules
MODULES = {
    "haive": {
        "docstring": """
        Haive: A Python framework for building and deploying AI agents.
        
        Haive provides tools, abstractions, and infrastructure for developing
        sophisticated AI agents that can reason, plan, and interact with their environment.
        """,
        "submodules": {
            "agents": {
                "docstring": """
                Agent implementations and frameworks.
                
                This module contains various agent implementations, from simple reactive
                agents to complex reasoning frameworks.
                """,
                "submodules": {
                    "summarizer": {
                        "docstring": """
                        A module for text summarization agents.
                        
                        These agents can process and summarize large amounts of text data.
                        """,
                        "submodules": {
                            "agent.py": """
                            Implementation of the summarizer agent.
                            
                            The SummarizerAgent takes in text and produces concise summaries
                            while preserving the key information.
                            
                            Classes:
                                SummarizerAgent: Main agent implementation for text summarization.
                            """,
                            "aug_llms.py": """
                            Augmented language models for summarization.
                            
                            Provides specialized extensions to base language models to improve
                            summarization capabilities.
                            
                            Classes:
                                SummaryAugmentedLLM: LLM with summarization-specific augmentations.
                            """,
                            "prompts.py": """
                            Prompts for summarization tasks.
                            
                            Contains templates and strategies for prompting language models
                            to perform effective summarization.
                            
                            Functions:
                                get_summary_prompt: Returns a prompt template for summarization.
                            """
                        }
                    },
                    "web_nav": {
                        "docstring": """
                        A module for web navigation agents.
                        
                        These agents can browse and interact with web content to extract information.
                        """,
                        "submodules": {
                            "agent.py": """
                            Implementation of the web navigation agent.
                            
                            The WebNavAgent can navigate websites and extract information.
                            
                            Classes:
                                WebNavAgent: Main agent implementation for web navigation.
                            """,
                            "state.py": """
                            State management for web navigation.
                            
                            Tracks the current state of a web navigation session.
                            
                            Classes:
                                BrowserState: Represents the state of a browser session.
                            """,
                            "tools.py": """
                            Tools for web interaction.
                            
                            Provides functionality for clicking, scrolling, typing, and other web-based actions.
                            
                            Classes:
                                WebTool: Base class for web interaction tools.
                                ClickTool: Tool for clicking elements on a page.
                                ScrollTool: Tool for scrolling a page.
                            """
                        }
                    },
                    "self_discover": {
                        "docstring": """
                        A module for self-discovering agents.
                        
                        These agents can autonomously explore and learn about their environment.
                        """,
                        "submodules": {
                            "agent.py": """
                            Implementation of the self-discovering agent.
                            
                            The SelfDiscoverAgent can explore and learn from its environment.
                            
                            Classes:
                                SelfDiscoverAgent: Main agent implementation for autonomous exploration.
                            """,
                            "aug_llms.py": """
                            Augmented language models for self-discovery.
                            
                            Provides extensions to base language models to facilitate 
                            autonomous exploration and learning.
                            
                            Classes:
                                ExplorationAugmentedLLM: LLM with exploration-specific augmentations.
                            """,
                            "state.py": """
                            State management for self-discovering agents.
                            
                            Tracks the agent's knowledge and exploration state.
                            
                            Classes:
                                ExplorationState: Represents the state of exploration.
                            """
                        }
                    },
                    "tot": {
                        "docstring": """
                        Tree of Thought agent implementation.
                        
                        Implements the Tree of Thought reasoning framework where multiple reasoning paths
                        are explored in parallel.
                        """,
                        "submodules": {
                            "agent.py": """
                            Implementation of the Tree of Thought agent.
                            
                            The ToTAgent explores multiple reasoning paths to solve complex problems.
                            
                            Classes:
                                ToTAgent: Main agent implementation for Tree of Thought reasoning.
                            """,
                            "state.py": """
                            State management for Tree of Thought agents.
                            
                            Tracks the multiple branches of reasoning being explored.
                            
                            Classes:
                                ThoughtTreeState: Represents the state of a thought tree.
                                ThoughtNode: A node in the thought tree.
                            """
                        }
                    },
                    "react_agent": {
                        "docstring": """
                        Reasoning and Acting agent implementation.
                        
                        Implements the ReAct framework where agents alternate between reasoning and acting.
                        """,
                        "submodules": {
                            "base.py": """
                            Base implementation of the ReAct agent.
                            
                            The ReActAgent alternates between reasoning and acting to solve tasks.
                            
                            Classes:
                                ReActAgent: Main agent implementation for ReAct framework.
                            """
                        }
                    }
                }
            },
            "flstaesr": {
                "docstring": """
                Flexible State and Search Representation.
                
                This module provides tools for representing and manipulating states
                and search spaces in agent-based systems.
                """,
                "submodules": {
                    "transform": {
                        "docstring": """
                        Tools for transforming data representations.
                        
                        Provides utilities for converting between different data formats and structures.
                        """,
                        "submodules": {
                            "base.py": """
                            Base transformation functionality.
                            
                            Defines the base interfaces and implementations for data transformations.
                            
                            Classes:
                                BaseTransformer: Abstract base class for all transformers.
                            """,
                            "inspect_experiment.py": """
                            Tools for inspecting and experimenting with transformations.
                            
                            Provides utilities for visualizing and analyzing transformation results.
                            
                            Functions:
                                inspect_transformer: Analyze the behavior of a transformer.
                            """
                        }
                    },
                    "annotate": {
                        "docstring": """
                        Tools for annotating data.
                        
                        Provides utilities for adding metadata and annotations to data.
                        """,
                        "submodules": {
                            "base.py": """
                            Base annotation functionality.
                            
                            Defines the base interfaces and implementations for data annotation.
                            
                            Classes:
                                BaseAnnotator: Abstract base class for all annotators.
                            """
                        }
                    }
                }
            },
            "core": {
                "docstring": """
                Core functionality for the Haive framework.
                
                Provides foundational tools and utilities used throughout the framework.
                """,
                "submodules": {
                    "utils.py": """
                    Utility functions and classes.
                    
                    Provides common utilities used across the Haive framework.
                    
                    Functions:
                        format_response: Format agent responses for display.
                        load_config: Load configuration from a file.
                    """,
                    "config.py": """
                    Configuration management.
                    
                    Provides tools for managing and accessing configuration settings.
                    
                    Classes:
                        Config: Central configuration management class.
                    """
                }
            }
        }
    }
}


def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    os.makedirs(directory, exist_ok=True)


def create_module_file(path, docstring):
    """Create a Python module file with the given docstring."""
    with open(path, 'w') as f:
        f.write(f'"""{docstring}"""\n\n')
        
        # Add mock classes or functions based on docstring content
        if "Classes:" in docstring:
            # Extract class names
            class_lines = [line.strip() for line in docstring.split('\n') 
                          if ':' in line and 'Classes:' not in line]
            for line in class_lines:
                class_name = line.split(':')[0].strip()
                f.write(f'\nclass {class_name}:\n    """\n    A mock class for documentation.\n    """\n    pass\n')
        
        if "Functions:" in docstring:
            # Extract function names
            func_lines = [line.strip() for line in docstring.split('\n') 
                         if ':' in line and 'Functions:' not in line]
            for line in func_lines:
                func_name = line.split(':')[0].strip()
                f.write(f'\ndef {func_name}():\n    """\n    A mock function for documentation.\n    """\n    pass\n')


def create_init_file(path, docstring, imports=None):
    """Create an __init__.py file with the given docstring and imports."""
    with open(path, 'w') as f:
        f.write(f'"""{docstring}"""\n\n')
        
        if imports:
            for imp in imports:
                f.write(f'from . import {imp}\n')


def process_module(module_path, module_data, current_path=""):
    """Process a module and its submodules recursively."""
    if current_path:
        new_path = os.path.join(current_path, module_path)
    else:
        new_path = module_path
    
    # If this is a directory module
    if "submodules" in module_data:
        module_dir = os.path.join(MOCKUP_DIR, new_path)
        create_directory_if_not_exists(module_dir)
        
        # Create __init__.py
        init_path = os.path.join(module_dir, "__init__.py")
        imports = [k for k in module_data["submodules"].keys() 
                  if not k.endswith('.py')]  # Only import submodules, not files
        create_init_file(init_path, module_data["docstring"], imports)
        
        # Process submodules
        for submodule_name, submodule_data in module_data["submodules"].items():
            process_module(submodule_name, submodule_data, new_path)
    
    # If this is a Python file
    elif module_path.endswith('.py'):
        file_path = os.path.join(MOCKUP_DIR, new_path)
        create_module_file(file_path, module_data)


def main():
    """Main function to create all mockup modules."""
    # Clean up any existing mockup directory
    if os.path.exists(MOCKUP_DIR):
        shutil.rmtree(MOCKUP_DIR)
    
    # Create the mockup directory
    create_directory_if_not_exists(MOCKUP_DIR)
    
    # Process all modules
    for module_name, module_data in MODULES.items():
        process_module(module_name, module_data)
    
    print(f"Created mockup modules in {MOCKUP_DIR}")


if __name__ == "__main__":
    main()