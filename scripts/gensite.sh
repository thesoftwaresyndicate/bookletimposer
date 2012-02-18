#!/bin/sh
pandoc --output site/index.html \
    --css style.css \
    --standalone \
    --table-of-contents \
    site/index.mdwn
txt2tags --target=html \
    --outfile=site/bookletimposer.1.html \
    --style=style.css \
    --css-sugar \
    doc/bookletimposer.1.t2t
xsltproc -o site/help.html \
    --stringparam html.stylesheet style.css \
    /usr/share/xml/docbook/stylesheet/nwalsh/xhtml/docbook.xsl \
    help/C/bookletimposer.xml
epydoc --docformat=restructuredtext \
    --output=site/api/ \
    --inheritance=included \
    --no-private \
    --no-frames \
    lib/pdfimposer.py
cp -r help/C/figures site/figures
