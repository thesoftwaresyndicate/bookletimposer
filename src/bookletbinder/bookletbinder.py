#!/usr/bin/env python
# -*- coding: UTF-8 -*-

########################################################################
# 
# PyPdfConv - Utility to convert PDF files between diffrents page layouts
# Copyright (C) 2008-2010 Kjö Hansi Glaz <kjo AT a4nancy DOT net DOT eu DOT org>
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
# bookletbinder/booketbinder.py
#
# This file is the main program of bookletbinder
#
# It contains the CLI frontend of bookletbinder, which can either work
# standalone or launch the GTK2+ frontend.
#
########################################################################

import optparse
import gettext

# XXX: use normal imports
from gui import *
from backend import *
import config

config.gettext_init()
_ = gettext.gettext

# XXX
VERSION = "0.01"

def main():
    """
    This is the function that launches the program
    """
    
    infiles = [""]
    
    parser = optparse.OptionParser(
        usage="%prog [options] [infile [infile2] ...]",
        version="%prog " + VERSION)
    parser.add_option ("-o", "--output", dest="outfile",
        help=_("output PDF file"))
    parser.add_option ("-a", "--no-gui", 
        action="store_false", dest="gui",
        default=True,
        help=_("automatic converstion (don't show the user interface). At least input file must be defined"))
    parser.add_option ("-i", "--gui", 
        action="store_true", dest="gui",
        default=True,
        help=_("shows the user interface (default)."))
    parser.add_option ("-b", "--booklet",
        action="store_const", dest="conv_type", 
        const=backend.ConversionType.BOOKLETIZE, default=backend.ConversionType.REDUCE,
        help=_("makes a booklet"))
    parser.add_option ("-l", "--linearize",
        action="store_const", dest="conv_type", 
        const=backend.ConversionType.LINEARIZE, default=backend.ConversionType.REDUCE,
        help=_("convert a booklet to single pages"))
    parser.add_option ("-n", "--no-reorganisation",
        action="store_const", dest="conv_type", 
        const=backend.ConversionType.REDUCE, default=backend.ConversionType.REDUCE,
        help=_("don't do any reorganisation (will only scale and assemble pages)"))
    parser.add_option ("-c", "--copy-pages",
        action="store_true", dest="copy_pages",
        default=False,
        help=_("Copy the same group of input pages on one output page"))
    parser.add_option ("-p", "--pages-per-sheet", 
        dest="pages_per_sheet", 
        default="2x1", 
        help=_("number of pages per sheet, in the format HORIZONTALxVERTICAL, e.g. 2x1"))
    parser.add_option ("-f", "--format", 
        dest="output_format", 
        default=None,
        help=_("output page format, e.g. A4 or A3R"))
    
    (options, args) = parser.parse_args()
    
    if len(args) >= 1:
        infiles = args
    
    preferences = backend.ConverterPreferences()
        
    if infiles[0]:
        preferences.infile_name = infiles[0]
    if options.outfile:
        preferences.outfile_name = options.outfile
    if options.conv_type:
        preferences.conversion_type = options.conv_type
    if options.output_format:
        preferences.outfile_format = options.output_format
    if options.pages_per_sheet:
        preferences.layout = options.pages_per_sheet
    if options.copy_pages:
        preferences.copy_pages = True
    
    if options.gui:
        ui = BookletBinderUI(preferences)
        gtk.main()
    else:
        converter = preferences.create_converter()
        def progress_callback(message, progress):
            print(_("%i %%: %s") % (progress*100, message))
        converter.set_progress_callback(progress_callback)
        converter.run()
    return 0 
    
if __name__ == "__main__":
    # Import Psyco if available
    try:
        import psyco
        print _("psyco imported. Bookletbinder will run faster.")
        psyco.full()
    except ImportError:
        print _("psyco not found. You can speed Bookletbinder up by installing it.")
    main()
