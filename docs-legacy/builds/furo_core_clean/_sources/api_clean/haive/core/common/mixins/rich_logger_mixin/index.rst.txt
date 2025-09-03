
haive.core.common.mixins.rich_logger_mixin
==========================================

.. py:module:: haive.core.common.mixins.rich_logger_mixin

.. autoapi-nested-parse::

   Rich logging mixin for enhanced console output.

   This module provides a mixin for adding rich console logging capabilities to
   Pydantic models. It leverages the Rich library to enable colorized, formatted
   console output with features like syntax highlighting and rich traceback display.

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins import RichLoggerMixin

       class MyProcessor(RichLoggerMixin, BaseModel):
           name: str

           def process(self, data):
               self._info(f"Processing data with {self.name}")
               try:
                   # Processing logic
                   result = self._process_data(data)
                   self._debug(f"Processed result: {result}")
                   return result
               except Exception as e:
                   self._error(f"Failed to process data: {e}")
                   raise

       # Create with debug enabled
       processor = MyProcessor(name="TestProcessor", debug=True)
       processor.process({"test": "data"})
       ```







Classes
-------

* :py:class:`RichLoggerMixin` - Mixin that provides rich console logging capabilities.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/rich_logger_mixin/RichLoggerMixin

Package Contents
----------------

