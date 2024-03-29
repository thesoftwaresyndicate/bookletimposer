% BookletImposer / pdfimposer
% Achieve some basic imposition on PDF documents


What is it ?
============

Bookletimposer is an utility to achieve some basic imposition on PDF
documents, especially designed to work on booklets.

Bookletimposer is implemented as a commandline and GTK+ interface to pdfimposer,
a reusable python module built on top of pyPdf.

It was tested on GNU/Linux althought it may work on any systems with a Python
interpreter.

Bookletimposer and pdfimposer are both free software released under the GNU
General Public License, either version 3 or (at your option) any later version.
See COPYING for the full text of the license.


Features
========

- transform linear documents to booklets
- transform booklets to linear documents
- reduce a document to put many on one sheet


Development state
=================

BookletImposer should be quite stable. Thanks to report bugs on
<https://git.codecoop.org/kjo/bookletimposer/issues>!

Dependencies
============

pdfimposer requires:

- python (>= 2.6)
- pyPdf2 (>= 1.23)

BookletImposer also requires:

- PyGObject
- gtk+ (>= 3.0)
- glib

In addition, the build and installation process requires:

- python-distutils-extra
- pandoc

And to build the website:

- python-epydoc
- xsltproc
- docbook-xsl

Quick installation
==================

Once the tarball downloaded and extracted:

    $ ./setup.py build

Then as root:

    # ./setup.py install


pdfimposer API documentation
============================

See generated epydoc documentation (available at
<https://kjo.herbesfolles.org/bookletimposer/api/>)


BookletImposer usage
====================

BookletImposer can be launched from the Office section of the Application menu,
or with te command:

    $ bookletimposer

Help on command line options is available in the man page.
