
haive.core.common.types.abc_root_wrapper
========================================

.. py:module:: haive.core.common.types.abc_root_wrapper

.. autoapi-nested-parse::

   from typing import Any
   This module provides an abstract base class for root-wrapped models that serialize with a named key.

   This is useful for models that are used as the root of a response, but need to be serialized with a named key.

   For example, if you have a model like this:
   ```python
   class Query(ABCRootWrapper[str]):
       pass
   ```

   It will serialize as `{"query": "Hello, world!"}` instead of `{"root": "Hello, world!"}`.







Classes
-------

* :py:class:`ABCRootWrapper` - Abstract base class for root-wrapped models that serialize with a named key
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/types/abc_root_wrapper/ABCRootWrapper

Package Contents
----------------

