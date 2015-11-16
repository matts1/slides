#!/bin/sh
rm -f lesson.pdf compiled/lesson.p.tex compiled/lesson.tex
# $1 means if you say 'sh build.sh handout', it automatically does handout mode
python lesson.py $1
if [ $? -eq 0 ]
  then
    cd compiled
    ptex2tex -DMINTED lesson.p.tex
    pdflatex -shell-escape -synctex=1 -interaction=nonstopmode lesson
    cd ..
#    sh clean.sh
    mv compiled/lesson.pdf .
    xdg-open lesson.pdf & # run in the background
#    rm data.txt executing.py
fi

./clean.sh