from core import *
import os, sys

class BeamerSlides(Slides):
    """ 
    Class for creating a presentation using the Beamer LaTeX package.

    Instances contain a number of slides, that may be arranged in sections and subsections.
    @ivar slides: Top-level slides that appear before the first section.
    @ivar sections: Eventual sections that the document is divided into, each section collects itself a number of slides
    and possibly also subsections.
    """

    def __init__(self, *args, **kwargs):
        Slides.__init__(self, *args, **kwargs)
        
    # Document header
    def _header(self):
        message = """\
%%
%% This latex prosper file was automatically generated from running the program
%%     %s
%% by latexslides (available from  googlecode.com).
%% Do not update this latex file - instead edit %s
%%

""" % (sys.argv[0], sys.argv[0])

        if not self.colour:
            self.beamer_colour_theme = 'seahorse'
        if not self.colour or self.handout or self.html:
            self.buf.write(r"""%s\documentclass[handout,xcolor=dvipsnames,aspectratio=169]{beamer}
""" % message)
        else:
            self.buf.write(r"""%s\documentclass[xcolor=dvipsnames,aspectratio=169]{beamer}
""" % message)

        self.buf.write(r"""
\usetheme{%s}

\usepackage{ptex2tex}
%% #ifdef MINTED
\usepackage{minted}  %% required pygments and latex -shell-escape filename
%% #endif
\usepackage{pgf,pgfarrows,pgfnodes,pgfautomata,pgfheaps,pgfshade}
\usepackage{graphicx}
\usepackage{epsfig}
\usepackage{fancyvrb,moreverb,relsize}
\usepackage{amsmath,amssymb}
\usepackage[latin1]{inputenc}
\usepackage{colortbl}
\usepackage[english]{babel}
%s
""" % (self.beamer_theme, self.latexpackages))
        if self.beamer_colour_theme == 'seahorse' and self.beamer_theme == 'simula':
            print """***warning:
   the theme 'simula' and the colour theme 'seahorse'
   do not go well together"""

    # Title page
    def _titlepage(self):
        if not self.titlepage:
            # Just dump the important information, then exit
            self.buf.write(r"""
\title%s{%s}

\author%s{%s}

\institute{%s}

\date{%s}
""" % (self.short_title, self.title, self.short_author, self.author_cmd, self.institute_cmd,
       self.date))
            self._ltx = self.buf.getvalue()
            return 0

        else:
            titlepage = r"\titlepage"

        option = ""
        if not self.header_footer:
            option = "[plain]"

        if True:    # self.toc_heading: # we always want section tocs, but
                    # toc_heading='' removes the initial toc (fine for
                    # using MappingSlide instead, and still get section tocs)
            toc_slides = r"""%% Delete this, if you do not want the table of contents to pop up at
%% the beginning of each section:
\AtBeginSection[]
{
    \begin{frame}<beamer>{%s}
    \tableofcontents[currentsection]
    \end{frame}
}
""" % self.toc_heading
        else:
            toc_slides = ''

        # Title page figure
        if not self.titlepage_figure:
            tp_fig = r"""
\title%s{%s}

\author%s{%s}

\institute{%s}

\date{%s}

%s

%% If you wish to uncover everything in a step-wise fashion, uncomment
%% the following command:

%%\beamerdefaultoverlayspecification{<+->}

\begin{frame}%s
%s
\end{frame}
""" % (self.short_title, self.title, self.short_author,
       self.author_cmd, self.institute_cmd,
       self.date, toc_slides, option, titlepage)

        else:
            # Figure to the right or below?
            if self.titlepage_figure_pos == 's':
                # Figure below title data:
                tp_fig = r"""
\title%s{%s}

\author%s{%s}

\institute{%s}

\date{%s \\ \ \\
\centerline{\psfig{figure=%s,width=%.1f\linewidth}}
}

%s

%% If you wish to uncover everything in a step-wise fashion, uncomment
%% the following command:

%%\beamerdefaultoverlayspecification{<+->}

\begin{frame}%s
%s
\end{frame}
""" % (self.short_title, self.title, self.short_author,
       self.author_cmd, self.institute_cmd,
       self.date, self.titlepage_figure, self.titlepage_figure_fraction_width,
       toc_slides, option, titlepage)

            else:
                # Two column titlepage:
                tp_fig = r"""
\title%s{%s}

\author%s{%s}

\institute{%s}

\date{%s}

%s

%% If you wish to uncover everything in a step-wise fashion, uncomment
%% the following command:

%%\beamerdefaultoverlayspecification{<+->}

\begin{frame}[plain]

\begin{columns}

\column{%.1f\textwidth}
%s
\column{%.1f\textwidth}

\mbox{}\vspace*{10mm}
\centerline{\psfig{figure=%s,width=%.1f\linewidth}}

\end{columns}

\end{frame}
""" % (self.short_title, self.title, self.short_author,
       self.author_cmd, self.institute_cmd,
       self.date, toc_slides, self.titlepage_left_column_width, titlepage,
       1.0 - self.titlepage_left_column_width, self.titlepage_figure,
       self.titlepage_figure_fraction_width)

        if self.beamer_theme == 'simula' or self.beamer_theme == 'cbc':  # hack!
            tp_fig += '\n\n' + r'\turnoffBackground' + '\n\n'

        self.buf.write(tp_fig) # Dump titlepage

        if self.toc_heading:
            if isinstance(self.toc_figure, basestring) and self.toc_figure:
                fig = r'\psfig{figure=%s,width=%s\linewidth}' % \
                      (self.toc_figure, self.toc_figure_fraction_width)
                self.buf.write(r"""
%% table of contents:
\begin{frame}[plain]
\frametitle{%s}

\begin{columns}

\column{%g\textwidth}
\tableofcontents
%%\tableofcontents[pausesections]

\column{%g\textwidth}
\begin{center}
%s
\end{center}

\end{columns}
\end{frame}
""" % (self.toc_heading, self.toc_left_column_width, 1.0 - self.toc_left_column_width, fig)
        )
