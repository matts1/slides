"""
Module for writing presentations in Python.

A presentation is represented by an instance of the class L{Slides}. Such an instance consists of a set of slides,
which can be divided into a set of sections (which can themselves be divided into subsections). A slide is constructed
from primitives, instances of class L{Content}. A special type of Content is the L{Block} class, which encapsulates other
content in a certain area. The area is painted in a certain colour and can also be equipped with a heading.

Primitive content is represented by different subclasses of class Content. There are classes for text, bullet lists,
figures and computer code.
"""
__all__ = ["BulletSlide", "Slide", "TextSlide", "TableSlide", "RawSlide",
           "MappingSlide", "Block", "Content", "TextBlock", "CodeBlock",
           "BulletBlock", "TableBlock", "Text", "Table", "BulletList",
           "Code", "generate", "Section", "SubSection", "Slides"]

import re, os, sys
from cStringIO import StringIO

def _latextable(table,
                column_headline_pos='c',
                column_pos='c',
                ):
    ncolumns = len(table[0])
    if len(column_pos) == 1:
        column_pos = column_pos*ncolumns
    if len(column_headline_pos) == 1:
        column_headline_pos = column_headline_pos*ncolumns
    if not len(column_headline_pos) == len(column_pos):
        raise IndexError, 'Mismatch between column header and column'

    s = r"""
\begin{tabular}{%s}
\hline\noalign{\smallskip}
""" % column_pos
    # Special construction of the headline:
    s += ' &\n'.join([r'\multicolumn{1}{%s}{%s}' % (pos, text) \
                      for pos, text in zip(column_headline_pos, table[0])])
    s += r'\\ ' + '\n'
    s += r'\noalign{\smallskip}' + '\n' + r'\hline' + '\n' + \
         r'\noalign{\smallskip}' + '\n'
    for row in table[1:]:
        s += '\t & \t'.join([str(entry) for entry in row]) + r' \\ ' + '\n'
    s += r'\hline' + '\n' + r'\end{tabular}' + '\n'
    return s

def generate(filename="tmp.py"):
    filebase, filext = os.path.splitext(filename)
    filecontent="""#!/usr/bin/env python
# -*- coding: latin-1 -*-

from latexslides import *

# Set institutions
inst1, inst2 = "inst1", "inst2"

# Set authors
authors = [("author1", inst1), ("author2", inst1, inst2),]

# Create slides, exchange 'Beamer' with 'Prosper' for Prosper
slides = BeamerSlides(title="presentationtitle",
                      author_and_inst=authors,
                      )

sec1 = Section("section1")

slide1 = Slide("slidetitle", content=[Text("text"), Code("code")])

sub1 = SubSection("subsection1")

slide2 = BulletSlide("slidetitle",
                     ["bullet1",
                      ["subbullet1", "subbullet2"],
                      "bullet2",],
                     block_heading="heading",)

collection = [sec1, slide1, sub1, slide2]
for c in collection:
    slides.add_slide(c)

# Dump to file:
slides.write("%s.tex")
""" % filebase
    ofile = open(filename, 'w')
    ofile.write(filecontent)
    ofile.close()

class Content(object):
    """Basic primitive that can be rendered into LaTeX code."""
    fig_scale = 1.0
    font_scale = False
    def __init__(self, latex_code, dim=True):
        # Used to be latex_code.strip()
        self._ltx = latex_code
        self._dim = dim
        self._verbatim = False
        for p in _verbatim_phrases():
            if self._ltx.find(p) != -1:
                self._verbatim = True
                break

    def checkVerbatim(self, bullets):
        self._verbatim = _verbatim_text(bullets)

    def render(self, buffer):
        """ Render to buffer.

        LaTeX code will be written to the buffer that starts
        and ends without whitespace except for a linebreak at the end.
        """
        buffer.write(self._ltx)
        buffer.write("\n")

    @property
    def containsVerbatim(self):
        return self._verbatim

class Text(Content):
    def __init__(self, text):
        if not isinstance(text, basestring):
            text = str(text)
        #text = ' '.join(text.splitlines())
        Content.__init__(self, text)

