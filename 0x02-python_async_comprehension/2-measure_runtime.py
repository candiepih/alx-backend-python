#!/usr/bin/env python3
"""Contains a method that measures the runtime of a function."""
from time import perf_counter
import asyncio
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Measures the runtime of an async coroutine running 4 times

    Returns:
        float: the runtime of the coroutine

    """
    start = perf_counter()
    tasks = [asyncio.create_task(async_comprehension()) for _ in range(4)]
    await asyncio.gather(*tasks)
    elapsed = perf_counter() - start
    return elapsed
