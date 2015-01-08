from core import *
import os, sys, re

class DoconceSlides(Slides):
    """
    Class for creating a presentation using the Doconce markup language.

    Instances contain a number of slides, that may be arranged in sections and subsections.
    @ivar slides: Top-level slides that appear before the first section.
    @ivar sections: Eventual sections that the document is divided into, each section collects itself a number of slides
    and possibly also subsections.
    """

    def __init__(self, *args, **kwargs):
        Slides.__init__(self, *args, **kwargs)

        Code.latex_envir = 'doconce'

    # Document header
    def _header(self):
        self.buf.write("""\
# This Doconce file was automatically generated by the latexslides
# program (see http://code.google.com/p/latexslides).
""")

    # Custom substs
    def fix(self, text):
        text = text.replace('\\mathbfx{', '\\bm{')
        text = text.replace('\\begin{document}', '')
        text = text.replace('\\begin{end}', '')
        text = re.sub(r'!bpop\n+!bblock', r'!bpop\n!bblock', text)
        text = re.sub(r'!epop\n!bpop', r'!epop\n\n!bpop', text)
        text = re.sub(r'!bblock\n+', r'!bblock\n', text)
        text = re.sub(r'!bblock (.+)\n+', r'!bblock \g<1>\n', text)
        text = re.sub(r'!bblock\n+!bc', r'!bblock\n!bc', text)
        text = re.sub(r'\n+!eblock', r'\n!eblock', text)
        text = re.sub(r'!eblock\n+!split', r'!eblock\n\n!split', text)
        text = re.sub(r'!epop\n+!split', r'!epop\n\n!split', text)
        #text = re.sub(r'!bpop\n+!epop', '', text)
        text = re.sub(r'===\n(!b.+)', r'===\n\n\g<1>', text)
        text = re.sub(r'\n+(^FIGURE:.+)\n+', r'\n\n\g<1>\n\n', text,
                      flags=re.MULTILINE)
        text = re.sub(r'\\emph\{(.+?)\}', '*\g<1>*', text,
                      flags=re.DOTALL)
        text = re.sub(r'\\emp\{(.+?)\}', '`\g<1>`', text,
                      flags=re.DOTALL)
        text = re.sub(r'\\code\{(.+?)\}', '`\g<1>`', text,
                      flags=re.DOTALL)
        text = text.replace('\\\\', '<linebreak>')
        text = text.replace(' -- ', ' - ')

        return text

    # Title page
    def _titlepage(self):
        self.buf.write(r"""

TITLE: %s
AUTHOR: %s at %s
DATE: %s
""" % (self.title, self.author_cmd, self.institute_cmd, self.date))

        if self.titlepage_figure:
            self.buf.write(r"""
FIGURE: [%s, width=400 frac=%s]
""" % (titlepage_figure, self.titlepage_figure_fraction_width))
        self._ltx = self.buf.getvalue()

    def _renderSlide(self, slide):
        # Do not ignore hidden slides, dump all
        if isinstance(slide, RawSlide):
            c = slide.content[0]
            self.renderContent[type(c)](c)
            return

        self.buf.write(r"""

!split
===== %s =====
""" % (slide.title))

        def write_text(row, column, cells=True, width=1):
            if cells:
                text = """
!slidecell %d%d  %s
%%s
!eslidecell
""" % (row, column, width)
            else:
                text = '\n%s\n'
            return text

        def write_figure(row, start_column=0, cells=True, width=1):
            for i, slide_text in enumerate(slide._fig):
                m = re.search(r'\\centerline{\\includegraphics\[width=(.+?)\\linewidth.+?\]\{(.+?)\}', slide_text)
                if m:
                    filename = m.group(2).strip()
                    figwidth = float(m.group(1))
                if cells:
                    text = r"""
!bslidecell %d%d  %s

FIGURE: [%s, width=%d frac=%.1f]

!eslidecell

""" %(row, start_column + i, width, filename, int(figwidth*600), figwidth)
                else:
                    text = r"""
FIGURE: [%s, width=%d frac=%.1f]

""" %(filename, int(figwidth*600), figwidth)
            return text

        # Here is the slide text
        if slide._dim:
            self._dim = slide._dim
        buf = self.buf
        from cStringIO import StringIO
        self.buf = StringIO()  # need new buffer for this slide
        for c in slide.content[:-1]:
            if slide._dim == 'blocks':
                self.buf.write("!bpop\n")
            self.renderContent[type(c)](c)
            if slide._dim == 'blocks':
                self.buf.write("!epop\n")
        for c in slide.content[-1:]:
            if slide._dim == 'blocks':
                self._dim = False
                self.buf.write("!bpop\n")
                self.renderContent[type(c)](c)
                self.buf.write("!epop\n")
            else:
                self.renderContent[type(c)](c)
        self._dim = False
        slide_text = self.buf.getvalue()
        self.buf = buf

        # If figure is to the north:
        # If figure is to the north:
        # Use cells for figure, but not for text
        if slide._fig and slide._fig_pos == 'n':
            self.buf.write(
                write_figure(row=0, start_column=0, cells=len(slide._fig) > 1,
                             width=1/len(slide._fig)))
            self.buf.write(
                write_text(row=1, column=0, cells=False,
                           width=1) % slide_text)

        # If figure is to the south:
        # Use cells for figure, but not for text
        elif slide._fig and slide._fig_pos == 's':
            self.buf.write(
                write_text(row=0, column=0, cells=False,
                           width=1) % slide_text)
            self.buf.write(
                write_figure(row=1, start_column=0, cells=len(slide._fig) > 1,
                             width=1/len(slide._fig)))

        # If figure is to the west:
        elif slide._fig and slide._fig_pos == 'w':
            self.buf.write(
                write_fig(row=0, start_column=0, cells=True,
                          width=slide._left_column_width))
            self.buf.write(
                write_text(row=1, column=len(slide._fig)+1, cells=True,
                           width=1-slide._left_column_width) % slide_text)

        # If figure is to the east:
        elif slide._fig and slide._fig_pos == 'e':
            self.buf.write(
                write_text(row=1, column=0, cells=True,
                           width=1-slide._right_column_width) % slide_text)
            self.buf.write(
                write_fig(row=0, start_column=1, cells=True,
                          width=slide._right_column_width))
        else:
            # No figures
            self.buf.write(slide_text)


        self._dim = False

    def _renderSection(self, section):
        self.buf.write("\n")
        self.buf.write(r"""======= %s =======
"""% (section._title))
        # Top-level slides
        for s in section.slides:
            self.buf.write("\n")
            self._renderSlide(s)
        # Nested slides
        for s in section.subsections:
            self.buf.write("\n")
            self._renderSubsection(s)

    def _renderSubsection(self, subsection):
        self.buf.write(r"""===== %s =====
""" % (subsection._title))
        for s in subsection.slides:
            self.buf.write("\n")
            self._renderSlide(s)

    def _renderBulletList(self, bulletlist):
        if self._dim == True or self._dim =='progressive':
            self.buf.write('!bpop\n')

        indent = 2
        for b in bulletlist.bullets:
            if isinstance(b, (list)):
                indent += 2
                for bi in b:
                    self.buf.write(' '*indent + '* ')
                    if isinstance(bi, basestring):
                        bi = Text(bi)
                    self.renderContent[type(bi)](bi)
                indent -= 2
            elif isinstance(b, BulletList):
                pass
                # Nested list
            else:
                self.buf.write(' '*indent + '* ')
                if isinstance(b, basestring):
                    b = Text(b)
                self.renderContent[type(b)](b)
        if bulletlist.bullets:
            self.buf.write('\n')

    def _renderBlock(self, block):
        if Block.unblock:
            if block.heading:
                self.buf.write(r"""_%s_

""" % block.heading)
        else:
            if block.heading:
                block.heading = " %s" % block.heading
            self.buf.write(r"""
!bblock%s

""" % block.heading)

        for c in block.content:
            if isinstance(c, basestring):
                c = Text(c)
            self.renderContent[type(c)](c)

        if Block.unblock:
            pass
        else:
            self.buf.write(r"""
!eblock
""")

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