class BulletList(Content):
    def __init__(self, bullets, dim=True):
        self.bullets = bullets
        self._dim = dim
        Content.checkVerbatim(self, bullets)

class Raw(Content):
    def __init__(self, text):
        Content.__init__(self, text)

def verbatimCode(code, file, from_regex, to_regex,
                 leftmargin, fontsize, ptex2tex_envir,
                 latex_envir):
    if file is not None:
        # Read code from file
        f = open(file, 'r')
        lines = []
        if from_regex is not None and to_regex is not None:
            copy = False
            for line in f:
                if re.search(from_regex, line):
                    copy = True
                if re.search(to_regex, line):
                    copy = False
                    # Do not include the to_regex line
                if copy:
                    lines.append(line)
        else:
            # Use the whole file:
            lines = f.readlines()
        code = ''.join(lines)
        code = code.strip()  # remove blank lines at the file top and bottom
        f.close()

    # Note: we don't use code.strip() because when specifying Code("""...
    # the user must be able to put in blank lines at the top and bottom
    # if that fits the text better. This doesn't make sense if the code
    # block is read from file.

    lines = [line for line in code.splitlines()]
    #lines = [line for line in code.splitlines() if line]

    #code = '\n'.join(lines)

    #import pprint
    #pprint.pprint(lines)

    # Check if ptex2tex environments are present
    ptex2tex = False
    envir = None
    end = None
    # First non-empty line *must* contain a begin envir
    line_no = 0
    while lines[line_no].strip() == '':
        line_no += 1
    if lines[line_no].startswith(r'\b') and \
           not lines[line_no].startswith(r'\begin{'):
        # Assume ptex2tex begin envir
        envir = line[2:]
        #print 'Found begin %s at line' % envir, line_no
        if ptex2tex_envir is not None:
            code = code.replace(r'\b%s' % envir, r'\b%s' % ptex2tex_envir)

        # Find the final end closing tag, searching backwards from the end
        line_no = len(lines)-1
        while lines[line_no].strip() == '':
            line_no -= 1
        if not lines[line_no].startswith(r'\e'):
            print 'No end match for begin of ptex2tex envir "%s"\n%s' % (envir, code)
            sys.exit(1)
        else:
            #print 'Found end %s at line' % envir, line_no
            if ptex2tex_envir is not None:
                code = code.replace(r'\e%s' % envir, r'\e%s' % ptex2tex_envir)

    #if envir:
    #    print 'Code after detection of envir %s' % envir
    #    print code

    if not envir:  # no explicit ptex2tex environments
        if ptex2tex_envir is None:
            # Use latex envir
            if latex_envir == 'Verbatim':
                code = r"""
\begin{Verbatim}[fontsize=%s,tabsize=4,baselinestretch=0.85,fontfamily=tt,xleftmargin=%s]
%s
\end{Verbatim}
""" % (fontsize, leftmargin, code)
            elif latex_envir == 'minted':
                code = r"""
\begin{minted}[fontsize=%s,tabsize=4,linenos=false,mathescape,baselinestretch=0.98,fontfamily=tt,xleftmargin=%s]{python}
%s
\end{minted}
""" % (fontsize, leftmargin, code)
            elif latex_envir == 'doconce':
                if '>>>' in code:
                    tp = 'pyshell'
                elif 'In [' in code:
                    tp = 'ipy'
                elif 'Terminal>' in code or 'Unix>' in code or 'Unix/DOS>' in code:
                    tp = 'sys'
                else:
                    tp =' pycod'
                code = r"""

!bc %s
%s
!ec
""" % (tp, code.rstrip())
            else:
                print 'Wrong latex_envir="%s" (must be Verbatim or minted)\nCode object:\n%s' % (latex_envir, code)
                sys.exit(1)
            #add """\noindent """

        else:
            # Use ptex2tex environment
            if code[0] != '\n':       # make sure there is a \n before \b...
                code = '\n' + code
            if code[-1] != '\n':
                code = code + '\n'    # make sure there is a \n before \e...

            code = '\n' + r'\b%s' % ptex2tex_envir + code + r'\e%s' % ptex2tex_envir + '\n'

    return code

