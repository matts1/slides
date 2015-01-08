#! /usr/bin/python3

import sys
from code import InteractiveConsole
from io import StringIO

class Stdin(StringIO):
    def __init__(self, data):
        self.data = data
        self.upto = 0
        Stdin.instance = self

    def readline(self, *args, **kwargs):
        line = self.data[self.upto].rstrip()
        self.upto += 1
        return line

def myinput(prompt=""):
    value = Stdin.instance.readline()
    FileCacher.instance.write(prompt + value + "\n")
    return value

class FileCacher:
    "Cache the stdout text so we can analyze it before returning it"
    def __init__(self):
        self.reset()
        FileCacher.instance = self
    def reset(self): self.out = []
    def write(self,line): self.out.append(line)
    def flush(self):
        output = ''.join(self.out)
        self.reset()
        return output

class ErrorCatcher(FileCacher):
    def write(self, line):
        FileCacher.write(self, line)

    def flush(self):
        output = ''.join(self.out)
        self.reset()
        FileCacher.instance.write(output)

class Shell(InteractiveConsole):
    "Wrapper around Python that can filter input/output to the shell"

    def __init__(self, code, inputs):
        self.stdin = Stdin(inputs)
        sys.stdin = self.stdin
        self.cache = FileCacher()
        self.stdout = sys.stdout
        self.upto = 0
        self.code = code
        self.output = ""
        super(Shell, self).__init__()
        self.locals['input'] = myinput


    def get_output(self): sys.stdout = self.cache
    def return_output(self): sys.stdout = self.stdout

    def raw_input(self, prompt=""):
        lines = self.code[self.upto].rstrip() + "\n"
        self.upto += 1
        while self.upto < len(self.code) and self.code[self.upto][0] in " \t":
            lines += self.code[self.upto].rstrip() + "\n"
            self.upto += 1
        return lines


    def push(self,line):
        sys.stdout = self.cache  # output to the cache
        # you can filter input here by doing something like
        # line = filter(line)
        try:
            InteractiveConsole.push(self,line)
        except Exception as e:
            raise TypeError
        sys.stdout = self.stdout  # put stdout back to what it should be
        output = self.cache.flush()
        # you can filter the output here by doing something like
        # output = filter(output)
        # print(output) # or do something else with it
        self.output += output
        # more if the next line is indented
        return self.upto < len(self.code) and self.code[self.upto][0] in " \t"

    def interact(self, banner=None):
        """Closely emulate the interactive Python console.

        The optional banner argument specifies the banner to print
        before the first interaction; by default it prints a banner
        similar to the one printed by the real Python interpreter,
        followed by the current class name in parentheses (so as not
        to confuse this with the real interpreter -- since it's so
        close!).

        """
        sys.ps1 = ">>> "
        sys.ps2 = "... "
        more = 0
        while self.upto < len(self.code):
            try:
                prompt = sys.ps2 if more else sys.ps1
                try:
                    line = self.raw_input(prompt)
                    self.output += prompt + line
                except EOFError:
                    self.write("\n")
                    break
                else:
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = 0

mode = sys.argv[1]
code = open("executing.py", "rU").readlines()
inputs = open("data.txt", "rU").readlines()
if mode == "shell":
    sh = Shell(code, inputs)
    sh.interact()
    print(sh.output)