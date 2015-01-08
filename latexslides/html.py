from beamer import *
import os

class HTMLSlides(BeamerSlides):
    """ Class for dumping slides to HTML using the tex4ht package. Uses Beamer.

    Instances contain a number of slides, that may be arranged in sections and subsections.
    @ivar slides: Top-level slides that appear before the first section.
    @ivar sections: Eventual sections that the document is divided into, each section collects itself a number of slides
    and possibly also subsections.
    """

    def __init__(self, *args, **kwargs):
        kwargs['html'] = True
        kwargs['toc_heading'] = ''
        BeamerSlides.__init__(self, *args, **kwargs)

    def get_latex(self):
        slides = self.slides[:]
        self.slides = []
        for s in slides:
            if not isinstance(s, (Section, SubSection)):
                self.add_slide(s)
        return Slides.get_latex(self)

    def write(self, filename):
        Slides.write(self, filename)
        filename = os.path.splitext(filename)[0]
        print 'latex %s.tex; latex %s.tex; latex %s.tex;' %(filename, filename, filename),
        print 'tex4ht %s.4tc; t4ht %s.4ct' %(filename, filename)
