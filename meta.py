from latexslides import BulletSlide, Code

lessoninfo = BulletSlide("Lesson Information", [
    "You will need to attend most lessons in order to not fall behind",
    "I'm not getting paid to put up with your crap, so if you're disruptive I'll just kick you out",
    "Programming is a skill like any other, requiring lots of work to get better. Hence, you will need to work from home in order to keep up",
    "If you don't understand something, I want to know about it. My explanations aren't amazing",
    "Most lessons involve a lecture like part where I explain a new concept to everyone, then a practical part where people get to code",
])

whatis = BulletSlide("What you will be learning", [
    "Building up to the skills required to:",
    [
        "Write software",
        "Create websites (backend)",
        "Make games (extremely extremely simple ones)",
    ],
    "It will probably take a few years before you can do anything actually useful",
    "You want to learn one aspect completely before you start the next aspect"
])

whatisnt = BulletSlide("What these lessons aren't", [
    "Teaching you how to hack",
    "Teaching you how to make games with a GUI (graphical user interface)",
    "Teaching you frontend for websites (HTML / CSS)",
])

whypython = BulletSlide("Why Python",[
    "Python is concise, simple, and easy to learn",
    "It doesn't have some of the more complex things that other languages do such as fixed data types, variable declaration, etc.",
    "It has very broad uses. I have wrote websites, made tools, and created programming languages with python. I even made this slide show with python",
   "Python is a programming language. Programming Language $\neq$ Markup Language"
])

installpython = BulletSlide("Installing Python", [
    "Windows / Mac",
    [
        "Download and install the latest python 3 release from \url{http://www.python.org}",
        "This will install IDLE on your computer"
     ],
    "Linux",
    [
        "Python is preinstalled on both Mac and Linux for the terminal, but as a beginner, a GUI is recommended, so I would install IDLE with the following command for Ubuntu" + Code('sudo apt-get install idle3')
    ],
    "After getting a bit of experience, I would recommend switching IDEs to a more fully featured one. I recommend PyCharm"
])

section = [
   ("Lesson Structure", "Lessons",
       [lessoninfo, whatis, whatisnt]
   ),
    ("Python",
        [whypython, installpython]
    )
]