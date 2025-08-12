
:py:mod:`core`
==============

.. py:module:: core

Core functionality module.

This package provides the core business logic, data structures,
and utilities for the application. It includes exception handling,
data models, services, and various utility functions.

Modules:
    exceptions: Custom exception hierarchy
    data_structures: Core data structures using dataclasses
    services: Service layer implementations
    utils: Utility functions and helpers

.. rubric:: Example

>>> from core import Task, TaskService, Priority
>>> from core.utils import generate_id, Timer
>>>
>>> # Create a new task
>>> task = Task(
...     id=generate_id("task"),
...     title="Complete documentation",
...     priority=Priority.HIGH
... )


.. autolink-examples:: core
   :collapse:

Classes
-------

.. autoapisummary::

   core.InMemoryTaskRepository
   core.MetricsCollector
   core.Point
   core.Priority
   core.RateLimiter
   core.Repository
   core.Result
   core.Status
   core.Task
   core.TaskService
   core.Timer


Module Contents
---------------




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for InMemoryTaskRepository:

   .. graphviz::
      :align: center

      digraph inheritance_InMemoryTaskRepository {
        node [shape=record];
        "InMemoryTaskRepository" [label="InMemoryTaskRepository"];
        "Repository[core.data_structures.Task]" -> "InMemoryTaskRepository";
      }

.. autoclass:: core.InMemoryTaskRepository
   :members:
   :undoc-members:
   :show-inheritance:




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for MetricsCollector:

   .. graphviz::
      :align: center

      digraph inheritance_MetricsCollector {
        node [shape=record];
        "MetricsCollector" [label="MetricsCollector"];
      }

.. autoclass:: core.MetricsCollector
   :members:
   :undoc-members:
   :show-inheritance:




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Point:

   .. graphviz::
      :align: center

      digraph inheritance_Point {
        node [shape=record];
        "Point" [label="Point"];
      }

.. autoclass:: core.Point
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **Point** is a dataclass. Enhanced schema documentation will be available soon.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Priority:

   .. graphviz::
      :align: center

      digraph inheritance_Priority {
        node [shape=record];
        "Priority" [label="Priority"];
        "enum.Enum" -> "Priority";
      }

.. autoclass:: core.Priority
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **Priority** is an Enum defined in ``core``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for RateLimiter:

   .. graphviz::
      :align: center

      digraph inheritance_RateLimiter {
        node [shape=record];
        "RateLimiter" [label="RateLimiter"];
      }

.. autoclass:: core.RateLimiter
   :members:
   :undoc-members:
   :show-inheritance:




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Repository:

   .. graphviz::
      :align: center

      digraph inheritance_Repository {
        node [shape=record];
        "Repository" [label="Repository"];
        "abc.ABC" -> "Repository";
        "Generic[T]" -> "Repository";
      }

.. autoclass:: core.Repository
   :members:
   :undoc-members:
   :show-inheritance:




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Result:

   .. graphviz::
      :align: center

      digraph inheritance_Result {
        node [shape=record];
        "Result" [label="Result"];
        "Generic[T]" -> "Result";
      }

.. autoclass:: core.Result
   :members:
   :undoc-members:
   :show-inheritance:




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Status:

   .. graphviz::
      :align: center

      digraph inheritance_Status {
        node [shape=record];
        "Status" [label="Status"];
        "enum.Enum" -> "Status";
      }

.. autoclass:: core.Status
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **Status** is an Enum defined in ``core``.





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Task:

   .. graphviz::
      :align: center

      digraph inheritance_Task {
        node [shape=record];
        "Task" [label="Task"];
      }

.. autoclass:: core.Task
   :members:
   :undoc-members:
   :show-inheritance:




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for TaskService:

   .. graphviz::
      :align: center

      digraph inheritance_TaskService {
        node [shape=record];
        "TaskService" [label="TaskService"];
      }

.. autoclass:: core.TaskService
   :members:
   :undoc-members:
   :show-inheritance:




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for Timer:

   .. graphviz::
      :align: center

      digraph inheritance_Timer {
        node [shape=record];
        "Timer" [label="Timer"];
      }

.. autoclass:: core.Timer
   :members:
   :undoc-members:
   :show-inheritance:


Functions
---------

.. autoapisummary::

   core.batch
   core.deep_merge
   core.find_files
   core.format_bytes
   core.generate_id
   core.hash_password
   core.memoize
   core.parse_size
   core.retry
   core.safe_json_loads
   core.slugify
   core.timedelta_to_human
   core.truncate_string
   core.validate_email

.. py:function:: batch(iterable, size: int)

   Split iterable into batches.

   :param iterable: Input iterable
   :param size: Batch size

   :Yields: Batches of specified size

   .. rubric:: Example

   >>> list(batch([1, 2, 3, 4, 5], 2))
   [[1, 2], [3, 4], [5]]


   .. autolink-examples:: batch
      :collapse:

