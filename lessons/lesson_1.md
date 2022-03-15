# Lesson 1

In this first lesson, we will install the IDE on our computer, flash Micropython onto the ESP8266, and run and understand a simple webserver.

This lesson basically combines the following tutorials:

* https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/
* https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/

## Introduction to Python

The tutorials do not cover an introduction to Python as a programming language. Thus we here highlight a few key language features the
webserver tutorial uses.

### Import Statements

Import statements extend Python by loading so-called modules, or parts defined there-in. For now, we assume that Python knows where to find
them, and instead focus on how to tell Python to load what we need.

In the tutorial, the following imports are defined, which also show the various flavors of imports (let's ignore the `try` and `except` part for now):

```python
try:
  import usocket as socket  # case 1
except:
  import socket

from machine import Pin  # case 2
import network  # case 3
```

1. tells Python to import a module `usocket` but give it a different name we can refer to. The syntax is `import MODULE as REFERENCE`. This is
   useful to e.g. avoid name collisions, inc case two modules define functions or classes of the same name. Here it is used to harmonize names,
   i.e. to refer to two different modules (`usocket` and `socket`) by the same reference for the remainder of the code.
2. tells Python to import only the `Pin` class from the `machine` module. The syntax is `from MODULE import ClassA, ClassB, function1`. It is good
   practice to only import what we use. Side note: how do we know it's a class, not a funciton or variable. Well actually, we don't but by convention
   classes should start with a upper-case letter and functions with a lower-case letter.
3. here the entire `network` module is imported. We can then refer to parts of it using `network.SOMETHING`.

### Calling functions

Next up in our example a function is called:

```python
import esp
esp.osdebug(None)
```

We already learned that this function is part of the `esp` module, which we import. It takes a single parameter: `None`, which is a special type in
Python. We also see that function calls are indicated by `()`. Functions can have any number of parameters, and parameters can be mandatory, or
so-called `keyword` arguments, which have defaults defined. The following variants are common to occur:


```python

# a function without any arguments
def func1():
   print("Hello")  # note how `print` also is a function
   
func1()  # it is called like this


# a function with arguments a and b
def func2(a, b):
   print(a + b)
   
func2(1, 2)  # called like this, and will print 3

def func3(a, c=2, d=0):
   return a - b  + d
   

func3(2)  # will return 0, and uses 2 as the default value for c, and 0 for d
func3(2, 0)  # will return 2, as we have set c to 0 now and keep d := 0
func3(2, d=1, c=1)  # will return 2, note how when addressing the keyword parameters by name, the order does not matter
```

We've also introduced `#` to signify comments, and `return` statements to return values from functions at this point.

### Variable Assignment

Next in out example we assign variables on a module level:

```python
ssid = 'REPLACE_WITH_YOUR_SSID'
password = 'REPLACE_WITH_YOUR_PASSWORD'

station = network.WLAN(network.STA_IF)
```

Assignment is indicated by the `=` operator (to compare equality, use `==` instead). As you can see we can assign constant expressions,
or the return value from a function using the same syntax. Python is dynamically types, so the type of a variable will depend on what
is currently assinged to it:

```python

a = 1  # a is an integer variable
a = 1.0  # now a is a floating point variable
a = 'Hello'  # we've now made a a string
b = (1, 2)  # b is a tuple of two integers
a = b  # now a is also a tuple of two integers
a = [1, 'Hello']  # now its a list containing an integer and a string
a = {"a": "b"}  # finally it's a dictionary
```

We've learned a few built-in types in the process: Integers, Floats, Strings, Tuples, Lists, and Dictionaries. The first three are 
quite obvious. Tuples and lists are sequence containers, the difference being that a tuple is immutable, i.e. once defined you cannot
alter it's length or members, which a list is mutable:

```
b = ["Hello"]
b.append("World")
b[0] = "Hi"
```
has created `b := ["Hi", "World"]`. Finally, a dictionary is a key-value container:

```
c = {"Hello": 1, "World": 2}
c[2.0] = 42  # extends c by adding 42 under key 2.0
c["Hello"]  # will return 1
```
As you can see, keys can be of many types.

### Control Structures

Python supports the common control structures `if`, `for` and `while`. Let's start with `while` as in our example:

```python
while station.isconnected() == False:
  pass
```

 This will untile the condition `station.isconnected() == False` evaluates to `True`, i.e. `station.isconnected()` return `True`.
 We could have also written
 
 ```python
while not station.isconnected():
  pass
```

thereby making use of the `not` keyword, and the implicit assumption of `while` and `if` evaluating against a `True` value. While
loops are thus useful to loop until an boolean exit condition is met. We should also note the `pass` statement here. It is necessary,
as structure in Python is indicated by indention level. In practice it is a no-op statement, i.e. it does nothing aside from 
provide for syntactical correctness.

For loops are useful to iterate over a sequence:

```python
for i in range(10):
    print(i)
    
for element in some_list:
    pass
    
for key, value in a_dictionary.items():
    pass
```

Here we iterate over the sequence if `i`s returned by the `range` generator, a `list`'s elements, and a `dictionary`'s keys and values.

Finally, `if` constructs allow for conditional program flow:

```
if something() == True:  # or if something()
   # 1 ...
elif a == "Foo":
   # 2 ...
else: 
   # 3...
```

will execute the first block in case the `something()` function evaluates (returns) `True`, otherwise check if the second block is to be
execute (i.e.  variable `a` is equal to the string "Foo"), and finally, if neither the first or second condition are met, execute the third block.
Note that you can have any number of `elif` statements in an `if`, `elif`, `else` construct.
 
### Multiline Strings

The final syntax contruct introduced in the example is the multiline string `""" ... """`. This is useful for expressing longer strings, including
linebreaks. Which might be especially handy if we follow the `PEP8` guideline of <80 chars per line:

```python

"""
This is a long string

which also has an empty new line in it
"""
```

You will commonly encounter multiline strings in so-called `doc-strings`, i.e. in-line code documentation:

```python
def foo():
  """ foo is a recurring example function
  
  A function of name foo should be included in any Python tutorial
  """
  pass
```


## Homework

Change the webserver such that there is a single button, which is labelled "Read Values". For now all this button shoudl do is light up the LED for 5 seconds,
and then switch it off again. You will likely need the `time.sleep` function for this.
