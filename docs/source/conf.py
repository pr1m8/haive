
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
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    
    # Third-party extensions
    'sphinx_autodoc_typehints',
    'sphinx_copybutton',
    'sphinx_tabs.tabs',
    'sphinx_design',
    'myst_parser',
    'sphinxcontrib.mermaid',
    'sphinx_togglebutton',
]

# Template path
templates_path = ['_templates']

# -- Autodoc configuration ---------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__, __dict__, __module__, __annotations__',
    'show-inheritance': True,
    'inherited-members': False,
    'ignore-module-all': True,  # Important for ignoring __all__
}

# More comprehensive mock imports
autodoc_mock_imports = [
    # ML/AI frameworks
    'torch', 'tensorflow', 'transformers', 'jax', 'flax',
    
    # Data science
    'numpy', 'pandas', 'scipy', 'sklearn', 'scikit-learn',
    
    # Visualization
    'matplotlib', 'seaborn', 'plotly', 'bokeh',
    
    # UI frameworks
    'streamlit', 'gradio', 'pygame', 'tkinter',
    
    # Game libraries
    'chess', 'python-chess',
    
    # Web/API
    'requests', 'httpx', 'aiohttp', 'fastapi', 'flask',
    
    # Database
    'sqlalchemy', 'pymongo', 'redis', 'psycopg2',
    
    # Testing/Development
    'pytest', 'hypothesis',
    
    # Other
    'opencv-cv2', 'cv2', 'PIL', 'Pillow',
]

# Type hints configuration
autodoc_typehints = 'description'
autodoc_typehints_format = 'short'
typehints_fully_qualified = False
always_document_param_types = True
typehints_document_rtype = True

# -- Autosummary configuration -----------------------------------------------
autosummary_generate = True
autosummary_imported_members = False
autosummary_ignore_module_all = True
autosummary_filename_map = {}

# IMPORTANT: Prevent autosummary from importing modules
autosummary_mock_imports = autodoc_mock_imports

# Don't generate for problematic modules
autosummary_generate_overwrite = False

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
    'langchain': ('https://python.langchain.com/', None),
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
    '**/generated/**',  # Exclude autogenerated files
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

# -- Custom autosummary handling ---------------------------------------------

class ErrorHandlingAutosummary:
    """Custom autosummary handling to catch import errors."""
    
    @staticmethod
    def get_documenter(app, obj, parent):
        """Get documenter with error handling."""
        try:
            from sphinx.ext.autodoc import get_documenter as orig_get_documenter
            return orig_get_documenter(app, obj, parent)
        except Exception as e:
            logging.warning(f"Failed to get documenter for {obj}: {e}")
            return None

# Monkey patch autosummary to handle errors better
try:
    from sphinx.ext import autosummary
    original_get_documenter = autosummary.get_documenter
    
    def safe_get_documenter(app, obj, parent):
        """Safely get documenter with error handling."""
        try:
            return original_get_documenter(app, obj, parent)
        except Exception as e:
            module_name = getattr(obj, '__module__', str(obj))
            logging.warning(f"Skipping {module_name}: {e}")
            SKIP_MODULES.add(module_name)
            return None
    
    autosummary.get_documenter = safe_get_documenter
except Exception:
    pass

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
    app.connect('autodoc-process-docstring', process_docstring)
    app.connect('autodoc-skip-member', skip_member)
    app.connect('autodoc-before-process-signature', before_process_signature)
    app.connect('source-read', source_read_handler)
    app.connect('build-finished', build_finished_handler)
    
    # Add custom configuration values
    app.add_config_value('haive_skip_modules', SKIP_MODULES, 'env')
    
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

def before_process_signature(app, what, name, obj, options, signature, return_annotation):
    """Handle signature processing errors."""
    try:
        # Check if we should skip this
        if not is_valid_module(name):
            return '(*args, **kwargs)', None
    except Exception as e:
        logging.error(f"Error processing signature for {name}: {e}")
        SKIP_MODULES.add(name)
        return '(*args, **kwargs)', None

def source_read_handler(app, docname, source):
    """Process source files before parsing."""
    # Skip problematic documents
    if any(skip in docname for skip in ['example', 'test', 'ui', 'demo', '_test']):
        source[0] = f"""
.. note::

   This is an example/test file. Please see the source code for implementation details.
   
   File: ``{docname}``
"""

def process_docstring(app, what, name, obj, options, lines):
    """Process docstrings with comprehensive error handling."""
    try:
        # Skip if module is invalid
        if not is_valid_module(name):
            if what == "module":
                lines[:] = [
                    f"Module excluded from documentation.",
                    "",
                    f"This module ({name}) has been excluded due to import errors or because it matches exclusion patterns.",
                    "",
                    "Common reasons for exclusion:",
                    "- Test files (test_*, *_test.py)",
                    "- Example files (example.py, examples/)",
                    "- UI files (ui.py, ui/)",
                    "- Demo files (demo.py, demos/)",
                ]
            else:
                lines[:] = [f"Member of excluded module {name}."]
            return
        
        # Track that we processed this successfully
        PROCESSED_MODULES.add(name)
        
    except Exception as e:
        logging.error(f"Error processing docstring for {name}: {e}")
        SKIP_MODULES.add(name)
        lines[:] = [f"Documentation unavailable due to processing error."]

def skip_member(app, what, name, obj, skip, options):
    """Determine whether member should be skipped."""
    try:
        # Skip private members (but not special methods)
        if name.startswith('_') and not name.startswith('__'):
            return True
        
        # Skip test/example/demo members
        skip_patterns = ['test', 'example', 'demo', 'ui', '_test']
        if any(pattern in name.lower() for pattern in skip_patterns):
            return True
        
        # Skip Pydantic internals
        pydantic_internals = [
            'model_config', 'model_fields', 'model_computed_fields',
            'model_extra', 'model_fields_set', 'model_post_init',
            '__pydantic_validator__', '__pydantic_fields__',
            '__pydantic_config__', '__pydantic_core_schema__',
            '__pydantic_decorators__', '__pydantic_generic_metadata__',
            '__pydantic_serializer__', '__pydantic_complete__',
        ]
        if name in pydantic_internals:
            return True
        
        # Skip if parent module is problematic
        if hasattr(obj, '__module__'):
            if obj.__module__ in SKIP_MODULES:
                return True
            if not is_valid_module(obj.__module__):
                return True
                
    except Exception as e:
        logging.error(f"Error checking skip for {name}: {e}")
        return True
    
    return skip

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