.. py:function:: deep_merge(dict1: Dict, dict2: Dict) -> Dict

   Deep merge two dictionaries.

   :param dict1: Base dictionary
   :param dict2: Dictionary to merge in

   :returns: Merged dictionary (dict1 is modified)

   .. rubric:: Example

   >>> d1 = {"a": 1, "b": {"c": 2}}
   >>> d2 = {"b": {"d": 3}, "e": 4}
   >>> deep_merge(d1, d2)
   {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}


   .. autolink-examples:: deep_merge
      :collapse:

.. py:function:: find_files(directory: Union[str, pathlib.Path], pattern: str = '*', recursive: bool = True) -> List[pathlib.Path]

   Find files matching pattern in directory.

   :param directory: Directory to search
   :param pattern: Glob pattern (default: "*")
   :param recursive: Search subdirectories

   :returns: List of matching file paths

   .. rubric:: Example

   >>> find_files("src", "*.py")
   [Path('src/main.py'), Path('src/utils.py'), ...]


   .. autolink-examples:: find_files
      :collapse:

.. py:function:: format_bytes(num_bytes: int, precision: int = 2) -> str

   Format bytes to human-readable string.

   :param num_bytes: Number of bytes
   :param precision: Decimal precision

   :returns: Formatted size string

   .. rubric:: Example

   >>> format_bytes(1536)
   '1.50 KB'


   .. autolink-examples:: format_bytes
      :collapse:

.. py:function:: generate_id(prefix: str = '', length: int = 8) -> str

   Generate a random ID with optional prefix.

   :param prefix: Optional prefix for the ID
   :param length: Length of random part (default: 8)

   :returns: Generated ID string

   .. rubric:: Example

   >>> generate_id("user", 6)
   'user_a3k9x2'


   .. autolink-examples:: generate_id
      :collapse:

.. py:function:: hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]

   Hash password with salt using SHA-256.

   :param password: Plain text password
   :param salt: Optional salt (generated if not provided)

   :returns: Tuple of (hashed_password, salt)

   .. note::

      This is a simple example. Use bcrypt or similar
      for production password hashing.


   .. autolink-examples:: hash_password
      :collapse:

.. py:function:: memoize(maxsize: int = 128)

   Decorator for memoizing function results.

   :param maxsize: Maximum cache size

   .. rubric:: Example

   >>> @memoize(maxsize=100)
   ... def expensive_function(x):
   ...     return x ** 2


   .. autolink-examples:: memoize
      :collapse:

.. py:function:: parse_size(size_str: str) -> int

   Parse human-readable size string to bytes.

   :param size_str: Size string (e.g., "10MB", "1.5GB")

   :returns: Size in bytes

   .. rubric:: Example

   >>> parse_size("10MB")
   10485760
   >>> parse_size("1.5GB")
   1610612736


   .. autolink-examples:: parse_size
      :collapse:

.. py:function:: retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0)

   Decorator for retrying failed operations.

   :param max_attempts: Maximum number of retry attempts
   :param delay: Initial delay between retries in seconds
   :param backoff: Backoff multiplier for each retry

   .. rubric:: Example

   >>> @retry(max_attempts=3, delay=0.5)
   ... async def flaky_operation():
   ...     # Operation that might fail
   ...     pass


   .. autolink-examples:: retry
      :collapse:

.. py:function:: safe_json_loads(json_str: str, default: Any = None) -> Any

   Safely parse JSON with default fallback.

   :param json_str: JSON string to parse
   :param default: Default value if parsing fails

   :returns: Parsed JSON or default value


   .. autolink-examples:: safe_json_loads
      :collapse:

.. py:function:: slugify(text: str, max_length: Optional[int] = None) -> str

   Convert text to URL-friendly slug.

   :param text: Input text to slugify
   :param max_length: Maximum length of slug

   :returns: URL-friendly slug

   .. rubric:: Example

   >>> slugify("Hello World! 123")
   'hello-world-123'


   .. autolink-examples:: slugify
      :collapse:

.. py:function:: timedelta_to_human(td: datetime.timedelta) -> str

   Convert timedelta to human-readable string.

   :param td: Timedelta object

   :returns: Human-readable duration string

   .. rubric:: Example

   >>> timedelta_to_human(timedelta(days=2, hours=3, minutes=15))
   '2 days, 3 hours, 15 minutes'


   .. autolink-examples:: timedelta_to_human
      :collapse:

.. py:function:: truncate_string(text: str, max_length: int, suffix: str = '...') -> str

   Truncate string to maximum length.

   :param text: Text to truncate
   :param max_length: Maximum length
   :param suffix: Suffix to append if truncated

   :returns: Truncated string

   .. rubric:: Example

   >>> truncate_string("Hello, World!", 10)
   'Hello, ...'


   .. autolink-examples:: truncate_string
      :collapse:

.. py:function:: validate_email(email: str) -> bool

   Validate email address format.

   :param email: Email address to validate

   :returns: True if valid email format

   .. rubric:: Example

   >>> validate_email("user@example.com")
   True
   >>> validate_email("invalid.email")
   False


   .. autolink-examples:: validate_email
      :collapse:



.. rubric:: Related Links

.. autolink-examples:: core
   :collapse:
   
.. autolink-skip:: next
