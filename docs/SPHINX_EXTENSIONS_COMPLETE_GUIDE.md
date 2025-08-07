# Complete Sphinx Extensions Usage Guide - Haive Framework

**Version**: 2.1
**Purpose**: Comprehensive guide for all 86+ Sphinx extensions configured in Haive
**Last Updated**: 2025-01-08

## 🚀 **Quick Start - Most Used Extensions**

### **Top 10 Extensions for Professional Documentation**

1. **`sphinx_design`** - Modern UI components (cards, grids, tabs)
2. **`sphinx_exec_code`** - Live code execution in docs
3. **`sphinx_jsonschema`** - Interactive Pydantic schemas
4. **`sphinxcontrib.mermaid`** - Architecture diagrams
5. **`sphinx_tabs`** - Multi-variant content
6. **`sphinx_copybutton`** - Copy code buttons
7. **`sphinx_tippy`** - Interactive tooltips
8. **`sphinx_needs`** - Requirements tracking
9. **`sphinxemoji`** - Rich emoji support
10. **`sphinx_last_updated_by_git`** - Version tracking

## 📋 **Extension Categories & Usage**

### 🎯 **ACTIVELY UTILIZED (22+ Extensions)**

#### **🔥 Live Execution Extensions**
1. **`sphinx_exec_code`** - Live Python code execution in docs
   ```rst
   .. exec_code::
      :caption: Live Python execution
      :linenos:
      
      # This code runs during doc build!
      from haive.core.engine.aug_llm import AugLLMConfig
      config = AugLLMConfig(temperature=0.7)
      print(f"✅ Config created: {type(config).__name__}")
   ```

2. **`sphinx_autorun`** - Code execution with output capture
   ```rst
   .. autorun:: python3
   
      import datetime
      print(f"🕰️ Build time: {datetime.datetime.now()}")
      print("📊 System metrics available!")
   ```

3. **`sphinx_runpython`** - Python script execution
   ```rst
   .. runpython::
      
      # Inline Python execution
      for i in range(3):
          print(f"🚀 Step {i+1}")
   ```

#### **📊 Interactive & Schema Extensions**
4. **`sphinx_jsonschema`** - Interactive JSON schema rendering
   ```rst
   .. jsonschema:: MyPydanticModel
      :lift_description: true
      :lift_definitions: true
      :auto_reference: true
      
      # Creates interactive, explorable schemas!
   ```

5. **`sphinxcontrib.autodoc_pydantic`** - Enhanced Pydantic model docs
   ```rst
   .. autopydantic_model:: MyModel
      :model-show-config-summary: True
      :model-show-field-summary: True
      :model-show-validator-members: True
      :field-list-validators: True
      :field-show-constraints: True
   ```

6. **`sphinx_tippy`** - Interactive tooltips
   ```rst
   Use :tippy:`tooltips <Hover text appears here>` for interactive help
   ```

7. **`sphinx_paramlinks`** - Parameter cross-references
   ```rst
   Check the :paramlink:`temperature parameter <Links to parameter docs>`
   ```

#### **🎨 Visual & Design Extensions**
8. **`sphinx_design`** - Modern cards, grids, tabs
   ```rst
   .. card:: 🤖 Agent Configuration
      :class-card: sd-rounded-3 sd-shadow-lg
      
      Professional card layout
      
      .. grid:: 1 2 2 2
         :gutter: 3
         
         .. grid-item-card:: Feature 1
         .. grid-item-card:: Feature 2
   ```

9. **`sphinx_tabs`** - Multi-variant content
   ```rst
   .. tab-set::
   
      .. tab-item:: Usage
         :sync: usage
         
         Usage documentation here
         
      .. tab-item:: Examples  
         :sync: examples
         
         Code examples here
   ```

10. **`sphinx_togglebutton`** - Collapsible sections
    ```rst
    .. dropdown:: 🔍 Advanced Configuration
       :color: info
       :icon: settings
       
       Hidden content here
    ```

#### **🔗 GitHub & Version Integration**
11. **`sphinx_issues`** + **`extlinks`** - GitHub integration
    ```rst
    See :issue:`123` for feature requests
    Check :pr:`456` for recent improvements  
    View :commit:`abc123` for latest changes
    ```