class Code(Content):
    ptex2tex_envir = None     # implies LaTeX environment latex_envir
    latex_envir = None        # used if ptex2tex_envir is None

    def __init__(self, code='', file=None, from_regex=None, to_regex=None,
                 leftmargin='7mm', fontsize=r'\footnotesize',  # Verbatim
                 ptex2tex_envir=None, latex_envir=None):

        if ptex2tex_envir is None:
            if Code.ptex2tex_envir is not None:
                # Use class "global" variable, set by the user
                ptex2tex_envir = Code.ptex2tex_envir
        if latex_envir is None:
            if Code.latex_envir is not None:
                # Use class "global" variable, set by the user
                latex_envir = Code.latex_envir
            else:
                latex_envir = 'Verbatim'

        # For Verbatim/minted environment (latex_envir)
        if not fontsize.startswith('\\'):
            fontsize = '\\' + fontsize
        if Content.font_scale:
            # Adjust fontsize
            if fontsize == r'\footnotesize':
                fontsize = r'\tiny'
            elif fontsize == r'\small':
                fontsize = r'\footnotesize'

        ltx = verbatimCode(code, file, from_regex, to_regex,
                           leftmargin, fontsize, ptex2tex_envir,
                           latex_envir)
        Content.__init__(self, ltx)

    def __str__(self):
        return str(self._ltx)

    def __repr__(self):
        return repr(self._ltx)

    def __add__(self, other):
        if isinstance(other, Text):
            raise TypeError, 'Cannot add Code and Text, use comma'
        return self._ltx + other

    def __radd__(self, other):
        if isinstance(other, Text):
            raise TypeError, 'Cannot add Code and Text, use comma'
        return other + self._ltx

class Table(Content):
    def __init__(self, table, column_headline_pos='c', column_pos='c'):
        """
        Translates a two-dimensional list of data, containing strings or
        numbers, optionally with row and column headings,
        to a LaTeX tabular environment.

        @param column_headline_pos: position l/c/r for the headline row.
        @param column_pos: specify the l/c/r position of data entries in columns,
        give either (e.g.) 'llrrc' or one char (if all are equal).
        @return: The LaTeX code.
        """
        Content.__init__(self, _latextable(table, column_headline_pos, column_pos))

class Block(Content):
    unblock = False  # can be used to turn off block formatting for all blocks
    def __init__(self, heading='', content=[], code=False):
        self.heading = heading
        self.content = content
        Content.checkVerbatim(self, content)
        if code:
            self._verbatim = True

class TextBlock(Block):
    """ Block with text. """
    def __init__(self, text='', heading=""):
        self.heading = heading
        if not isinstance(text, basestring):
            text = str(text)
        Block.__init__(self, heading=heading, content=[Text(text)])

class BulletBlock(Block):
    """ Block with bulleted list. """
    def __init__(self, bullets, heading='', dim=True):
        self.heading = heading
        if not isinstance(dim, (bool,int)):
            raise ValueError, 'dim can only be True or False for a block'
        Block.__init__(self, heading=heading, content=[BulletList(bullets, dim)])

class CodeBlock(Block):
    """ Block with code. """
    def __init__(self, code='', file=None, from_regex=None, to_regex=None,
                 leftmargin='7mm', fontsize=r'\footnotesize', heading="",
                 ptex2tex_envir=None):
        self.heading = heading
        Block.__init__(self, heading=heading, code=True,
                       content=[Code(code=code, file=file,
                                     from_regex=from_regex,
                                     to_regex=to_regex,
                                     leftmargin=leftmargin,
                                     fontsize=fontsize,
                                     ptex2tex_envir=ptex2tex_envir)])

class TableBlock(Block):
    """ Block with table."""
    def __init__(self, table, column_headline_pos='c',
                 column_pos='c', heading='', center=False):
        self.heading = heading
        self.center = center
        Block.__init__(self, heading=heading,
                       content=[Table(table, column_headline_pos, column_pos)])


