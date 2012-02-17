pandoc -o site/index.html -s site/index.mdwn
txt2tags --target=html --outfile=site/bookletimposer.1.html doc/bookletimposer.1.t2t 
docbook2html -o site/help help/C/bookletimposer.xml
epydoc --docformat=restructuredtext --output=site/api/ --inheritance=included --no-private --no-frames --verbose lib/pdfimposer.py
ln -s ../../help/C/figures site/help/figures
