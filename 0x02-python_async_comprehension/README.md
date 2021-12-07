# Python - Async Comprehension

This topic's aim was to understand the following concepts:

* How to write an asynchronous generator 
* How to use async comprehensions 
* How to type-annotate generators

## Files

The following task files were used to test various concepts:

[0-async_generator.py](./0-async_generator.py)

Contains an async generator function that yields a random float.

[1-async_comprehension.py](./1-async_comprehension.py)

Contains the async_comprehension function that collects 10 random numbers using async comprehensive over async_generator.

[2-measure_runtime.py](./2-measure_runtime.py)

Contains a method that measures the runtime of an async coroutine running 4 times