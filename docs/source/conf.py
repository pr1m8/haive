
# docs/source/conf.py
import os
import sys
from pathlib import Path
import warnings
import logging
from datetime import datetime

# Suppress warnings
warnings.filterwarnings("ignore")

# -- Path setup --------------------------------------------------------------
# Get workspace root (docs/source/conf.py -> workspace root)
workspace_root = Path(__file__).resolve().parents[2]
docs_root = Path(__file__).resolve().parent.parent  # docs directory

# Create build directory if it doesn't exist
build_dir = docs_root / 'build'
build_dir.mkdir(exist_ok=True)

# Configure logging to capture import errors
log_file = build_dir / 'sphinx-import-errors.log'
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(str(log_file), mode='w'),
        logging.StreamHandler()
    ]
)

# Add package paths
packages = ['haive-core', 'haive-agents', 'haive-tools', 'haive-games', 'haive-dataflow', 'haive-prebuilt']
for package in packages:
    package_src = workspace_root / 'packages' / package / 'src'
    if package_src.exists():
        sys.path.insert(0, str(package_src))
        print(f"Added: {package_src}")

# Add main src
main_src = workspace_root / "src"
if main_src.exists():
    sys.path.insert(0, str(main_src))

# -- Project information -----------------------------------------------------
project = 'Haive'
copyright = f'2025-{datetime.now().year}, William R. Astley'
author = 'William R. Astley'
release = '1.0.0'
version = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    # Sphinx built-in
    'sphinx.ext.todo',
    'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    
    # Third-party extensions
    'sphinx_copybutton',
    'sphinx_tabs.tabs',
    'sphinx_design',
    'myst_parser',
    'sphinxcontrib.mermaid',
    'sphinx_togglebutton',
]

# Template path
templates_path = ['_templates']

# -- Autodoc configuration ------------------------------------------------------
extensions.extend([
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
])

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'special-members': '__init__',
    'member-order': 'bysource',
    'exclude-members': '__weakref__,__dict__,__module__',
}
autodoc_typehints = 'description'
autodoc_typehints_format = 'short'
autodoc_inherit_docstrings = True
autodoc_mock_imports = [
    # LangChain
    'langchain', 'langchain_core', 'langchain_community', 'langchain_openai',
    
    # Databases
    'neo4j', 'sqlalchemy', 'psycopg2', 'sqlite3', 'chromadb', 'faiss', 'pinecone',
    
    # Data science
    'networkx', 'numpy', 'pandas', 'matplotlib', 'scipy', 'torch', 'transformers',
    
    # LLM providers
    'openai', 'anthropic', 'deepseek', 'mistral', 'deepinfra', 'together',
    
    # Monitoring and logging
    'wandb', 'mlflow', 'ray', 'prometheus_client', 
    
    # Google services
    'google', 'google_auth_oauthlib', 'googleapiclient', 'google.cloud',
    
    # Web and parsing
    'beautifulsoup4', 'bs4', 'requests', 'httpx', 'aiohttp', 'PIL', 'pillow',
    
    # Development tools
    'jira', 'github', 'gitlab', 'boto3', 'botocore', 'slack_sdk', 
    
    # UI
    'textual', 'rich', 'tkinter', 'gradio', 'streamlit',
    
    # Core dependencies that might cause type issues
    'pydantic', 'pydantic_core', 'typing_extensions',
    
    # Framework and architecture
    'fastapi', 'flask', 'asyncio', 'grpc', 'uvicorn',
    
    # Specific Haive modules
    'haive.core.persistence', 'haive.agents.sequential',
    'haive.games.chess', 'haive.games.checkers', 'haive.games.poker', 'haive.games.hold_em',
    'haive.games.tic_tac_toe', 'haive.games.mancala', 'haive.games.dominoes'
]

# -- Autosummary configuration ---------------------------------------------------
autosummary_generate = True  # Generate API docs automatically
autosummary_imported_members = True  # Include imported members
autosummary_ignore_module_all = False  # Use __all__ to control what's documented

# -- MyST configuration ------------------------------------------------------
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "html_image",
    "colon_fence",
    "smartquotes",
    "replacements",
    "linkify",
    "strikethrough",
]

# Support both RST and Markdown
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Master document
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'

# Static files
html_static_path = ['_static']