12. **`sphinx_last_updated_by_git`** - Git timestamps
    ```rst
    .. last-updated:: ModuleName
       :format: Last updated: %Y-%m-%d %H:%M
    ```

#### **📝 Documentation & Requirements**
13. **`sphinx_needs`** - Requirements tracking
    ```rst
    .. req:: Agent Configuration
       :id: REQ_AGENT_001
       :status: implemented
       :priority: high
       :tags: agent, config
       
       All agents must have AugLLMConfig engine.
       
    .. test:: Configuration Test
       :id: TEST_AGENT_001
       :status: passed
       :links: REQ_AGENT_001
    ```

14. **`sphinxemoji`** - Rich emoji support
    ```rst
    :emoji:`robot` :emoji:`zap` :emoji:`books` :emoji:`checkmark`
    ```

15. **`sphinx_jinja2`** - Dynamic content generation
    ```rst
    .. jinja::
    
       **Build Information:**
       - Version: {{ version }}
       - Build Date: {{ now.strftime('%Y-%m-%d') }}
       - Extensions: {{ extensions|length }}
    ```

#### **📐 Diagram Extensions**
16. **`sphinxcontrib.mermaid`** - Architecture diagrams
    ```rst
    .. mermaid::
       :caption: Haive Framework Architecture
       
       graph TB
           UI[User Interface] --> Agent[AI Agent]
           Agent --> Tools[External Tools]
           Agent --> Memory[Memory Store]
    ```

#### **🖥️ CLI Documentation** 
17. **`sphinx_click`** - Click CLI documentation
    ```rst
    .. click:: mymodule:cli_command
       :prog: haive
       :nested: full
    ```

18. **`sphinx_argparse`** - Argparse CLI documentation
    ```rst
    .. argparse::
       :module: mymodule
       :func: get_parser
       :prog: haive
    ```

#### **🔧 Enhanced Autodoc**
19. **`sphinx_autodoc_typehints`** - Full type hint support
    ```python
    # Configured in conf.py:
    autodoc_typehints = "description"
    autodoc_typehints_format = "short"
    typehints_document_rtype = True
    ```

20. **`sphinx_copybutton`** - Copy code buttons
    ```python
    # Auto-adds copy buttons to all code blocks
    copybutton_prompt_text = r">>> |\.\.\. |\$ "
    ```

21. **`sphinxcontrib.programoutput`** - Live command output
    ```rst
    .. command-output:: python --version
       :shell:
    ```

22. **`sphinx_inheritance_diagram`** - Class hierarchy visualization
    ```rst
    .. inheritance-diagram:: MyClass
       :parts: 2
       :caption: Class Hierarchy
    ```

---

### 🚫 **CONFIGURED BUT NOT YET UTILIZED**

#### **📊 Diagram Extensions (Ready to Use)**
- **`sphinxcontrib.plantuml`** - UML diagrams
  ```rst
  .. plantuml::
     
     @startuml
     User -> Agent : Request
     Agent -> LLM : Process
     LLM -> Agent : Response
     Agent -> User : Result
     @enduml
  ```

- **`sphinxcontrib.blockdiag`** - Block diagrams
  ```rst
  .. blockdiag::
     
     diagram {
        A -> B -> C;
        B -> D;
     }
  ```

- **`sphinxcontrib.seqdiag`** - Sequence diagrams
  ```rst
  .. seqdiag::
     
     seqdiag {
        User -> Agent -> LLM;
        Agent <-- LLM;
        User <-- Agent;
     }
  ```

- **`sphinxcontrib.nwdiag`** - Network diagrams
  ```rst
  .. nwdiag::
     
     nwdiag {
        internet [shape = cloud];
        internet -- router;
     }
  ```

#### **🎥 Media Extensions**
- **`sphinxcontrib.youtube`** - YouTube video embeds
  ```rst
  .. youtube:: dQw4w9WgXcQ
     :width: 100%
     :height: 315
  ```

#### **📚 Gallery & Examples**
- **`sphinx_gallery.gen_gallery`** - Auto-generated example galleries
  ```python
  # Currently disabled, can be re-enabled
  sphinx_gallery_conf = {
      'examples_dirs': '../examples',
      'gallery_dirs': 'auto_examples',
      'plot_gallery': True,
  }
  ```

