from latexslides import BulletSlide, Code

whatis = BulletSlide("What you will be learning", [
    "Building up to the skills required to:",
    [
        "Write software",
        "Create websites",
        "Make games",
    ],
    "Programming is a skill that takes time to learn. You can become decent in a few weeks, but to become very good takes a long time",
])

installpython = BulletSlide("Installing Python on your home computers", [
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
   ("Lesson Information", "Info",
       [whatis, installpython]
   ),
]