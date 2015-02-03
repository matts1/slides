from custom import ShellCode
from latexslides import BulletSlide

slides = [
    BulletSlide("Dictionaries", [
        "Dictionaries work like the books do. They are like a list, except each item in it points to another item. They are used to store associated data about something. It becomes very easy to find data associated with it.",
        "To create, change, or get a value in a dictionary, you use indexing.",
        ShellCode("""
phones = {'Matt': '1234 567 890', 'Bob': '9839 234 853'}
print(phones['Bob'])  # get Bob's phone number
phones['Greg'] = '4359 129 580'  # create Greg's phone number
phones['Matt'] = '9584 857 239'  # overwrite Matt's phone number
phones"""),
    "There can only be one value for each key, which is why it overwrote Matt's phone number"
    ])
]