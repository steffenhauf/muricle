# Lesson 3

In this lesson we introduce asyncio into the project. So far we've handled
all our sensors and serving the webpage in synchronous, i.e. sequentially.
This works well for projects which do not need to act on external input,
and provide (near) realtime feedback.

For projects that require such  communication, synchronuous behaviour can be
problematic. Image a TCP request coming in to measure from user Alice. This
request now triggers sensors which need multiple seconds to measure. A user
Bob would now not be able to perform any request during the time the
measurements are happening.

Here, asynchronous programming can help. The measurements (and also serving
the page) are so-called input/output (I/O) bound task: the CPU waits on
an input or output task to complete, while it itself has not much to do.
In an asyncronous scenario, the CPU can use this time to do other tasks,
e.g. importantly, trigger more I/O bound tasks. In this lesson we refactor
the code to do exactly that: we call the measurement asyncronously as
we know it can take some time. In the meantime the CPU can server e.g. another
request from a different user.

## Introduction to Python Continued ... Asyncio

Have a look at https://github.com/steffenhauf/muricle/pull/3 which refactors
our project so far into `asyncio` sensor handling.

Let's start with the straight forward change in `sensor.py` and the various
concrete sensor classes. What used to be

```python
def measure(self):
    ...

```

turns into


```python
async def measure(self):
    ...

```

The `async` key word declares a asyncronous function, also known as a
coroutine, i.e. one that can be scheduled on a so called event loop (more on
that later), and potentially can be suspended during its operation. Async.
functions return so-called futures. As the name already indicates a future
is not guaranteed to have a value at the time it is returned, but can
be `await`ed until it has a value, or checked if a value now exists. Because
of these futures, asyncronous programs are non-sequential: a result might
have to be revisited at a later point in time when its ready and can be
used.

We've implemented this pattern in the `Blinker` class, where we
now would like to wait for a given amount of time, which can be quite long,
and the switch off the LED again.

```
async def _reset_blink(self):
     await uasyncio.sleep(self.blink_duration)
     # turns off the led
     self.led.value(1)
```

The `_reset_blink` function `await`s the value of the future `uasyncio.sleep`
returns. In this case the value is `None`, so we don't use it, but it
takes `self.blink_duration` to be returned. It then turns the led off again.

The function `_reset_blink` is not called in the usual way, but scheduled
on the event loop to run (semi) concurrently with other tasks, i.e. it does
not block. It run semi-concurrently, as the interpreter will slice out a
bit of time once in a while to run it, interrupting other tasks, rather than
guaranteeing fully concurrent execution. This works because the `sleep`
function can be considered an I/O bound tasks. Its internals are such that
calling it and importantly waiting for its result will not block the rest of
the interpreter. Hence

```python
loop.create_task(self._reset_blink())
```

will return immediately, while in the background `_reset_blink` is still
running.

### The asyncio Event Loop

From the Python documentation: "The event loop is the core of every asyncio
application. Event loops run asynchronous tasks and callbacks,
perform network IO operations, and run subprocesses."

One can thus think of the event loop as an arbiter which schedules and
executes tasks, and notifies of their results. Importanly, event loops in
Python do not guarantee any actual concurrency in this, which due to the
global interpreter lock might be hard to acheive anyway. Rather, they provide
a framework to run work in the background (from the Python interpreter
perspective), such that the interpreter can continue elsewhere. In practice,
e.g. on our single core microcontroller this backgrounding leads to a time
slicing of this work, which is dense enough to leave the impression of
concurrent task handling.

Event loops scale extremeley well for I/O heavy tasks, especially if `awaited`
work actually can run concurrently in another thread (like on large servers).
Even with the global interpreter lock in Python this might well be possible
as an I/O function might call code which releases the GIL until it is done.

For a more complete example on Pythons `asyncio` visit e.g. :
https://realpython.com/async-io-python/