import asyncio
import time
from fastapi import FastAPI

app = FastAPI()

@app.get("/1")
async def endpoint1(): # process sequentially
    """
    - If you send multiple request using this way, your fastapi handle one request at one time and another request 
    after completing first request. It is handled synchronously one by one.
    - time.sleep is Blocking I/O operation, can not awaited, function execution cannot be paused, instead
    event loop is blocked while waiting for the result
    - Here is no point of adding async keyword there because you method is not waiting anywhere in the code.
    """
    print("Hello!!!")
    time.sleep(5) # Blocking operation
    print("Bye!!!")
    return "Hello world"


@app.get("/2")
async def endpoint2(): # process concurrently
    """
    - If you send multiple request using this way, your fastapi handle request concurrently. Because you use the 
    property async/await which make sure if your current thread is waiting for something then its better to
    do other job instead of keeping your cpu idle.
    - Your asyncio is non-blocking I/O operation, awaited, function executing paused while waiting operation to finished
    During this paused the event loop can handle processing other request.
    - For using await, it is mandatory to use async keyword in front of it.
    """
    print("Hello!!!")
    await asyncio.sleep(5)
    print("Bye!!!")
    return "Hello world"



@app.get("/3")
def endpoint3(): # process parrallely
    """
    - If you send multiple request using this way, your fastapi handle request concurrently.
    """
    print("Hello!!!")
    time.sleep(5)
    print("Bye!!!")
    return "Hello world"


"""
1. When you start your fastapi using uvicorn. It start a thread which is known as main thread.
2. All the end point which is defined as couroutine runs direclty in the event loop which run in main thread.
3. For normal function, it runs in different threads. When a thread is blocked on I/O, it releases the GIL. 
So another thread can run — this is where multithreading shines in Python.
"""


"""
BEST PRACTICES:
1. Use async def for endpoint with non blocking I/O operations.
2. Don't use async def with blocking I/O operations.
3. Use Normal function for blocking I/O operations. (DB cline library which doesn't have await feature, time module)
"""

"""
Important:
1. async def endpoints run on the event loop (single thread, cooperative multitasking).
2. def endpoints run on worker threads via a threadpool (like concurrent.futures.ThreadPoolExecutor)
"""