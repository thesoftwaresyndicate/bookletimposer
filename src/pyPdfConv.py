#!/usr/bin/env python
# -*- coding: UTF-8 -*-

########################################################################
# 
# PyPdfConv - Utility to convert PDF files between diffrents page layouts
# Copyright (C) 2008-2009 Kjö Hansi Glaz <kjo AT a4nancy DOT net DOT eu DOT org>
# 
# This program is  free software; you can redistribute  it and/or modify
# it under the  terms of the GNU General Public  License as published by
# the Free Software Foundation; either  version 3 of the License, or (at
# your option) any later version.
# 
# This program  is distributed in the  hope that it will  be useful, but
# WITHOUT   ANY  WARRANTY;   without  even   the  implied   warranty  of
# MERCHANTABILITY  or FITNESS  FOR A  PARTICULAR PURPOSE.   See  the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

########################################################################
#
# pyPdfConv.py
#
# This python module enables to change PDF page layout. It is the backend
# of pyPdfConv.
#
########################################################################

# IMPORT REQUIRED MODULES
# =======================

# XXX gruge de dev
if True:
    import sys
    sys.path = ["/home/kjo/Documents/Dev/pyPdfConv/pypdf-git/pyPdf"] + sys.path
    print "DEBUG added custom pyPdf dir in path, which is now ", sys.path
# XXX /gruge de dev

# abstract base class (up to python 2.6.1)
#import abc

import re
import sys
import os

import pyPdf
import pyPdf.generic
import pyPdf.pdf

# XXX: Fix these translatable strings
_ = lambda x: x

########################################################################

# XXX: I think there is a best way to define constants
BOOKLETIZE = 1
LINEARIZE = 2
REDUCE = 3

PORTRAIT = False
LANDSCAPE = True

########################################################################