#### **🔍 Search & Quality**
- **`sphinxcontrib.spelling`** - Spell checking
  ```python
  # Add to conf.py:
  spelling_lang = 'en_US'
  spelling_show_suggestions = True
  ```

#### **📄 Version Management**
- **`sphinx_multiversion`** - Multi-version documentation
  ```rst
  .. versionadded:: 1.5
     New feature description
     
  .. deprecated:: 2.0
     Use NewClass instead
  ```

- **`sphinx_version_warning`** - Version warnings
- **`sphinx_removed_in`** - Deprecation notices

#### **🎭 Presentation Extensions**  
- **`sphinx_revealjs`** - HTML presentations
- **`hieroglyph`** - Slide presentations

#### **🌐 Web Features**
- **`sphinx_sitemap`** - XML sitemaps
- **`sphinx_notfound_page`** - Custom 404 pages  
- **`sphinx_reredirects`** - URL redirects

---

## 🎯 **HOW TO USE THESE EXTENSIONS**

### **In RST Templates:**

#### **1. Enhanced Class Template:**
```rst
{{ fullname | escape | underline}}

.. card:: 🤖 Class: {{ objname }}
   :class-card: sd-rounded-3 sd-shadow-lg

.. tab-set::

   .. tab-item:: Overview
      :sync: overview
      
      .. autoclass:: {{ objname }}
         :members:
         :show-inheritance:

   .. tab-item:: Live Demo
      :sync: demo
      
      .. exec_code::
         :caption: Test {{ objname }}
         
         from {{ module }} import {{ objname }}
         print(f"✅ Class available: {{ objname }}")

.. req:: Class Requirements
   :id: REQ_{{ objname.upper() }}_001
   :status: implemented
   
.. last-updated:: {{ fullname }}
   :format: Updated: %Y-%m-%d

.. seealso::
   
   * :issue:`new` - Request features
   * :doc:`/examples/index` - Usage examples
```

#### **2. Enhanced Module Template:**
```rst
{{ fullname | escape | underline}}

.. card:: 📦 Module: {{ fullname.split('.')[-1] | title }}

.. autorun::

   import {{ fullname }}
   print(f"📊 Module: {{ fullname }}")
   attrs = [name for name in dir({{ fullname }}) if not name.startswith('_')]
   print(f"🔧 Public items: {len(attrs)}")

.. mermaid::
   :caption: Module Architecture
   
   graph LR
       Module[{{ fullname }}] --> Classes[Classes]
       Module --> Functions[Functions]  
       Module --> Constants[Constants]

.. tippy:`Interactive help <Click elements for details>`
```

#### **3. Enhanced Function Template:**
```rst
{{ fullname | escape | underline}}

.. card:: ⚙️ Function: {{ objname }}

.. autofunction:: {{ objname }}

.. dropdown:: 🧪 Test Function
   :color: success
   :icon: play
   
   .. exec_code::
      
      from {{ module }} import {{ objname }}
      import inspect
      
      sig = inspect.signature({{ objname }})
      print(f"📝 Signature: {{ objname }}{sig}")
      print(f"📋 Parameters: {len(sig.parameters)}")

.. admonition:: 💡 Usage Tips
   :class: tip
   
   * Check :paramlink:`parameters <Parameter documentation>`
   * Use :tippy:`type hints <Python type hints>`
   * Read :emoji:`books` docstring for details
```

### **In Documentation Pages:**

#### **1. Interactive API Documentation:**
```rst
API Reference
=============

.. exec_code::
   :caption: Live API Overview
   
   import haive
   print(f"🤖 Haive Framework v{haive.__version__}")
   print("📊 Available modules:")
   
   modules = ['core', 'agents', 'tools', 'games']
   for module in modules:
       try:
           imported = __import__(f'haive.{module}')
           print(f"  ✅ haive.{module}")
       except:
           print(f"  ❌ haive.{module}")

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: 🤖 Agents
      :shadow: lg
      
      * :doc:`/api/agents/index`
      * :issue:`agent-features` for requests
      
   .. grid-item-card:: 🔧 Tools
      :shadow: lg
      
      * :doc:`/api/tools/index`  
      * :pr:`tool-integrations` for improvements

.. req:: API Completeness
   :id: API_001
   :status: in_progress
   
   All public APIs must have complete documentation.
```

