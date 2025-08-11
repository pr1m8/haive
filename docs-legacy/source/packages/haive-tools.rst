haive-tools
===========

Tool library for extending agent capabilities.

Overview
--------

The ``haive-tools`` package provides a comprehensive toolkit for AI agents:

- **Web Tools** - Search, scraping, and API access
- **File Tools** - File operations and document processing  
- **Data Tools** - Data manipulation and analysis
- **Integration Tools** - Third-party service connections
- **Custom Tools** - Framework for building your own tools

Installation
------------

.. code-block:: bash

   pip install haive-tools

Or as part of the full framework:

.. code-block:: bash

   pip install haive

Quick Start
-----------

.. code-block:: python

   from haive.tools import tool
   from haive.tools.web import WebSearchTool
   from haive.tools.file import FileReaderTool
   
   # Use pre-built tools
   search = WebSearchTool()
   reader = FileReaderTool()
   
   # Create custom tools
   @tool
   def word_counter(text: str) -> int:
       """Count words in text."""
       return len(text.split())

Tool Categories
---------------

Web Tools
^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: WebSearchTool
      :link: ../api/tools/web/search/index
      :link-type: doc

      Web search capabilities
      
      - Multiple search engines
      - Result ranking
      - Content extraction
      - Safe search options

   .. grid-item-card:: WebScraperTool
      :link: ../api/tools/web/scraper/index
      :link-type: doc

      Web content extraction
      
      - HTML parsing
      - Content cleaning
      - Link extraction
      - JavaScript support

File Tools
^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: FileReaderTool
      :link: ../api/tools/file/reader/index
      :link-type: doc

      File reading operations
      
      - Text files
      - JSON/YAML/CSV
      - PDF extraction
      - Encoding detection

   .. grid-item-card:: FileWriterTool
      :link: ../api/tools/file/writer/index
      :link-type: doc

      File writing operations
      
      - Safe writing
      - Format conversion
      - Append modes
      - Backup creation

Data Tools
^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: DataAnalysisTool
      :link: ../api/tools/data/analysis/index
      :link-type: doc

      Data analysis functions
      
      - Statistical analysis
      - Data visualization
      - Trend detection
      - Report generation

   .. grid-item-card:: DatabaseTool
      :link: ../api/tools/data/database/index
      :link-type: doc

      Database operations
      
      - SQL queries
      - Multiple DB support
      - Connection pooling
      - Transaction support

Core Tool Classes
-----------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.tools.base.BaseTool
   haive.tools.decorator.tool
   haive.tools.toolkit.Toolkit

Web Tools
---------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.tools.web.search.WebSearchTool
   haive.tools.web.scraper.WebScraperTool
   haive.tools.web.browser.BrowserTool
   haive.tools.web.api.APITool

File Tools
----------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.tools.file.reader.FileReaderTool
   haive.tools.file.writer.FileWriterTool
   haive.tools.file.manager.FileManagerTool
   haive.tools.document.loader.DocumentLoaderTool

Data Tools
----------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.tools.data.analysis.DataAnalysisTool
   haive.tools.data.database.DatabaseTool
   haive.tools.data.csv.CSVTool
   haive.tools.data.json.JSONTool

Tool Functions
--------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/function.rst

   haive.tools.decorator.tool
   haive.tools.utils.validate_tool_args
   haive.tools.utils.tool_error_handler

Creating Custom Tools
---------------------

Basic Tool
^^^^^^^^^^

.. code-block:: python

   from haive.tools import tool
   
   @tool
   def calculate_area(length: float, width: float) -> float:
       """Calculate area of a rectangle.
       
       Args:
           length: Length of the rectangle
           width: Width of the rectangle
           
       Returns:
           Area of the rectangle
       """
       return length * width

Tool with Validation
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.tools import tool
   from pydantic import Field
   
   @tool
   def send_email(
       to: str = Field(..., description="Recipient email"),
       subject: str = Field(..., description="Email subject"),
       body: str = Field(..., description="Email body")
   ) -> dict:
       """Send an email with validation."""
       # Validate email format
       if "@" not in to:
           return {"error": "Invalid email address"}
       
       # Send email logic here
       return {"status": "sent", "to": to}

Tool Class
^^^^^^^^^^

.. code-block:: python

   from haive.tools.base import BaseTool
   from typing import Type
   from pydantic import BaseModel, Field
   
   class WeatherInput(BaseModel):
       """Input for weather tool."""
       city: str = Field(description="City name")
       units: str = Field(default="celsius", description="Temperature units")
   
   class WeatherTool(BaseTool):
       """Get weather information."""
       
       name = "weather"
       description = "Get current weather for a city"
       args_schema: Type[BaseModel] = WeatherInput
       
       def _run(self, city: str, units: str = "celsius") -> str:
           """Execute the weather lookup."""
           # Implementation here
           return f"Weather in {city}: 20°{units[0].upper()}"

Complete API Reference
----------------------

For the complete API documentation with all tools:

.. toctree::
   :maxdepth: 3

   ../api/tools/index

Tool Integration
----------------

With SimpleAgent
^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.agents.simple.agent_v3 import SimpleAgentV3
   from haive.tools.web import WebSearchTool
   
   agent = SimpleAgentV3(
       name="researcher",
       engine=AugLLMConfig(),
       tools=[WebSearchTool()]
   )
   
   result = await agent.arun("Search for Python tutorials")

With ReactAgent
^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.agents.react.agent import ReactAgent
   from haive.tools import tool
   
   @tool
   def calculator(expression: str) -> str:
       """Evaluate math expressions."""
       return str(eval(expression))
   
   agent = ReactAgent(
       name="math_helper",
       engine=AugLLMConfig(),
       tools=[calculator, WebSearchTool()]
   )

Tool Kits
^^^^^^^^^

.. code-block:: python

   from haive.tools.kits import ResearchToolkit, DataToolkit
   
   # Pre-configured tool collections
   research_tools = ResearchToolkit()  # Web search, scraping, summarization
   data_tools = DataToolkit()  # CSV, JSON, SQL, analysis
   
   agent = ReactAgent(
       name="analyst",
       tools=research_tools.get_tools() + data_tools.get_tools()
   )

Best Practices
--------------

1. **Use descriptive names** and docstrings for tools
2. **Validate inputs** using Pydantic models
3. **Handle errors gracefully** and return informative messages
4. **Keep tools focused** on a single responsibility
5. **Test tools independently** before agent integration
6. **Document expected outputs** clearly

Tool Development Guidelines
---------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Guideline
     - Description
   * - **Single Purpose**
     - Each tool should do one thing well
   * - **Clear Interface**
     - Well-defined inputs and outputs
   * - **Error Handling**
     - Graceful failure with helpful messages
   * - **Async Support**
     - Implement async versions when beneficial
   * - **Documentation**
     - Comprehensive docstrings with examples

Related Documentation
---------------------

- :doc:`../guide/tools` - Tool development guide
- :doc:`../api/tools/index` - Complete tools API reference
- :doc:`haive-agents` - Agents that use tools
- :doc:`../examples/index` - Tool usage examples