class PyPdfError(Exception):
    """
    This class defines the exceptions raised by PyPdfConv;

    The attribute "message" contains a message explaining the cause of the
    error
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

########################################################################

class MismachingOrientationsError(PyPdfError):
    """
    This exception is raised if the output page orientation is incompatible
    with the input page orientation.

    XXX: Document the error message
    """

########################################################################

class UnknownFormatError(PyPdfError):
    """
    This exception is raised when the user tries to set an unknown page
    format.
    """

########################################################################

class AbstractConverter(object):
    #__metaclass__ = abc.ABCMeta
    """
    This class provides an interface for various conversions on PDF files.
    It is an abstract class, with some abstract functions which should be
    overriden.
    """

    page_formats = {
        "A3":(841,1190),
        "A3":(842,1192),
        "A4":(595,841),
        "A4":(595,842),
        "A5":(420,595), 
        }

    def __init__(self, 
                 conversion_type=BOOKLETIZE, 
                 layout='2x1',
                 format='A4',
                 orientation=PORTRAIT,
                 copy_pages=False):
        """
        XXX: Documentation
        """
        self.conversion_type = None
        self.layout = None
        self.output_format = None
        self.output_orientation = None

        self.set_conversion_type(conversion_type)
        self.set_layout(layout)
        self.set_output_format(format)
        self.set_output_orientation(orientation)
        self.set_copy_pages(copy_pages)

        def default_progress_callback(msg, prog):
            print "%s (%i%%)" % (msg, prog*100)

        self.set_progress_callback(default_progress_callback)


    # GETTERS AND SETTERS
    # ===================

    def set_output_height(self, height):
        # XXX: verify that height > width
        self.output_height = int(height)

    def get_output_height(self):
        return self.output_height

    def set_output_width(self, width):
        # XXX: verify that height > width
        self.output_width = int(width)

    def get_output_width(self):
        return self.output_width

    def set_output_orientation(self, output_orientation):
        self.output_orientation = bool(output_orientation)

    def get_output_orientation(self):
        return self.output_orientation

    def set_pages_in_width(self, num):
        self.pages_in_width = int(num)

    def get_pages_in_width(self):
        return self.pages_in_width

    def set_pages_in_height(self, num):
        self.pages_in_height = int(num)

    def get_pages_in_height(self):
        return self.pages_in_height

    def set_conversion_type(self, type):
        assert(type == BOOKLETIZE or type == LINEARIZE or type == REDUCE)
        self.conversion_type = type

    def get_conversion_type(self):
        return self.conversion_type

    def set_copy_pages(self, copy_pages):
        self.copy_pages = bool(copy_pages)

    def get_copy_pages(self):
        return self.copy_pages

    def set_progress_callback(self, progress_callback):
        """
        Register a callback function that will be called to inform on the progress of the conversion
        
        @param progress_callback The callback function which is called to return the conversion progress. Its signature must be : a string for the progress message; a number in the range [0, 1] for the progress
        """
        # XXX: Fix this check
        assert(isinstance(progress_callback, type(lambda x: x)))
        self.progress_callback = progress_callback

    def get_progress_callback(self):
        """
        Gets the callback function that will be called to inform on the progress of the conversion
        
        @return progress_callback The callback function which is called to return the conversion progress. Its signature must be : a string for the progress message; a number in the range [0, 1] for the progress
        """

    # SOME GETTERS THAT CALCULATE THE VALUE THEY RETURN FROM OTHER VALUES
    # ===================================================================
    def get_size(self):
        """
        Returns the page size of the input PDF file, expressed in default user space units
        """
        return (self.get_width(), self.get_height())

    #@abstractmetod
    def get_height(self):
        """
        Returns the height of the input PDF file, expressed in default user space units

        """
        pass

    #@abstractmetod
    def get_width(self):
        """
        Returns the width of the input PDF file, expressed in pts

        """
        pass

    def get_orientation(self):
        if self.get_height() > self.get_width():
            return PORTRAIT
        elif self.get_height() < self.get_width():
            return LANDSCAPE
        else:
            #XXX: is square
            return None

    def set_layout(self, num):
        pages_in_width, pages_in_height = num.split('x')
        self.set_pages_in_width(int(pages_in_width))
        self.set_pages_in_height(int(pages_in_height))

    def get_layout(self):
        return str(self.pages_in_width) + 'x' + str(self.pages_in_height)

    def get_pages_in_sheet(self):
        return self.pages_in_width * self.pages_in_height

    def set_output_format(self, format):
        try:
            width, height = AbstractConverter.page_formats[format]
            self.set_output_height(height)
            self.set_output_width(width)
        except KeyError:
            raise UnknownFormatError(format)

    def get_output_format(self):
        for output_format in AbstractConverter.page_formats.keys():
            if AbstractPdfConv.page_formats[output_format] == \
                (self.get_output_width, self.get_output_height):
                return output_format

    def get_page_format(self):
        """
        Returns the page format of the input PDF file (eg. A4)

        """
        for k in self.page_formats.keys():
            if self.page_formats[k] == self.get_size():
                return k

    #@abstractmetod
    def get_page_count(self):
        """
        Returns the number of pages of the input PDF file

        """
        pass

    def get_reduction_factor(self):
        """
        Calculates the reduction factor

        @return the reduction factor
        """
        return float(self.get_output_width()) / \
            (self.get_pages_in_width() * self.get_width())

    def get_increasing_factor(self):
        """
        Calculates the increasing factor

        @return the increasing factor
        """
        return float(self.get_pages_in_width() * self.get_output_width()) / \
            self.get_width()

    # CONVERSION FUNCTIONS
    # ====================

    def run(self):
        """
        Do the actual conversion.

        This method launches the actual conversion, using the parameters set
        before.
        """
        if self.conversion_type == BOOKLETIZE:
            self.bookletize()
        elif self.conversion_type == LINEARIZE:
            self.linearize()
        elif self.conversion_type == REDUCE:
            self.reduce()

    #@abstractmethod
    def bookletize(self):
        """
        Converts a linear PDF to a booklet.
        """
        pass

    #@abstractmethod
    def lineraize(self):
        """
        Converts a booklet to a linear PDF.
        """
        pass

    #@abstractmethod
    def reduce(self):
        """
        Reduce a PDF.

        """
        pass

########################################################################

class StreamConverter(AbstractConverter):
    """
    XXX: documentation
    """

    def __init__(self,
                 input_stream, 
                 output_stream,
                 conversion_type=BOOKLETIZE, 
                 layout='2x1',
                 format='A4',
                 orientation=PORTRAIT,
                 copy_pages=False):
        """
        XXX: documentation
        """

        AbstractConverter.__init__(self, conversion_type, layout, format, 
                                   orientation, copy_pages)

        

        self.output_stream = output_stream
        self.input_stream = input_stream

        self.inpdf = pyPdf.PdfFileReader(input_stream)

    def get_height(self):
        """
        Returns the height of the input PDF file, expressed in default user space units

        """
        page = self.inpdf.getPage(0)
        height = page.mediaBox.getHeight()
        return int(height)

    def get_width(self):
        """
        Returns the width of the 1st page of the input PDF file, expressed in pts
        
        """
        page = self.inpdf.getPage(0)
        width = page.mediaBox.getWidth()
        return int(width)

    def get_page_count(self):
        """
        Returns the number of pages of the input PDF file
        
        """
        return self.inpdf.getNumPages()

    def __fix_page_orientation(self, cmp):
        """
        Adapt the output page orientation
        """
        if cmp(self.get_pages_in_width(), self.get_pages_in_height()):
            if self.get_orientation() == PORTRAIT:
                if self.get_output_orientation() == PORTRAIT:
                    self.set_output_orientation(LANDSCAPE)
            else: #if self.get_orientation() == LANDSCAPE:
                raise MismachingOrientationsError("2X x X")
        elif cmp(self.get_pages_in_height(), self.get_pages_in_width()):
            if self.get_orientation() == LANDSCAPE:
                if self.get_output_orientation() == LANDSCAPE:
                    self.set_output_orientation(PORTRAIT)
            else:
                # XXX: Localized error message
                raise MismachingOrientationsError("X x 2X")
        else:
            if self.get_orientation() == LANDSCAPE:
                if self.get_output_orientation() == PORTRAIT:
                    self.set_output_orientation(LANDSCAPE)
            else:
                if self.get_output_orientation() == LANDSCAPE:
                    self.set_output_orientation(PORTRAIT)

    def __fix_page_orientation_for_booklet(self):
        """
        Adapt the output page orientation
        """
        def __is_two_times(op1, op2):
            if op1 == 2 * op2:
                return True
            else:
                return False
        self.__fix_page_orientation(__is_two_times)
        #self.__fix_page_orientation(lambda op1, op2: [False, True][op1 == 2 * op2])

    def __fix_page_orientation_for_linearize(self):
        def __is_half(op1, op2):
            if op2 == 2 * op1:
                return True
            else:
                return False
        self.__fix_page_orientation(__is_half)
        #self.__fix_page_orientation(lambda op1, op2: [False, True][op2 == 2 * op1])

    def __get_sequence_for_booklet(self):
        """
        XXX: Documentation
        """
        n_pages = self.get_page_count()
        pages = range(0, n_pages)
        print "initial pages =", pages # XXX: DEBUG

        # Check for missing pages
        print n_pages % 4
        if (n_pages % 4) == 0:
            n_missing_pages = 0
        else:
            #n_missing_pages = (4 - (n_pages % 4)) / self.get_pages_in_sheet()
            n_missing_pages = 4 - (n_pages % 4)
            # si le nombre de pages n'est pas divisible par 4,
            # XXX: afficher un warning (autre callback ?)
        print "n_missing_pages =", n_missing_pages

        # Add reference to the missing empty pages to the pages sequence
        for missing_page in range(0, n_missing_pages):
            pages.append(None)
        print "pages after adding blank pages =", pages # XXX: DEBUG

        # XXX: Document this
        def append_and_copy(list, pages):
            """
            XXX: Doc
            """
            if self.get_copy_pages():
                for i in range(self.get_pages_in_sheet() / 2):
                    list.extend(pages)
            else:
                list.extend(pages)

        # Arranges the pages in booklet order
        sequence = []
        while pages :
            append_and_copy(sequence, [pages.pop(), pages.pop(0)])
            append_and_copy(sequence, [pages.pop(0), pages.pop()])

        print "sequence =", sequence # XXX: DEBUG
        return sequence

    def __get_sequence_for_linearize(self, booklet=True):
        """
        XXX: Doc
        """
        # XXX: We assume copy_pages = False
        # XXX: booklet argument is not useful ?
        if booklet:
            sequence = []
            try :
                for i in range(0, self.get_page_count() *
                               self.get_pages_in_sheet(), 4):
                    sequence.append(i/2)
                    sequence.append(i/2)
                    sequence.append(i/2+1)
                    sequence.append(i/2+2)
            except IndexError :
                # XXX: Print a warning
                pass
        else:
            sequence = range(0, npages * self.get_pages_in_sheet())
        return sequence

    def bookletize(self):
        """
        Converts a linear PDF to a booklet.

        XXX: Doc
        """
        # XXX: Translated progress messages

        self.__fix_page_orientation_for_booklet()
        sequence = self.__get_sequence_for_booklet()
        outpdf = pyPdf.PdfFileWriter()

        current_page = 0
        while current_page < len(sequence):
            self.progress_callback(
                _("creating page %i") %
                    ((current_page + self.get_pages_in_sheet()) /
                        self.get_pages_in_sheet()),
                float(current_page) / len(sequence)
                )
            page = outpdf.addBlankPage(self.get_output_width(), 
                self.get_output_height())
            for vert_pos in range(0, self.get_pages_in_height()):
                for horiz_pos in range(0, self.get_pages_in_width()):
                    if sequence[current_page] is not None:
                        page.mergeScaledTranslatedPage(
                            self.inpdf.getPage(sequence[current_page]),
                            self.get_reduction_factor(), 
                            horiz_pos*self.get_output_width() / \
                                self.get_pages_in_width(),
                            self.get_output_height() - ( 
                                (vert_pos + 1) * self.get_output_height() / \
                                self.get_pages_in_height())
                            )
                    current_page += 1
            page.compressContentStreams()
        self.progress_callback(_("writing converted file"), 1)
        outpdf.write(self.output_stream)
        self.progress_callback(_("done"), 1)

    def linearize(self, booklet=True):
        """
        Revert a booklet into single pages.
        
        XXX: Doc
        """
        # XXX: Translated progress messages
        # XXX: Mauvais facteur de zoom quand 2x1 p. ex

        self.__fix_page_orientation_for_linearize()
        sequence = self.__get_sequence_for_linearize()
        outpdf = pyPdf.PdfFileWriter()

        output_page = 0
        for input_page in range(0, self.get_page_count()):
            for vert_pos in range(0, self.get_pages_in_height()):
                for horiz_pos in range(0, self.get_pages_in_width()):
                    self.progress_callback(
                        _("extracting page %i") % output_page + 1,
                        float(output_page) / len(sequence))
                    page = outpdf.insertBlankPage(self.get_output_width(),
                                                  self.get_output_height(),
                                                  sequence[output_page])
                    page.mergeScaledTranslatedPage(
                        inpdf.getPage(input_page),
                        self.get_increasing_factor (), 
                        - horiz_pos * self.get_output_width(),
                        (vert_pos - self.get_pages_in_height() + 1) * \
                            self.get_output_height ()
                        )
                    page.compressContentStreams()
                    output_page += 1
          
        self.progress_callback(_("writing converted file..."), 1)
        outpdf.write(outfile)
        self.progress_callback(_("done"), 1)

########################################################################

class FileConverter(StreamConverter):
    """
    XXX: documentation
    """

    def __init__(self,
                 infile_name,
                 outfile_name=None,
                 conversion_type=BOOKLETIZE, 
                 layout='2x1',
                 format='A4',
                 orientation=PORTRAIT,
                 copy_pages=False):
        
        # outfile_name is set if provided
        if outfile_name:
            self._set_outfile_name(outfile_name)
        else:
            self.outfile_name = None
          
        # Then infile_nameis set, so if outfile_name was not provided we
        # can create it from infile_name
        self._set_infile_name(infile_name)

        # Now initialize a streamConverter
        self.input_stream = open(self.get_infile_name(), 'rb')
        self.output_stream = open(self.get_outfile_name(), 'wb')
        StreamConverter.__init__(self, self.input_stream, self.output_stream,
                                 conversion_type, layout, format, orientation,
                                 copy_pages)

    def __del__(self):
        """
        XXX: documentation
        """
        try:
            self.input_stream.close()
        except IOError:
            # XXX: Do something better
            pass

        try:
            self.output_stream.close()
        except IOError:
            # XXX: Do something better
            pass


    # GETTERS AND SETTERS SECTION
    # ===========================

    def _set_infile_name(self, name):
        self.infile_name = name

        if not self.outfile_name:
            result = re.search("(.+)\.\w*$", name)
            if result:
                self.outfile_name = result.group(1) + '-conv.pdf'
            else:
                self.outfile_name = name + '-conv.pdf'

    def get_infile_name(self):
        return self.infile_name

    def _set_outfile_name(self, name):
        self.outfile_name = name

    def get_outfile_name(self):
        return self.outfile_name

def bookletize_on_stream(input_stream, 
                         output_stream,
                         layout='2x1',
                         output_format='A4',
                         output_orientation='PORTRAIT',
                         copy_pages=False):
    """
    XXX: Doc
    """
    StreamConverter(BOOKLETIZE, layout, format, orientation, copy_pages,
                    input_stream, output_stream()).run()

def bookletize_on_file(input_file, 
                       output_file=None,
                       layout='2x1',
                       format='A4',
                       orientation='PORTRAIT',
                       copy_pages=False):
    """
    XXX: Doc
    """
    FileConverter(input_file, output_file, BOOKLETIZE, layout, format,
                  orientation, copy_pages).run()

def linearize_on_stream(input_stream, 
                        output_stream,
                        layout='2x1',
                        format='A4',
                        orientation='PORTRAIT',
                        copy_pages=False):
    """
    XXX: Doc
    """
    StreamConverter(input_stream, output_stream, LINEARIZE, layout,
                    format, orientation,copy_pages).run()

def linearize_on_file(input_file, 
                      output_file=None,
                      layout='2x1',
                      format='A4',
                      orientation='PORTRAIT',
                      copy_pages=False):
    """
    XXX: Doc
    """
    FileConverter(input_file, output_file, LINEARIZE, layout, format,
                  orientation, copy_pages).run()

def reduce_on_stream(input_stream, 
                     output_stream,
                     layout='2x1',
                     format='A4',
                     orientation='PORTRAIT',
                     copy_pages=False):
    """
    XXX: Doc
    """
    StreamConverter(input_stream, output_stream, REDUCE, layout, format, 
                    orientation, copy_pages).run()

def reduce_on_file(input_file, 
                   output_file=None,
                   layout='2x1',
                   format='A4',
                   orientation='PORTRAIT',
                   copy_pages=False):
    """
    XXX: Doc
    """
    FileConverter(input_file, output_file, REDUCE, layout, format,
                  orientation, copy_pages).run()