# CSS and JS files
html_css_files = [
    'custom.css',
]

html_js_files = [
    'custom.js',
]

html_copy_source = True
html_show_sourcelink = True

html_title = "Haive Documentation"
html_short_title = "Haive"

# Theme options
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2962ff",
        "color-brand-content": "#2962ff",
        "color-api-background": "#F5F5F5",
        "color-api-background-hover": "#EEEEEE",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4fc3f7",
        "color-brand-content": "#4fc3f7",
        "color-api-background": "#1A1A1A",
        "color-api-background-hover": "#2A2A2A",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "announcement": "📚 This documentation is under active development",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/will-astley/haive",
            "html": "",
            "class": "fa fa-github",
        },
    ],
    "source_repository": "https://github.com/will-astley/haive/",
    "source_branch": "main",
    "source_directory": "docs/",
}

# -- Copy button configuration -----------------------------------------------
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_line_continuation_character = "\\"

# -- Mermaid configuration ---------------------------------------------------
mermaid_version = "10.6.1"

# -- Graphviz configuration --------------------------------------------------
graphviz_output_format = 'svg'

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pydantic': ('https://docs.pydantic.dev/latest/', None),
    'langchain_core': ('https://api.python.langchain.com/en/latest/langchain_core/', None),
    'langchain_community': ('https://api.python.langchain.com/en/latest/langchain_community/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
}

# -- Napoleon settings (Google docstrings) -----------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True

# -- Todo extension ----------------------------------------------------------
todo_include_todos = True

# -- Suppress all warnings more aggressively ---------------------------------
suppress_warnings = [
    'app.add_node',
    'app.add_directive', 
    'app.add_role',
    'autosummary',
    'autosummary.import_cycle',
    'autosummary.missing_attribute',
    'autosummary.not_autosummary',
    'autodoc',
    'autodoc.import_object',
    'autodoc.importer',
    'autodoc.missing_attribute',
    'ref.citation',
    'ref.footnote',
    'ref.numref',
    'ref.keyword',
    'ref.option',
    'ref.term',
    'ref.ref',
    'ref.doc',
    'misc.highlighting_failure',
    'toc.circular',
    'toc.no_title',
]

# -- Exclude patterns --------------------------------------------------------
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '**/.git',
    '**/node_modules',
    '**/__pycache__',
    '**/test_*.py',
    '**/tests/**',
    '**/testing/**',
    '**/*_test.py',
    '**/example.py',
    '**/examples/**',
    '**/ui.py',
    '**/ui/**',
    '**/demo.py',
    '**/demos/**',
    '**/*.ipynb',
    '**/*.egg-info/**',
    # '**/generated/**',  # Don't exclude autogenerated files, we need these for API docs
]

# -- Custom error handling ---------------------------------------------------

# Track problematic modules globally
SKIP_MODULES = set()
PROCESSED_MODULES = set()