def _verbatim_phrases():
    pro = ' pro pypro cypro cpppro cpro fpro pl pro shpro mpro'
    cod = pro.replace('pro', 'cod')
    ptex2tex_envirs = 'ccq cc ccl cod pro cppans pyans bashans swigans uflans sni dat dsni sys slin py rpy plin' + pro + cod
    ptex2tex_phrases = ['\\e' + envir for envir in ptex2tex_envirs]
    phrases = ['{Verbatim}', '{verbatim}', 'SaveVerbatim', '{minted}'] + ptex2tex_phrases
    return phrases

def _verbatim_text(bullets):
    """
    Check if we have verbatim text (i.e., if we need a fragile command
    in a beamer frame).
    """
    verbatim = False
    phrases = _verbatim_phrases()

    for item in bullets:
        if isinstance(item, (list,tuple)):
            for item2 in item:
                for p in phrases:
                    if item2.find(p) != -1:
                        return True
        elif isinstance(item, (BulletList)):
            return _verbatim_text(item.bullets)
        elif isinstance(item, (Text, Code, Table)):
            for p in phrases:
                if item._ltx.find(p) != -1:
                    return True
        else:
            for p in phrases:
                if item.find(p) != -1:
                    return True
    return False

class Slide(object):
    """
    A presentation slide.
    """
    def __init__(self, title="", content=[], figure=None,\
                 figure_pos='s', figure_size=None, \
                 figure_fraction_width=1.0, \
                 figure_angle=None, hidden=False,\
                 left_column_width=0.5, dim=False):
        if figure_size: # Support both figure_size and figure_fraction_width
            figure_fraction_width = figure_size
        figure_size = figure_fraction_width
        if not isinstance(title, basestring):
            raise TypeError, "The title should be a string"
        if figure_pos not in (['n', 's', 'w', 'e']):
            raise TypeError, "figure_pos must be in ['n', 's', 'w', 'e']"
        self.title, self.hidden = title, hidden
        self.content = []
        if dim not in('single', 'single_then_all', 'progressive', 'blocks', True, False):
            raise ValueError, 'wrong argument value of dim argument: %s' %dim
        self._dim = dim
        self._buf = LatexBuffer()
        self._fragile = False
        self._fig_pos = figure_pos
        self._fig_sz = figure_size
        if figure:
            if not isinstance(figure_size, (list)):
                if not isinstance(figure_size, (int, float, tuple)):
                    raise TypeError, 'figure_size should be int, float, tuple or list'
                if isinstance(figure_size, tuple):
                    figure_size = list(figure_size)
                else:
                    figure_size = [figure_size,]
            self._fig = []
            if not isinstance(figure, (list, tuple)):
                if not isinstance(figure, basestring):
                    raise TypeError, "figure should be string, tuple or list"
                figure = (figure,)
            if len(figure) != len(figure_size):
                if len(figure_size) == 1:
                    figure_size *= len(figure)
            for i in range(len(figure_size)):
                figure_size[i] = float(figure_size[i])
                figure_size[i] *= Content.fig_scale
            if figure_pos in ['w', 'e']:
                for i in range(len(figure_size)):
                    figure_size[i] *= 2
                    figure_size[i] /= len(figure)
            for (f, fs) in zip(figure, figure_size):
                _fig = r'\centerline{\includegraphics[width=%f\linewidth,keepaspectratio' % fs
                if figure_angle:
                    _fig += r',angle=%s' %(str(figure_angle))
                _fig += r']{%s}}' %(f)
                self._fig.append(_fig)
        else:
            self._fig = None

        self._left_column_width = float(left_column_width)
        self._right_column_width = 1.0 - left_column_width

        for c in content:
            self.add_content(TextBlock(c) if isinstance(c, str) else c)

    @property
    def hide(self):
        self.hidden = True
        return self
    @property
    def unhide(self):
        self.hidden = False
        return self

    def add_content(self, content):
        if content._verbatim:
            self._fragile = True
        self.content.append(content)