#             else: # plain toc, no figure
#                 self.buf.write(r"""
# %% table of contents:
# \begin{frame}[plain]
# \frametitle{%s}
# \tableofcontents
# %%\tableofcontents[pausesections]
# \end{frame}
# """ % self.toc_heading)
        self._ltx = self.buf.getvalue()


    def _renderSlide(self, slide):
        if slide.hidden:
            return

        if isinstance(slide, RawSlide):
            c = slide.content[0]
            self.renderContent[type(c)](c)
            return

        options = []
        if not self.header_footer:
            options.append("plain")

        for c in slide.content:
            if not slide._fragile and c.containsVerbatim:
                slide._fragile = True
            
        if slide._fragile:
            options.append("fragile")
        if options:  # Any options must be enclosed in brackets
            options = '[%s]' % ",".join(options)
        else:
            options = ""

        self.buf.write(r"""

\begin{frame}%s
\frametitle{%s}

""" % (options, slide.title))

        # If figure is to the north:
        if slide._fig and slide._fig_pos == 'n':
            width = 1./len(slide._fig)
            self.buf.write(r"""
\begin{columns}
""" )
            for i in slide._fig:
                self.buf.write(r"""
\column{%g\textwidth}
%s
""" %(width, i))
            self.buf.write(r"""
\end{columns}
""")

        # If figure is to the west:
        if slide._fig and slide._fig_pos == 'w':
            self.buf.write(r"""
\begin{columns}
\column{%g\textwidth}
""" %(slide._left_column_width))
            for i in slide._fig:
                self.buf.write(r"""
%s
""" %(i))
            self.buf.write(r"""
\column{%g\textwidth}
""" %(slide._right_column_width))

        # If figure is to the east:
        if slide._fig and slide._fig_pos == 'e':
            self.buf.write(r"""
\begin{columns}
\column{%g\textwidth}
""" %(slide._left_column_width))

        if slide._dim:
            self._dim = slide._dim
            self._dimi = 2 # If 1, starts at first element
        # Remove next to lines to start at first block
        if slide._dim == 'blocks':
            self.buf.write(r"\pause" + "\n")
        for c in slide.content[:-1]:
            self.renderContent[type(c)](c)
        for c in slide.content[-1:]:
            if slide._dim == 'blocks':
                self._dim = False
                self.renderContent[type(c)](c)
            else:
                self.renderContent[type(c)](c)
        self._dim = False
        self._dimi = 0

        # If figure is to the east:
        if slide._fig and slide._fig_pos == 'e':
            self.buf.write(r"""
\column{%g\textwidth}
""" %(slide._right_column_width))
            for i in slide._fig:
                self.buf.write(r"""
%s
""" %(i))
            self.buf.write(r"""
\end{columns}
""")

        # If figure is to the west:
        if slide._fig and slide._fig_pos == 'w':
            self.buf.write(r"""
\end{columns}
""")

        # If figure is to the south:
        if slide._fig and slide._fig_pos == 's':
            width = 1./len(slide._fig)
            self.buf.write(r"""
\begin{columns}
""")
            for i in slide._fig:
                self.buf.write(r"""
\column{%g\textwidth}
%s
""" %(width, i))
            self.buf.write(r"""
\end{columns}
""")

        self.buf.write(r"""
\end{frame}
""")
        self._dim = False

    def _renderSection(self, section):
        self.buf.write("\n")
        self.buf.write(r"""\section%s{%s}
"""% (section._short_title, section._title))
        # Top-level slides
        for s in section.slides:
            self.buf.write("\n")
            self._renderSlide(s)
        # Nested slides
        for s in section.subsections:
            self.buf.write("\n")
            self._renderSubsection(s)

    def _renderSubsection(self, subsection):
        self.buf.write(r"""\subsection%s{%s}
""" % (subsection._short_title, subsection._title))
        for s in subsection.slides:
            self.buf.write("\n")
            self._renderSlide(s)

    def _renderBulletList(self, bulletlist):
        dims = ['' for i in range(len(bulletlist.bullets))]
        if isinstance(self._dim, (bool, int)) or self._dim =='progressive':
            if self._dim:
                dims = []
                for i in range(len(bulletlist.bullets)):
                    if isinstance(bulletlist.bullets[i], (list, tuple)) and bulletlist._dim:
                        self._dimi -= 1
                    dims.append('<%d->' % self._dimi)
                    if bulletlist._dim:
                        self._dimi += 1
                # Prevent from making next block progressive if
                # bulletlist.progressive is false
                if not bulletlist._dim:
                    self._dimi += 1

        elif isinstance(self._dim, (list, tuple)):
             pass

        if isinstance(self._dim, basestring):
            if self._dim =='single_then_all':
                dims = []
                step = self._dimi # Step to show all in one block
                length = 0 # Shorten list
                if not bulletlist._dim:
                    length -= len(bulletlist.bullets)
                    self._dimi += 1
                for i in bulletlist.bullets:
                    if isinstance(i, (list,tuple)) and bulletlist._dim:
                        length -= 1
                for i in bulletlist.bullets:
                    if not isinstance(i, (list,tuple)) and bulletlist._dim:
                        self._dimi += 1
                    dims.append('<%d,%d>' % (self._dimi-1, len(bulletlist.bullets)+length+step))
                self._dimi += 1

            elif self._dim == 'single':
                dims = []
                step = 0
                for i in range(len(bulletlist.bullets)):
                    if isinstance(bulletlist.bullets[i], (list,tuple)) and bulletlist._dim:
                        self._dimi -= 1
                    dims.append('<%d>' % (self._dimi))
                    if bulletlist._dim:
                        self._dimi += 1
                # Prevent from making next block progressive if
                # bulletlist.progressive is false
                if not bulletlist._dim:
                    self._dimi += 1