def load_skip_list():
    """Load list of modules to skip from previous builds."""
    skip_file = build_dir / 'skip_modules.txt'
    if skip_file.exists():
        with open(skip_file, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_skip_list():
    """Save list of problematic modules."""
    skip_file = build_dir / 'skip_modules.txt'
    with open(skip_file, 'w') as f:
        for module in sorted(SKIP_MODULES):
            f.write(f"{module}\n")

# Load previous skip list
SKIP_MODULES = load_skip_list()

def is_valid_module(module_name):
    """Check if a module should be documented."""
    # Skip if in our skip list
    if module_name in SKIP_MODULES:
        return False
        
    # Skip known problematic patterns
    problematic_patterns = [
        'test', 'tests', 'testing', '_test',
        'example', 'examples', 'demo', 'demos',
        'ui', '_ui', 'gui',
        '__pycache__',
        'experimental', 'deprecated',
        '.ipynb_checkpoints',
        'tmp', 'temp',
    ]
    
    parts = module_name.split('.')
    
    # Check each part of the module path
    for part in parts:
        part_lower = part.lower()
        if any(pattern in part_lower for pattern in problematic_patterns):
            SKIP_MODULES.add(module_name)
            return False
    
    # Skip specific known problematic modules
    known_bad = [
        'haive.agents.rag.db_rag.sql_rag',
        'haive.games.framework',
        'haive.agents.simple.test2',
        'haive.games.tic_tac_toe',
        'haive.games.poker',
        'haive.games.chess',
        'haive.games.clue',
        'haive.games.battleship',
    ]
    
    for bad_module in known_bad:
        if module_name.startswith(bad_module):
            SKIP_MODULES.add(module_name)
            return False
    
    return True

# -- No custom autosummary handling

# -- Sphinx setup and event handlers -----------------------------------------

def setup(app):
    """Custom Sphinx application setup."""
    # Ensure directories exist
    static_dir = Path(app.srcdir) / '_static'
    static_dir.mkdir(exist_ok=True)
    
    templates_dir = Path(app.srcdir) / '_templates'
    templates_dir.mkdir(exist_ok=True)
    
    autosummary_dir = templates_dir / 'autosummary'
    autosummary_dir.mkdir(exist_ok=True)
    
    # Create generated directories for API docs
    api_dir = Path(app.srcdir) / 'api'
    if api_dir.exists():
        generated_dirs = [
            api_dir / 'core' / 'generated',
            api_dir / 'agents' / 'generated',
            api_dir / 'tools' / 'generated',
            api_dir / 'games' / 'generated'
        ]
        for gen_dir in generated_dirs:
            gen_dir.mkdir(parents=True, exist_ok=True)
            
    # No custom autosummary handler needed now
    
    # Create CSS file if it doesn't exist
    css_file = static_dir / 'custom.css'
    if not css_file.exists():
        css_content = """
/* Haive Documentation Custom CSS */
/* Your custom CSS here */
"""
        css_file.write_text(css_content)
    
    # Create JS file if it doesn't exist
    js_file = static_dir / 'custom.js'
    if not js_file.exists():
        js_content = """
// Haive Documentation Custom JavaScript
console.log('Haive documentation loaded!');
"""
        js_file.write_text(js_content)
    
    # Connect event handlers
    app.connect('source-read', source_read_handler)
    app.connect('build-finished', build_finished_handler)
    
    # Add custom configuration values
    app.add_config_value('haive_skip_modules', SKIP_MODULES, 'env')
    
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

# No signature processor

def source_read_handler(app, docname, source):
    """Process source files before parsing."""
    # Skip problematic documents
    if any(skip in docname for skip in ['example', 'test', 'ui', 'demo', '_test']):
        source[0] = f"""
.. note::

   This is an example/test file. Please see the source code for implementation details.
   
   File: ``{docname}``
"""

# No docstring processor

def build_finished_handler(app, exception):
    """Handle build completion."""
    # Save skip list
    save_skip_list()
    
    # Log summary
    logging.info(f"Build completed.")
    logging.info(f"Processed {len(PROCESSED_MODULES)} modules successfully")
    logging.info(f"Skipped {len(SKIP_MODULES)} problematic modules")
    
    if exception:
        logging.error(f"Build failed with exception: {exception}")
    
    # Write summary to file
    summary_file = build_dir / 'build_summary.txt'
    with open(summary_file, 'w') as f:
        f.write(f"Build Summary\n")
        f.write(f"=============\n\n")
        f.write(f"Processed modules: {len(PROCESSED_MODULES)}\n")
        f.write(f"Skipped modules: {len(SKIP_MODULES)}\n\n")
        
        if SKIP_MODULES:
            f.write("Skipped modules:\n")
            for module in sorted(SKIP_MODULES):
                f.write(f"  - {module}\n")

# Create autosummary template with error handling
autosummary_template = '''
{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. automodule:: {{ fullname }}
   
   {% block attributes %}
   {% if attributes %}
   .. rubric:: Module Attributes
   
   .. autosummary::
      :nosignatures:
   {% for item in attributes %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
   
   {% block functions %}
   {% if functions %}
   .. rubric:: Functions
   
   .. autosummary::
      :nosignatures:
   {% for item in functions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
   
   {% block classes %}
   {% if classes %}
   .. rubric:: Classes
   
   .. autosummary::
      :nosignatures:
   {% for item in classes %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
'''

# Write the template
autosummary_template_file = Path('docs/source/_templates/autosummary/module.rst')
autosummary_template_file.parent.mkdir(parents=True, exist_ok=True)
autosummary_template_file.write_text(autosummary_template)