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

class ConversionType:
    """The conversion type constants"""
    BOOKLETIZE = 1
    """The conversion from a linear document to a booklet"""
    LINEARIZE = 2
    """The conversion from a booklet to a linear document"""
    REDUCE = 3
    """The conversion from multiple input pages to one output page"""

class PersistentConverter(pypdfconv.FileConverter):
    """
    This class performs conversions on true files.
    """

    XXX: Find a better name

    def __init__(self,
                 infile_name=None,
                 outfile_name=None,
                 conversion_type=ConversionType.BOOKLETIZE,
                 layout='2x1',
                 format='A4',
                 copy_pages=False):
        """
        Create a PersistentConverter.

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
        #Should create the FileConverter if infile_name is set
        FileConverter.__init__(self, infile_name, outfile_name,
                                 conversion_type, layout, format, copy_pages)

    # CONVERSION FUNCTIONS
    # ====================

    def run(self):
        """
        Perform the actual conversion.

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
        """
        Set conversion that will be performed when caling run().

        :Parameters:
          - `type`: A constant from the ConversionType class.
        """
        assert(type == ConversionType.BOOKLETIZE or type == ConversionType.LINEARIZE or type == ConversionType.REDUCE)
        self.__conversion_type = type

    def get_conversion_type(self):
        """
        Get conversion that will be performed when caling run().

        :Returns:
            A constant from ConversionType class.
        """
        return self.__conversion_type

    def set_infile_name(self, name):
        #Should (re)create the converter
