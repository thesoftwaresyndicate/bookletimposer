#!/bin/sh
echo generate main page
pandoc --output site/index.html \
    --include-before-body site/inc_title.html \
    --css style.css \
    --standalone \
    --table-of-contents \
    site/index.mdwn
echo generate changelog page
pandoc --output site/changelog.html \
    --include-before-body site/inc_title.html \
    --css style.css \
    --standalone \
    CHANGELOG
echo generate todo page
pandoc --output site/todo.html \
    --css style.css \
    --include-before-body site/inc_title.html \
    --standalone \
    TODO
echo generate man page
pandoc --output=site/bookletimposer.1.html \
    --css style.css \
    --include-before-body site/inc_title.html \
    --standalone \
    doc/bookletimposer.1.mdwn
echo generate online help
xsltproc -o site/help.html \
    --stringparam html.stylesheet style.css \
    /usr/share/xml/docbook/stylesheet/nwalsh/xhtml/docbook.xsl \
    help/C/bookletimposer.xml
cp -r help/C/figures site/figures
echo generate API documentation
epydoc --docformat=restructuredtext \
    --output=site/api/ \
    --inheritance=included \
    --no-private \
    --no-frames \
    lib/pdfimposer.py
