#!/usr/bin/env python

from latexslides import *
import latexslides

# Usage: import oldlatexslides as LaTeXSlides

import re, os, sys

#newcommands = r"""
#\newcommand{\emp}[1]{{\smaller\texttt{#1}}}
#\newcommand{\mathbfx}[1]{{\mbox{\boldmath $#1$}}}
#"""

newcommands = ""
latexpackages = ''
slidepackage = 'beamer'   # or 'prosper'

# global variables governing styles, fonts, etc.:
verbatimsize = r'\footnotesize'
# best choice for font size compatibility with beamer:
prosperstyle = 'hplplainsmall'
beamertheme = 'simula'
beamercolor = 'default'
header_footer = True
slidesobj = None

class LaTeXSlides(object):
    """Wrapper class for converting old LaTeXSlides objects to new ones.
       usage: import oldlatexslides as LaTeXSlides in old code."""
    def __init__(self, filename=None):
        self.slides = None
        
    def fileheader(self, *args):
        """Checks commandline arguments for the black and white keyword bw."""
        self.bw = False
        if '--bw' in sys.argv:
            self.bw = True

    def titlepage(self,
                  title='',
                  author_and_inst=[('author1','institution1'),
                                   ('author2','institution2',
                                    'institution3')],
                  date='',
                  titlepage_figure='',
                  titlepage_fraction_width=1.0,
                  titlepage_left_column_width=0.5,
                  titlepage_figure_pos='s',
                  short_title='',
                  short_author='',
                  toc_heading='',
                  toc_figure='',
                  toc_figure_fraction_width=1.0,
                  toc_left_column_width=0.5,
                  copyright_text='',
                  left_column_width=0.5
                  ):
        """Create the main slide object. All the information needed is in the
           arguments of the old function titlepage."""
        if slidepackage == 'beamer':
            self.slides = BeamerSlides(title=title,
                                       author_and_inst=author_and_inst,
                                       date=date,
                                       titlepage_figure=titlepage_figure,
                                       titlepage_left_column_width=titlepage_left_column_width,
                                       titlepage_figure_pos=titlepage_figure_pos,
                                       short_title=short_title,
                                       short_author=short_author,
                                       toc_heading=toc_heading,
                                       toc_figure=toc_figure,
                                       toc_figure_fraction_width=toc_figure_fraction_width,
                                       toc_left_column_width=toc_left_column_width,
                                       copyright_text=copyright_text,
                                       colour=not self.bw,
                                       newcommands=(newcommands),
                                       beamer_theme=beamertheme,
                                       beamer_colour_theme=beamercolor,
                                       header_footer=header_footer,
                                       latexpackages=latexpackages)
        elif slidepackage == 'prosper':
            self.slides = ProsperSlides(title=title,
                                        author_and_inst=author_and_inst,
                                        date=date,
                                        titlepage_figure=titlepage_figure,
                                        titlepage_left_column_width=titlepage_left_column_width,
                                        titlepage_figure_pos=titlepage_figure_pos,
                                        short_title=short_title,
                                        short_author=short_author,
                                        toc_heading=toc_heading,
                                        toc_figure=toc_figure,
                                        toc_figure_fraction_width=toc_figure_fraction_width,
                                        toc_left_column_width=toc_left_column_width,
                                        copyright_text=copyright_text,
                                        colour=not self.bw,
                                        newcommands=(newcommands),
                                        prosper_style=prosperstyle,
                                        header_footer=header_footer,
                                        latexpackages=latexpackages)
        else:
            print 'slidepackage unknown:', slidepackage
            sys.exit(1)
        # set slides object global
        global slidesobj
        slidesobj = self.slides
            
    def section(self, title='', short_title=''):
        return Section(title=title, short_title=short_title)
    def subsection(self, title='', short_title=''):
        return SubSection(title=title, short_title=short_title)

    def bulletslide(self,
                    title='Here goes the title of the slide',
                    bullets=[],  # list of bullet points
                    dim=False,   # dimming of bullet points
                    intro='',
                    outro='',
                    figure=None, # filename(s) with figure(s)
                    figure_pos='s',  # north, east, south, west
                    figure_fraction_width=1.0,
                    figure_angle=0, # indicates rotation (90, 270)
                    bullet_block=True,
                    bullet_block_heading='',
                    intro_block = True,
                    intro_block_heading = '',
                    outro_block = True,
                    outro_block_heading = '',
                    left_column_width=0.5,
                    header_footer=None,
                    hide=False,
                    ):
        """Adds a new bulletslide. intro- and outro-blocks are converted to
           regular TextBlocks.
        """
        content = []
        if intro:
            if intro_block:
                if intro_block_heading:
                    intro = TextBlock(intro, heading=intro_block_heading)
                else:
                    intro = TextBlock(intro)
            else:
                intro = Text(intro)
            content.append(intro)
        if bullets:
            bulletblock = BulletBlock(bullets, heading=bullet_block_heading)
            content.append(bulletblock)
        if outro:
            if outro_block:
                if outro_block_heading:
                    outro = TextBlock(outro, heading=outro)
                else:
                    outro = TextBlock(outro)
            else:
                outro = TextBlock(outro)
            content.append(outro)
        return latexslides.Slide(title=title, content=content, dim=dim,
                                 figure=figure, figure_pos=figure_pos,
                                 figure_size=figure_fraction_width,
                                 figure_angle=figure_angle,
                                 left_column_width=left_column_width,
                                 hidden=hide)
        
    def filefooter(self):
        """Not necessary in new implematation, kept for ease."""
        pass

class Slide(object):
    """Class for dumping buffer content to file. Class is used for minimal
       change of the old code."""
    
    def all2file(filename='', slides=None):
        """Static method for dumping buffer content to file. slide keyword is
           not used, but rather the global slide object."""
        if not filename:
            filename, suffix = os.path.splitext(sys.argv[0])
            filename += '.tex'
        ofile = file(filename, 'w')
        for slide in slides:
            slidesobj.add_slide(slide)
        ofile.write(slidesobj.get_latex())
        ofile.close()
    all2file = staticmethod(all2file)
