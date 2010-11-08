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
# config.py
#
# This file contains the configuration variables defined at install time
# which will be used somewhere in the program.
#
########################################################################

import gettext
import os.path

def get_sharedir():
    if os.path.exists("/usr/local/share/bookletbinder"):
        return "/usr/local/share"
    elif os.path.exists("/usr/share/bookletbinder"):
        return "/usr/share"
    else:
        return "data"

def get_datadir():
    return os.path.join (get_sharedir(), "bookletbinder")

def get_pixmapsdir():
    return os.path.join (get_sharedir(), "pixmaps")

def gettext_init():
    gettext.bindtextdomain("bookletbinder", os.path.join(get_datadir(), "locale"))
    gettext.textdomain("bookletbinder")

