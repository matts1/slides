from custom import ShellCode, Code
from latexslides import Slide

slides = [
    Slide("Boolean Expression", [
        "Boolean expressions are simply something that is either True or False",
        ShellCode("1 > 2\n'foo' == \"foo\"\n'foo' != 'bar' # != means not equal\nbool(0)\nbool(1)"),
        "In conditions, if something is not a boolean, pretend it has bool(x) around it"
    ]),

    Slide("If", [
          "If statements allow you to choose whether to execute a block of code (indented section) based on some sort of condition. A simple example is a password on the computer. The syntax works like this.",
          Code("if <condition>: # the next line being indented is necessary\n    <do something>", latex_envir='minted'),
          ShellCode("""
if input("Enter the password: ") == "mypassword":
    print("Correct")
    print("You have been logged in")
          """, data="mypassword")
    ]),

    Slide("Else", [
        "Else allows you to execute a condition if none of the previous conditions were true",
        Code("""
if 1 == 2:
    print("Maths is broken")
else:
    print("Maths still works")
Maths still works
        """)
    ]),

    Slide("Elif", [
        r"Elif is a combination of else and if. Elif will execute if none of the previous conditions were executed \textbf{and} the condition in the elif is True",
        Code("""
marks = 72
if marks >= 85:  # isn't true, so goes to the next part
    print("High distinction")
elif marks >= 75:  # isn't true, so goes to next part
    print("Distinction")
elif marks >= 65:  # is true, so executes the inside and then doesn't look at the rest
    print("Credit")
elif marks >= 50:
    print("Pass")
else:
    print("Fail")
Credit
        """, latex_envir='minted')
    ]),
]