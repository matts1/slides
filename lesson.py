import sys
from latexslides.beamer import BeamerSlides
import meta, basics


slides = BeamerSlides(
    title="Learning Programming",
    short_title='Programming',
    author_and_inst=[("Matthew Stark",)],
    short_author="Matthew Stark",
    beamer_theme="Frankfurt",
    date=r"\today",

    # latexpackages just puts it at top, so any other top declarations here
    # http://tex.stackexchange.com/questions/2072/beamer-navigation-circles-without-subsections
    latexpackages=r"""
\usepackage{hyperref}
\usepackage{remreset}

\makeatletter
\@removefromreset{subsection}{section}
\makeatother
\setcounter{subsection}{1}""",
    handout='handout' in sys.argv
)


sections = [meta, basics]
for section in sections:
    slides.add_slides(section.section, generate_slides=True)

# Dump to file:
slides.write("compiled/lesson.p.tex")
