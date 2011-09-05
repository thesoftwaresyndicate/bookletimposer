#!/usr/bin/env python
# -*- coding: UTF-8 -*-

########################################################################
# 
# BookletImposer - Utility to achieve some basic imposition on PDF documents
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

def debug(msg):
    if __debug__: print msg

def get_sharedir():
    if __debug__ and os.path.exists("data"):
        return "data"
    if os.path.exists(os.path.join("/", "usr", "local", "share",
            "bookletimposer")):
        return os.path.join("/", "usr", "local", "share")
    elif os.path.exists(os.path.join("/", "usr", "share", "bookletimposer")):
        return os.path.join("/", "usr", "share")

def get_datadir():
    return os.path.join(get_sharedir(), "bookletimposer")

def get_pixmapsdir():
    return os.path.join(get_sharedir(), "pixmaps")

def gettext_init():
    gettext.bindtextdomain("bookletimposer", os.path.join(get_datadir(), "locale"))
    gettext.textdomain("bookletimposer")

