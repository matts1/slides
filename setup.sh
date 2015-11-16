#!/bin/bash
sudo apt-get install ptex2tex latex-beamer python-pygments
sudo apt-get install texlive-latex-base # for pdflatex, can probably find a more minimal package
sudo apt-get install texlive-latex-extra # for minted, again want a more minimal package

git clone git://github.com/matts1/pygments-style-idleclassic.git
cd pygments-style-idleclassic
sudo python setup.py install
cd -
rm -r pygments-style-idleclassic