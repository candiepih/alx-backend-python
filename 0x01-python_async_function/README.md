# Python - Async

This topic was created to understand what async is and how to execute async program with asyncio.

The objectives of the topic were as follows:-
* The `async` and `await` syntax 
* How to execute an async program with `asyncio`
* How to run concurrent coroutines 
* How to create `asyncio` tasks 
* How to use the `random` module

## Files

[0-basic_async_syntax.py](./0-basic_async_syntax.py)

"Contains a coroutine that delays a certain amount of time and returns it

[1-concurrent_coroutines.py](./1-concurrent_coroutines.py)

Contains a method that spawns wait_random n times with a
specified delay between each call.

[2-measure_runtime.py](./2-measure_runtime.py)

Contains a method that measure the total execution time of
a function

[3-tasks.py](./3-tasks.py)

Contains a method that returns a task

[4-tasks.py](./4-tasks.py)

Contains a method that spawns Tasks n times with a
specified delay between each call.