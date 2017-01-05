#!/bin/sh
mkdir -p build/site
echo copying images
cp site/img build/site/ -r
echo generate main page
pandoc --output build/site/index.html \
    --include-before-body site/inc_title.html \
    --css style.css \
    --standalone \
    --table-of-contents \
    site/index.mdwn
echo generate changelog page
pandoc --output build/site/changelog.html \
    --include-before-body site/inc_title.html \
    --css style.css \
    --standalone \
    CHANGELOG
echo generate todo page
pandoc --output build/site/todo.html \
    --css style.css \
    --include-before-body site/inc_title.html \
    --standalone \
    TODO
echo generate man page
pandoc --output=build/site/bookletimposer.1.html \
    --css style.css \
    --include-before-body site/inc_title.html \
    --standalone \
    doc/bookletimposer.1.mdwn
echo generate online help
xsltproc -o build/site/help.html \
    --stringparam html.stylesheet style.css \
    /usr/share/xml/docbook/stylesheet/nwalsh/xhtml/docbook.xsl \
    help/C/index.docbook
cp -r help/C/figures site/figures
echo generate API documentation
epydoc --docformat=restructuredtext \
    --output=build/site/api/ \
    --inheritance=included \
    --no-private \
    --no-frames \
    lib/pdfimposer.py
