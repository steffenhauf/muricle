# Lesson 2

In this lesson we will refactor (i.e. update and improve) our code from
lesson two into a design which allows us to more easily extend the
functionality of our microcontroller with additional sensors in the future.

For this lesson, since we still lack any meaninful read-back sensor, we
will treat the built-in LED of the ESP8266 as a sensor, and switch it on
and off.

The refactoring can be found in the following pull request (PR):
https://github.com/steffenhauf/muricle/pull/1/files and comments have
been added to describe the design choices.

## Introduction to Python Continued ... Classes

In the PR of this lecture we introduces classes into our project. In the
suggested design, each sensor is a `class` which derives from a base class
`Sensor`. By doing so we follow the object-oriented programming
(https://en.wikipedia.org/wiki/Object-oriented_programming) design
pattern of `inheritance`.

In Python a class is defined such

```python

class Foo:

    b = 1

    def __init__(self, a):
        self.a = a

    def bar(self):
        print(self.a + self.b)
```

By convention class names are capitalized. Everything that is part of the
class is indented by 4 spaces. Parts of the class definition can be

* class variables (in our example `b`), which will be common among all
    instances of a class.
* instance variables (`self.a` in the example) which a distinct for each
    instance of a class
* special class methods, such as `__init__`, which is called when a class
    instance is created
* instance methods, such as `bar`, which take and implicit reference `self`
    to the class instance.

The difference between class and instance variables is e.g. explained here:
https://careerkarma.com/blog/python-class-variables/

Classes generally provide us with a way to structure data and methods which
logically belong together, e.g. in the case of our LED blinker, the information
needed to connect to the LED (pass to `__init__` upon creation of the class),
as well as methods to interact with the LED and return its current state.

Classes furthermore allow for `inheritance`. Consider e.g. the following:

```python

class Toy:

    def __init__(self, name):
        self.name

    def info(self):
        print(f"I am {self.name}")

    def get_name(self):
        return self.name

class Ball(Toy):
    def __init__(self, name, radius):
        super().__init__(name)
        self.radius = radius

    def info(self):
        print(f"I am a {self.name} Ball")
        print(f"My radius is {self.radius}")

```

Here, we have defined a base class `Toy`, which upon instantiation takes
a `name` argument. It defines an `info` method to print information about
itself, and a `get_name` method to return the name.

The `Ball` class now inherits from `Toy` (simply by writing `class BalL(Toy)`).
This means `Ball` shares the methods and variables of the base class `Toy`.
It also means `Ball` is responsible for correctly constructing its `Toy` base,
as indicated here through the use of the `super()` method: `super()` refers to
the parent or base, and thus `super().__init__` says to call `__init__` on
`Toy`, not on `Ball`, which also defines it. If one doesn't use `super`
methods are resolved such that always the last definition is used. This is
e.g. the case for the `info` method:

```python
b = Ball("Big Ball", 42)
b.info()
```

will print

```
I am a Big Ball Ball
My radius is 42
```

as the last definition of `info` is the one in `Ball`, not the one in `Toy`.

For our concrete example of a LED `Blinker` deriving from a `Sensor` base
class, we make use of this fact, in that `Sensor` defines and interface
that e.g. in `main.py` we expect all sensors to follow: there's always to be
a `measure` and a `render` method to be provided by each concrete sensor. If
not it's a `NotImplementedError`. Also, each sensor requires a name.

Note that in principle we could do without that and just agree on that these
methods are implemented in each sensor. However, by explicitely defining
the expected interface in the base class we document our intent, and make it
much more obvious to future maintainers. Somebody adding a future sensor will
not need to go through all our code to see what methods might be called
on a `Sensor`, but can rather implement an interface as described by the
base class.