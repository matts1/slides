from custom import ShellCode
from latexslides import Slide, BulletSlide

slides = [
    BulletSlide("Lists", [
        "Lists allow you to store multiple pieces of data in a single variable",
        "Say you wanted to calculate the average height of a class of students, you could do something like this",
        ShellCode("""
heights = input('Enter the students\\' heights, space seperated: ').split()
heights
heights = list(map(int, heights))  # applies int to all items in heights
heights
print(sum(heights) / len(heights))  # average = total / amount of items
""", data="157 165 162")
    ]),

    BulletSlide("Useful functions on lists", [
        "list = str.split(seperator) splits string up by seperator, defaults to space",
        "list.append(item) adds item to end of list",
        "len(list) returns the amount of items in list",
        "list.remove(item) removes first instance of item from list",
        "item = list.pop(index) removes item at index, defaults to end",
        "list[index] returns item at index index",
        "list[start:stop:step] returns all items between start and stop, stepping by step",
        "list = sorted(list) returns the sorted version of the list",
        "list = map(function, list) returns the function applied to each item in the list",
    ]),

    BulletSlide("Tuples", [
        "Tuples are like lists, but cannot be modified. You cannot add to them (list.append), remove from them (list.pop or list.remove), or change items in them (list[x] = y)",
        "Instead of using [] to define a list, we use () to define a tuple. You can also use the tuple function, just like the list function",
        "It is rare you will need to use tuples until you get to more advanced levels",
        ShellCode("list(range(3))\ntuple(range(3))")
    ])
]