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
# util/backend.py
#
# This file contains backend should not be part of the python module.
#
########################################################################

import pypdfconv
import os.path

class ConversionType:
    """The conversion type constants"""
    BOOKLETIZE = 1
    """The conversion from a linear document to a booklet"""
    LINEARIZE = 2
    """The conversion from a booklet to a linear document"""
    REDUCE = 3
    """The conversion from multiple input pages to one output page"""

class ConverterPreferences(object):
    def __init__(self):
        self._infile_name = None
        self._conversion_type = None
        self.copy_pages = None
        self.layout = None
        self.paper_format = None
        self.paper_orientation = None
        self.outfile_name = None

    @property
    def infile_name(self):
        return self._infile_name

    @infile_name.setter
    def infile_name(self, value):
        assert value == None or os.path.isfile(value)
        self._infile_name = value

    @property
    def conversion_type(self):
        return self._conversion_type

    @conversion_type.setter
    def conversion_type(self, value):
        assert value == None or \
               value == ConversionType.BOOKLETIZE or \
               value == ConversionType.LINEARIZE or \
               value == ConversionType.REDUCE
        self._conversion_type = value

    @property
    def copy_pages(self):
        return self._copy_pages

    @copy_pages.setter
    def copy_pages(self, value):
        self._copy_pages = bool(value)

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, value):
        # XXX : verify value
        self._layout = value

    @property
    def paper_format(self):
        return self._paper_format

    @paper_format.setter
    def paper_format(self, value):
        # XXX : verify value
        self._paper_format = value

    @property
    def paper_orientation(self):
        return self._paper_orientation

    @paper_orientation.setter
    def paper_orientation(self, value):
        # XXX : verify value
        self._paper_orientation = value

    @property
    def outfile_name(self):
        return self._outfile_name

    @outfile_name.setter
    def outfile_name(self, value):
        assert value == None or os.path.exists(os.path.dirname(value))
        self._outfile_name = value

    def create_converter(self):
        if not self._infile_name:
            # Use a better exception
            raise Exception, "Cannot create converter without an input file"
            return None
        elif self._outfile_name:
            converter = TypedFileConverter(self._infile_name, self._outfile_name)
        else:
            converter = TypedFileConverter(self._infile_name)
        if self._layout: converter.set_layout(self._layout)
        if self._paper_format: converter.set_output_format(self._paper_format)
        if self._paper_orientation:
            converter.set_output_orientation(self._paper_orientation)
        if self._copy_pages: converter.set_copy_pages(self._copy_pages)
        return converter

class TypedFileConverter(pypdfconv.FileConverter):
    """A FileConverter that stores the conversion type.

    """
    def __init__(self,
                 infile_name=None,
                 outfile_name=None,
                 conversion_type=ConversionType.BOOKLETIZE,
                 layout='2x1',
                 format='A4',
                 copy_pages=False):
        """Create a TypedFileConverter.

        :Parameters:
          - `infile_name`: The name to the input PDF file.
          - `outfile_name`: The name of the file where the output PDF
            should de written. If ommited, defaults to the
            name of the input PDF postponded by '-conv'.
          - `conversion_type`: The type of the conversion that will be performed
            when caling run() (see set_converston_type).
          - `layout`: The layout of input pages on one output page (see
            set_layout).
          - `format`: The format of the output paper (see set_output_format).
          - `copy_pages`: Wether the same group of input pages shoud be copied
            to fill the corresponding output page or not (see
            set_copy_pages).
        """
        
        pypdfconv.FileConverter.__init__(self, infile_name, outfile_name,
                                         layout, format, copy_pages)
        self._conversion_type = conversion_type

    # CONVERSION FUNCTIONS
    # ====================

    def run(self):
        """Perform the actual conversion.

        This method launches the actual conversion, using the parameters set
        before.
        """
        if self.get_conversion_type() == ConversionType.BOOKLETIZE:
            self.bookletize()
        elif self.get_conversion_type() == ConversionType.LINEARIZE:
            self.linearize()
        elif self.get_conversion_type() == ConversionType.REDUCE:
            self.reduce()

    # GETTERS AND SETTERS SECTION
    # ===========================

    def set_conversion_type(self, type):
        """Set conversion that will be performed when caling run().

        :Parameters:
          - `type`: A constant from the ConversionType class.
        """
        assert(type == ConversionType.BOOKLETIZE or \
               type == ConversionType.LINEARIZE or \
               type == ConversionType.REDUCE)
        self._conversion_type = type

    def get_conversion_type(self):
        """
        Get conversion that will be performed when caling run().

        :Returns:
            A constant from ConversionType class.
        """
        return self._conversion_type