class BulletSlide(Slide):
    """ A slide with a block enclosing a bullet list. """
    def __init__(self, title="", bullets=[], block_heading="", hidden=False, dim=False):
        if not isinstance(bullets, (list, tuple)):
            raise TypeError, "Bullets should be passed as a sequence"
        Slide.__init__(self, title=title, hidden=hidden, dim=dim)
        self.add_content(BulletBlock(heading=block_heading, bullets=bullets))

class TextSlide(Slide):
    """ A slide with a block of text. """
    def __init__(self, title="", text="", block_heading="", hidden=False):
        Slide.__init__(self, title=title, hidden=hidden)
        self.add_content(TextBlock(heading=block_heading, text=text))

class RawSlide(Slide):
    """ A slide consisting of pure LaTeX text for a complete slide. """
    def __init__(self, rawtext="", hidden=False):
        Slide.__init__(self, title="", hidden=hidden, dim=False)
        self.add_content(Raw(rawtext))

class TableSlide(Slide):
    """ A slide consisting of a LaTeX table. """
    def __init__(self, title="", table=[[],[]], column_headline_pos='c',
                 column_pos='c', center=False, block_heading="", hidden=False):
        Slide.__init__(self, title=title, hidden=hidden)
        self.add_content(TableBlock(heading=block_heading, table=table, center=center,
                                    column_headline_pos=column_headline_pos,
                                    column_pos=column_pos))

def generate_mapping_slide_table(heading_figure_pairs):
    fp = heading_figure_pairs # short form
    #text = r"""\begin{frame}[plain]"""
    text = ""
    nrows = len(fp)
    ncolumns = len(fp) + 1
    column_width = 1.0/ncolumns
    for r in range(nrows):
        text += r"""
\begin{columns}
"""
        for c in range(ncolumns-1):  # c==r writes two columns, skip the last
            if c == r:
                if len(fp[r]) == 3:
                    # 3rd element is the figure width
                    figure_width = fp[r][2]
                else:
                    figure_width = 1.0  # default
                text += r"""\column{%s\textwidth}
    \centerline{\includegraphics[width=%s\linewidth,keepaspectratio]{%s}}
\column{%s\textwidth}
    %s
    """ % (column_width, figure_width, fp[r][1], column_width, fp[r][0])
            else:
                text += r"""\column{%s\textwidth}
""" % column_width
        text += r"""\end{columns}
    """
    return text

class MappingSlide(Slide):
    """
    Michael Alley-style mapping slide: tabular format of images and text
    to communicate the contents of a talk.
    """
    def __init__(self, heading_figure_pairs=[]):
        Slide.__init__(self, title="", hidden=False, dim=False)
        rawtext = generate_mapping_slide_table(heading_figure_pairs)
        self.add_content(Raw(rawtext))


class LatexBuffer(object):
    """ Verifying LaTeX buffer """
    __rePhrases = [re.compile(p) for p in ['\b', r'\sexttt\{.+\}',]]

    def __init__(self):
        self._buf = StringIO()
        self._verbatim = False

    def tell(self):
        return self._buf.tell()

    def write(self, txt, validate=True):
        """
        Write text to buffer after, after optionally checking
        whether LaTeX backslashes are there or raw strings have
        been forgotten.
        """
        if validate:
            for rp in self.__rePhrases:
                #print 'checking "%s" in %s' % (p, string)
                if rp.search(txt):
                    raise ValueError, \
                          'This text,\n----\n%s\n----\ncontains '\
                          'LaTeX commands but was not typed as a raw string' \
                          % txt

        # Why this??? Nothing happens and actions for verbatim envirs
        # are taken in _verbatim_text
        if not self._verbatim:
            phrases = _verbatim_phrases()
            for p in phrases:
                if txt.find(p) != -1:
                    self._verbatim = True
                    break

        self._buf.write(txt)

    def get_text(self):
        return self._buf.getvalue()

class SubSection(object):
    """A presentation Subsection"""
    def __init__(self, title="", slides=None, short_title=""):
        self.slides = slides
        self.hidden = True

        self._title = title
        if short_title:
            short_title = '[%s]' % short_title
        self._short_title = short_title

    def __repr__(self):
        return '%s %s' % (self._title, repr(self.slides))

    def add_slide(self, slide):
        self.slides.append(slide)

