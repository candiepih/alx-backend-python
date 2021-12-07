#!/usr/bin/env python3
"""Contains an async generator function."""
import random
import asyncio
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """
    An async generator function that yields a random float.

    Returns:
        The yielded float value.
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