#### **2. Architecture Documentation:**
```rst
Framework Architecture
====================

.. mermaid::
   :caption: Haive Framework Overview
   
   graph TB
       subgraph "User Layer"
           UI[User Interface]
       end
       
       subgraph "Agent Layer"  
           SA[SimpleAgent]
           RA[ReactAgent]
           MA[MultiAgent]
       end
       
       subgraph "Core Layer"
           Engine[AugLLMConfig]
           Memory[Memory Store]
           Tools[Tool Registry]
       end
       
       UI --> SA
       UI --> RA  
       UI --> MA
       
       SA --> Engine
       RA --> Engine
       RA --> Tools
       MA --> SA
       MA --> RA

.. dropdown:: 🔍 Component Details
   :color: info
   :open:
   
   .. tab-set::
   
      .. tab-item:: Agents
         :sync: agents
         
         .. autorun::
         
            agent_types = {
                'SimpleAgent': 'Basic conversational AI',
                'ReactAgent': 'Tool-enabled reasoning',
                'MultiAgent': 'Agent coordination'
            }
            
            for agent, desc in agent_types.items():
                print(f"🤖 {agent}: {desc}")
      
      .. tab-item:: Architecture
         :sync: arch
         
         The framework follows a layered architecture:
         
         * **User Layer**: Interface and API
         * **Agent Layer**: AI agent implementations  
         * **Core Layer**: Engine and utilities

.. seealso::

   * :doc:`/guides/architecture` - Detailed architecture guide
   * :issue:`architecture` - Architecture discussions
   * :commit:`arch-improvements` - Recent changes
```

---

## 🚀 **QUICK WINS - Extensions to Add Next**

### **1. Re-enable sphinx_gallery**
```python
# In conf.py, uncomment:
"sphinx_gallery.gen_gallery",

# Then create examples/ directory with Python files
# They'll auto-generate into beautiful galleries!
```

### **2. Add Diagram Support**
```rst
# Add to architecture docs:
.. plantuml::
   :caption: System Architecture
   
   @startuml
   User -> Agent : Request
   Agent -> Tools : Execute
   Tools -> Agent : Results  
   Agent -> User : Response
   @enduml

.. seqdiag::
   :caption: API Flow
   
   seqdiag {
      User -> API -> Agent -> LLM;
      User <-- API <-- Agent <-- LLM;
   }
```

### **3. Add YouTube Integration**
```rst
# Add video tutorials:
.. youtube:: your-video-id
   :width: 100%
   :height: 400
   
   Tutorial: Building Your First Agent
```

### **4. Add Version Management**
```rst
# Add to API docs:
.. versionadded:: 1.5
   New MultiAgent coordination features
   
.. deprecated:: 2.0
   OldClass is deprecated, use NewClass instead
   
.. versionchanged:: 1.8
   Enhanced parameter validation
```

---

## 📊 **EXTENSION STATUS SUMMARY**

| Category | Extensions | Status | Usage |
|----------|------------|---------|--------|
| **Live Execution** | 3 | ✅ Active | All templates |
| **Interactive** | 4 | ✅ Active | All templates |  
| **Visual Design** | 5 | ✅ Active | Cards, grids, tabs |
| **GitHub Integration** | 3 | ✅ Active | Issues, PRs, commits |
| **Documentation** | 7 | ✅ Active | Requirements, emoji |
| **Diagrams** | 6 | ⏳ Ready | Need to add usage |
| **Media** | 2 | ⏳ Ready | YouTube, presentations |
| **Version Control** | 3 | ⏳ Ready | Multi-version, warnings |
| **Quality** | 4 | ⏳ Ready | Spelling, search |
| **Web Features** | 4 | ⏳ Ready | Sitemap, redirects |

**Total**: 86+ extensions configured, 22+ actively used, 20+ ready for quick integration

---

## 🎯 **NEXT STEPS**

1. **Enable sphinx_gallery** - Auto-generated example galleries
2. **Add diagram templates** - PlantUML, sequence diagrams  
3. **Integrate YouTube** - Video tutorials in docs
4. **Add version warnings** - Deprecation and version notices
5. **Enable spell checking** - Professional quality control

**Result**: Complete utilization of all 86+ configured Sphinx extensions for world-class documentation! 🌟