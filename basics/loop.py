from custom import ShellCode, Code
from latexslides import BulletSlide

slides = [
    BulletSlide("While Loops", [
        "While loops are very similar to if statements. The only difference is at the end, if the condition is still true, they come back to the start",
        "There are generally 4 parts to any while loop. You initiate the variable so you can use it, then run a check, do whatever it is you want to do, then do some sort of increment",
        ShellCode("i = 0 # initiation\nwhile i < 3: # condition\n        print(i) # operation\n        i += 1 # increment")
    ]),

    BulletSlide("For loops", [
        ShellCode("iterable = 'abc'\nfor item in iterable:\n        print(item)"),
        "An iterable is a list-like object that you can go through a single part at a time",
        "Try the example above, setting it to various data types",
        "A for loop goes through everything inside it, then goes back to the start, each time setting item to the next item in the iterable",
        "For loops are slightly less powerful than while loops, but they are generally far more concise than while loops. The previous slide's while loop can simply be wrote as follows",
        Code("for i in range(3):\n        print(i)")
    ]),

    BulletSlide("Common problems with loops", [
        "Infinite loops - usually caused by forgetting to increment or having the wrong conditional in a while loop. Not really a problem with for loops",
        "Data resetting - for loops reset item to the next item in the iterable, even if you change item, as shown below",
        ShellCode("for i in range(3):\n        print(i)\n        i = 10")
    ]),

    BulletSlide("Special loop keywords", [
        "break - exits the loop",
        "continue - skips the rest of the inside of the loop and goes back to the start if it still meets the conditional"
    ])
]