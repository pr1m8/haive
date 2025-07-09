"""
Protocol definitions for the Haive engine system.

This module defines protocol classes that establish common interfaces
for various components in the Haive framework. These protocols enable
static type checking, runtime type checking, and duck typing for components
that implement common behaviors.
"""

from typing import Protocol, TypeVar, runtime_checkable

# Type variables
I = TypeVar("I")  # Input type
O = TypeVar("O")  # Output type


@runtime_checkable
class Invokable(Protocol[I, O]):
    """
    Protocol for objects that can be invoked synchronously.

    Defines a common interface for any object that can process
    input data and return output data through an invoke method.
    This enables consistent interaction with different components
    that share this capability.

    Type Parameters:
        I: The input data type.
        O: The output data type.

    Examples:
        >>> from typing import Dict, Any
        >>> class MyProcessor:
        ...     def invoke(self, input_data: str, **kwargs) -> Dict[str, Any]:
        ...         return {"processed": input_data.upper()}
        ...
        >>> processor = MyProcessor()
        >>> from haive.core.engine.base.protocols import Invokable
        >>> isinstance(processor, Invokable)
        True
        >>> result = processor.invoke("hello")
        >>> result
        {'processed': 'HELLO'}
    """

    def invoke(self, input_data: I, **kwargs) -> O:
        """
        Process input data and return output data.

        Args:
            input_data (I): The input data to process.
            **kwargs: Additional keyword arguments for processing.

        Returns:
            O: The processed output data.
        """
        ...


@runtime_checkable
class AsyncInvokable(Protocol[I, O]):
    """
    Protocol for objects that can be invoked asynchronously.

    Defines a common interface for any object that can process
    input data and return output data through an asynchronous
    ainvoke method. This allows for non-blocking invocation of
    components that implement this interface.

    Type Parameters:
        I: The input data type.
        O: The output data type.

    Examples:
        >>> import asyncio
        >>> from typing import Dict, Any
        >>> class MyAsyncProcessor:
        ...     async def ainvoke(self, input_data: str, **kwargs) -> Dict[str, Any]:
        ...         await asyncio.sleep(0.1)  # Simulate async work
        ...         return {"processed": input_data.upper()}
        ...
        >>> processor = MyAsyncProcessor()
        >>> from haive.core.engine.base.protocols import AsyncInvokable
        >>> isinstance(processor, AsyncInvokable)
        True
        >>> # Usage in an async context
        >>> async def process():
        ...     result = await processor.ainvoke("hello")
        ...     print(result)
        >>> # {'processed': 'HELLO'}
    """

    async def ainvoke(self, input_data: I, **kwargs) -> O:
        """
        Process input data asynchronously and return output data.

        Args:
            input_data (I): The input data to process.
            **kwargs: Additional keyword arguments for processing.

        Returns:
            O: The processed output data.
        """
        ...