class Section(object):
    """ A presentation section. """
    def __init__(self, title="", slides=None, short_title=""):
        hasslides = slides and isinstance(slides[0], Slide)
        self.slides = slides if hasslides else []
        self.subsections = [] if hasslides else slides
        self.hidden = True

        self._title = title
        if short_title:
            short_title = '[%s]' % short_title
        self._short_title = short_title

    def __repr__(self):
        return '%s %s' % (self._title, repr(self.subsections))

    def add_slide(self, slide):
        if not self.subsections:
            self.slides.append(slide)
        else:
            self.subsections[-1].add_slide(slide)


class Slides(object):
    """ Superclass for different slide packages."""
    def __init__(self,
                 title='Here goes the title of the talk',
                 author_and_inst=[('author1','inst1'),
                                  ('author2','inst2', 'inst3')],
                 date=None,
                 figure=None,
                 titlepage_figure=None,
                 titlepage_figure_fraction_width=1.0,
                 titlepage_left_column_width=0.5,
                 titlepage_figure_pos='s',
                 short_title='',
                 short_author=None,
                 copyright_text=None,
                 toc_heading="Outline",
                 toc_figure=None,
                 toc_figure_fraction_width=1.0,
                 toc_left_column_width=0.5,
                 colour=True,
                 handout=False,
                 newcommands=[],
                 beamer_theme="shadow",
                 beamer_colour_theme="default",
                 prosper_style="default",
                 header_footer=True,
                 latexpackages="",
                 html=False,
                 titlepage=True):
        """See the documentation for what the arguments mean."""

        elements = locals()
        del elements['self']
        for key, value in elements.items():
            setattr(self, key, value)
        self.newcommands = [r"{\emp}[1]{{\smaller\texttt{#1}}}", r"{\mathbfx}[1]{{\mbox{\boldmath $#1$}}}"]

        if not isinstance(newcommands, (tuple, list)):
            for command in newcommands.strip().split(r"\newcommand"):
                if len(command) > 1:
                    self.newcommands.append(command)
        else:
            self.newcommands += newcommands

        if html:
            addpackage = r"""\usepackage{tex4ht}"""
            self.latexpackages += "\n"
            self.latexpackages += addpackage
        self.slides = []
        self.sections = []
        self.buf = StringIO()
        self._dim = False
        self._header()
        self._init_titlepage()
        self._titlepage()
        self.renderContent = {}
        # The render methods for most Content subclasses must be moved to the
        # subclasses of Slides, as they are package-dependent. In order to
        # keep track of which one to call, we create a dictionary that maps
        # the type of the Content subclass to a renderfunction specific for
        # that subclass. Hence, renderContent[BulletBlock] refers to
        # Slide._renderBulletBlock():
        for subclass in Content.__subclasses__():
            self.addSubClasses(subclass)

    def addSubClasses(self, content, root=True):
        if root == True: root = content
        self.renderContent[content] = eval('self._render%s' % root.__name__)
        for c in content.__subclasses__():
            self.addSubClasses(c, root)

    def _header(self):
        pass

    def _main(self):
        pass

    # Initialize title page
    def _init_titlepage(self):
        self.buf.write("\n% User's newcommands:\n" + "\n".join([r"\newcommand%s" % n for n in self.newcommands]) + '\n')
        self.buf.write(r"""
\begin{document}
""")

        if self.date is None:
            import time
            self.date = time.strftime("%B %d, %Y")

        # Transform author_and_inst to [(author, instlist), ...]
        # from [(author, inst1, inst2, ...), ...]
        self.author_and_inst = [(elem[0], elem[1:]) for elem in self.author_and_inst]

        # Institutions are written only once
        # (put institutes in a set to avoid multiple items, but use
        # a list to hold the distinct institutitions for correct
        # sequence, join the list with \and):
        tmp = set()
        insts = []
        counter = 1
        for a, i in self.author_and_inst:
            for inst in i:
                if not inst in tmp:
                    insts.append(inst)
                    tmp.add(inst)

        if len(self.author_and_inst) > 1:
            institute_cmd = []  # Insts with latex decorations
            # Prefix \inst{1}:
            for i in range(len(insts)):
                institute_cmd.append(insts[i] + r'\inst{%d}' % (i + 1))
            # Join all institutes with \and:
            institute_cmd = '\n\\and\n'.join(institute_cmd)
            # Couple each author with institutions:
            author_cmd = []
            for a, i in self.author_and_inst:
                author_cmd.append(\
                a + r'\inst{%s}' % (','.join([str(insts.index(inst) + 1) for inst in i])))
            author_cmd = '\n\\and\n'.join(author_cmd)
        else:  # Just one author, drop the footnote
            institute_cmd = '\n\\and\n'.join(self.author_and_inst[0][1])
            author_cmd = self.author_and_inst[0][0]

        if self.short_title:
            self.short_title = '[%s]' % self.short_title
        if not self.short_author:
            # Use standard rules:
            first_author = ''.join(self.author_and_inst[0][0].split()[-1])
            if len(self.author_and_inst) == 1:
                # Just last name of a single author:
                self.short_author = first_author
            elif len(self.author_and_inst) == 2:
                # Just last name of the two authors:
                second_author = ''.join(self.author_and_inst[1][0].split()[-1])
                self.short_author = first_author + ' and ' + second_author
            else:
                self.short_author = first_author + ' et al.'
            self.short_author = '[%s]' % self.short_author
        else:
            self.short_author = '[%s]' % self.short_author
        self.institute_cmd = institute_cmd
        self.author_cmd = author_cmd
        self.insts = insts

    def add_slide(self, slide):
        """ Add slide to content.

        If this presentation is not yet divided into sections, the slide is added directly to the slides attribute.
        Otherwise the slide is added to the last section.
        """
        if isinstance(slide, (Section)):
            self.sections.append(slide)
        elif isinstance(slide, Slide):
            self.slides.append(slide)
        else:
            raise TypeError("Can only add sections and slides to presentations")
        if self.sections and self.slides:
            raise TypeError("Cannot have both slides and sections at root level")

    def add_slides(self, slides, generate_slides=False):
        """ Add several slides at the same time. """
        if generate_slides:
            slides = make_tree(slides)
        for slide in slides:
            self.add_slide(slide)

    def get_latex(self):
        self.buf = StringIO()
        self.buf.write(self._ltx)
        # Top-level slides
        for s in self.slides:
            self._renderSlide(s)
        # Now the nested content
        for s in self.sections:
            self._renderSection(s)

        self.buf.write(r"""
\end{document}
""")

        return self.buf.getvalue()

    def _renderSlide(self, slide):
        pass

    def _renderSection(self, section):
        pass

    def _renderSubsection(self, subsection):
        pass

    def _renderRaw(self, raw):
        raw.render(self.buf)

    def _renderText(self, text):
        text.render(self.buf)

    def _renderBulletList(self, bulletlist):
        bulletlist.render(self.buf)

    def _renderCode(self, code):
        code.render(self.buf)

    def _renderTable(self, table):
        table.render(self.buf)

    def _renderBlock(self, block):
        block.render(self.buf)

    def _renderTextBlock(self, textblock):
        textblock.render(self.buf)

    def _renderBulletBlock(self, bulletblock):
        bulletblock.render(self.buf)

    def _renderCodeBlock(self, codeblock):
        codeblock.render(self.buf)

    def _renderTableBlock(self, tableblock):
        tableblock.render(self.buf)

    def write(self, filename):
        text = self.get_latex()
        of = open(filename, 'w')
        of.write(text)
        of.close()

def make_tree(sections, parent=None):
    if parent is None:
        return [make_tree(section, "root") for section in sections]
    if isinstance(sections, Slide):
        return sections
    elif isinstance(sections, (tuple, list)) and len(sections) > 1:
        if len(sections) == 2: sections = (sections[0], sections[0], sections[1])
        title, shorttitle, children = sections
        cls = Section if parent == "root" else SubSection
        return cls(title, [make_tree(child, "sect") for child in children], shorttitle)
    else:
        raise ValueError("Got %s as a slide or section" % repr(sections))