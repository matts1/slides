import os

from latexslides import Code as OldCode, Content
from subprocess import Popen, PIPE


class Code(OldCode):
    def __init__(self, code='', file=False, language="python3", fontsize=r'\footnotesize', linenos=False, mathescape=True, **kwargs):
        style = dict(python3="idleclassic", python="idleclassic").get(language, "default")
        style = "default" # TODO: get this working without this
        kwargs.update(fontsize=fontsize, linenos=linenos, mathescape=mathescape, numberblanklines=True)
        kwargs = ",".join(["%s=%s" % (key, value) for key, value in kwargs.items()])
        code = open(code, "rU").read() if file else code
        ltx = "\\usemintedstyle{%s}\n\\begin{minted}[%s]{%s}\n%s\n\\end{minted}" % (style, kwargs, language, code)
        Content.__init__(self, ltx)


class ShellCode(Code):
    mode = "shell"

    def __init__(self, code='', data="", fromfile=False, language="python3", fontsize=r'\footnotesize', linenos=False,
                 mathescape=True, **kwargs):
        code = open(code, "rU").read() if fromfile else code
        f = open("executing.py", "w")
        f.write(code.strip("\n"))
        f.close()
        f = open("data.txt", "w")
        f.write(data)
        f.close()
        code = Popen(["python3", "executor.py", self.mode], stdout=PIPE).communicate()[0]
        super(ShellCode, self).__init__(code, False, language, fontsize, linenos, mathescape, **kwargs)

        os.remove("data.txt")
        os.remove("executing.py")


class ExecCode(Code):
    mode = "exec"
