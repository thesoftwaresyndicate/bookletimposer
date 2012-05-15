#!/bin/sh
pandoc --output site/index.html \
    --css style.css \
    --standalone \
    --table-of-contents \
    site/index.mdwn
pandoc --output=site/bookletimposer.1.html \
    --css style.css \
    --include-before-body site/inc_title.html \
    --standalone \
    doc/bookletimposer.1.mdwn
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
