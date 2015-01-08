from latexslides import Slide, BulletSlide
from custom import ShellCode

slides = [
    Slide("Data Types", [
        "There are 4 common simple data types that you will be dealing with. Also note that anything that comes after the '\#' is a 'comment' so will be ignored and coloured in red",
        ShellCode("""
"Hello World!" # string (str), a bunch of characters surrounded by quotes
5 # integer (int), number with no decimal places
5.5 # floating point number (float), number with decimal places
5.0 # also a floating point number, despite there being no decimal places
False # a boolean (bool), equivalent to 0, either true or false
True # equivalent to 1
""")
    ]),

    Slide("Maths", [
        "One of the things python is great at is maths. It can do pretty much any operation that you can think of that makes sense",
        ShellCode("""
3 - 2 # int + int = int, int - int = int
1 + 1.0 # int + float = float, even if there is nothing after the decimal point
5 / 2 # int / int = float, even if it goes evenly, like below
4 / 2
"abc" + "def" # str + str joins 2 strings
"abc" * 3 # str * int produces repetitions
"12" * 5 # python doesn't know that "12" is actually an integer
""")
    ]),

    Slide("Variables", [
        "Python can even do algebra (sort of). We can store any data type under a 'variable'",
        ShellCode("""
a = 5
b = 3 + 1
c = a * b
c
d = 5 + c * 4  # order of operations is done correctly, as 5 + (20 * 4)
d
a = "abc" # we just overwrote a
a * b # it just multiplies the contents of variables together
""")
    ]),

    Slide("Type conversion", [
        "Since sometimes we do have things like the string '12' which we want to treat like an integer, you need to know type conversion",
        ShellCode("""
a = '12'
a, int(a), float(a), str(a), bool(a) # to convert, <datatype>(whatever)
b = 5
a * b
(int(a) * b - 7) / 4 # we can do as many things as we want on one line
int(a * b) # remember your order of operations - brackets resolve first
""")
    ]),

    BulletSlide("Practical Ideas", [
        "Python does all the operations that seem reasonable. Try doing something that doesn't make sense. For example, \"abc\" - 5.",
        "Next we will move on to input and output. Once you know that you can make whole programs, rather than entering your code line by line."
    ]),
]