##             elif self._dim == 'blocks':
##                 dims = []
##                 for i in range(len(bulletlist.bullets)):
##                     dims.append('<%d->' %self._dimi)
##                 self._dimi += 1
             
        if bulletlist.bullets:
            self.buf.write(r'\begin{itemize}' + '\n')

        for b, d in zip(bulletlist.bullets, dims):
            if isinstance(b, (list)):
                self.buf.write(r'\begin{itemize}' + '\n')
                for bi in b:
                    self.buf.write(r'\item%s ' %d)
                    if isinstance(bi, basestring):
                        bi = Text(bi)
                    self.renderContent[type(bi)](bi)
                self.buf.write(r'\end{itemize}' + '\n')
            elif isinstance(b, BulletList):
                pass
                # Nested list
            else:
                self.buf.write(r"\item%s " %d)
                if isinstance(b, basestring):
                    b = Text(b)
                self.renderContent[type(b)](b)
        if bulletlist.bullets:
            self.buf.write(r"""\end{itemize}
""")

    def _renderBlock(self, block):
        if Block.unblock:
            if block.heading:
                self.buf.write(r"""{\bf %s

""" % block.heading)
        else:
            if block.heading:
                block.heading = "{%s}" % block.heading
            self.buf.write(r"""
\begin{block}%s

""" % block.heading)

        if isinstance(block, TableBlock):
            if block.center:
                self.buf.write(r"""\begin{center}""")

        for c in block.content:
            if isinstance(c, basestring):
                c = Text(c)
            self.renderContent[type(c)](c)

        if isinstance(block, TableBlock):
            if block.center:
                self.buf.write(r"""\end{center}""")

        if Block.unblock:
            pass
        else:
            self.buf.write(r"""
\end{block}
""")
        if self._dim == 'blocks':
            self.buf.write(r"\pause" + "\n")
            
    def _renderTextBlock(self, textblock):
        self._renderBlock(textblock)

    def _renderBulletBlock(self, bulletblock):
        self._renderBlock(bulletblock)
        
    def _renderCodeBlock(self, codeblock):
        self._renderBlock(codeblock)

    def _renderTableBlock(self, tableblock):
        self._renderBlock(tableblock)

    def write(self, filename):
        Slides.write(self, filename)
        basename, ext = os.path.splitext(filename)
        if basename[-2:] == '.p':
            basename = basename[:-2]
            ptex2tex_line = 'ptex2tex -DMINTED %s; ' % basename
        else:
            ptex2tex_line = ''
        # Check if latex or pdflatex, depending on figure extensions
        text = self.get_latex()
        import re
        pattern = 'includegraphics\[.+?\]\{(.+?)\}'
        figfiles = re.findall(pattern, text)
        figfiletypes = {}
        for fname in figfiles:
            ext = os.path.splitext(fname)[1]
            if not ext in figfiletypes:
                figfiletypes[ext] = 1
            else:
                figfiletypes[ext] += 1
        def check(illegal):
            # Check if other illegal image types are present
            for name in illegal:
                if name in figfiletypes:
                    return True

        if '.ps' in figfiletypes or '.eps' in figfiletypes:
            latex = 'latex -shell-escape'
            if check(['.jpg', '.jpeg', '.png']):
                print 'Cannot have jpeg/png files and ps/eps files mixed!'
                sys.exit(1)
        elif '.jpg' in figfiletypes or '.jpeg' in figfiletypes or \
                 '.png' in figfiletypes:
            latex = 'pdflatex -shell-escape'
            if check(['.eps', '.ps']):
                print 'Cannot have jpeg/png files and ps/eps files mixed!'
                sys.exit(1)
        else:
            # No figures
            latex = 'latex'

        print '%s%s %s;' % (ptex2tex_line, latex, basename),
        print 'dvipdf %s' % basename if latex == 'latex' else ''
