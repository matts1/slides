from custom import ShellCode
from latexslides import Slide, BulletBlock

slides = [
    Slide("Functions", [
          BulletBlock([
              "Any function has up to 3 parts to it",
              [
                  "Input - these are often called 'arguments' or 'parameters'",
                  "Output - what is given back to the program",
                  "Side Effect - can be a variety of things, usually printing something out or asking for input"
              ],
              "For example, in maths, if we have the function $f(x) = 3x + 4$, the input is $x$ and the output is $3x + 4$",
              "All the type conversions done in the previous section were actually functions which take something as input and output that same thing but as a different data type",
              "Similarly, in the example below, the input is something that can be turned into an integer (in this case, the string '7'), and the output is an integer (in this case, the integer 7)"
          ]),
          ShellCode("int('7')")
    ]),

    Slide("Output", [
        r"The function for output is called print. It takes in any amount of arguments (seperate with commas) and outputs, perhaps unintuitively, \textbf{nothing}. However, it does have the side effect of displaying something on the screen - your arguments, space seperated.",
        ShellCode("print('Hello World!')\nprint(print('Hello', 'World!'))"),
        "This is proof that the print statement doesn't output anything. With order of operations, the inside print statements go first, writing 'Hello World!' to the screen. Then the outside print statement evaluates, printing the output of the inside ones to the screen, which is None (don't worry if you don't understand this)",
    ]),

    Slide("Input", [
        "The function for input is, surprise surprise, 'input'. It takes an input of a prompt, and then has a side effect of asking the user for input with that prompt. Its output is whatever you type as a string",
        ShellCode("number = input('Enter a number: ')\nprint(number, type(number))", data="5\n"),
        "In the example above, we enter in a number, but the value is a string. If we want to use it as a number, we need to use the int function."
    ]),

    Slide("Help", [
        "The help function often comes in handy. It displays information about a function. For example:",
        ShellCode("help(print)")
    ]),

    Slide("Optional arguments", [
        "In the previous slide we saw optional arguments. These arguments are arguments with a default value. For example, the default value for sep (the seperator) in print statements is ' ' (a space). We can override this by specifically telling it what it should be",
        ShellCode("print('foo', 'bar', sep=',')"),
        "Similarly, the prompt for input is an optional argument",
        ShellCode("input() # first line prompt / input, second line output. It defaults to no prompt", data='abc')
    ]),

    Slide("Stacking functions", [
        "Python is like maths. You can stack lots of things together, as long as it makes sense. For example, if I was to make a program which asked the user for a number, and multiplied it by 5, I could do this",
        ShellCode("print(int(input('Enter a number: ')) * 5)", data='3'),
        "Or an easier way to comprehend it is to slowly replace things with their values in your head, just like with order of operations",
        ShellCode("""
print(int('3') * 5) # input is '3'
print(3 * 5) # int('3') is 3
print(15) # 3 * 5 = 15"""),
    ])
]