#!/usr/bin/env python3
"""Contains the async_comprehension function."""
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Collects 10 random numbers using async comprehensive
    over async_generator.

    Returns:
        A list of 10 random numbers.
    """
    return [i async for i in async_generator()]
