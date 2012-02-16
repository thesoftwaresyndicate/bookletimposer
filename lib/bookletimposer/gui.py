#!/usr/bin/env python
# -*- coding: UTF-8 -*-

########################################################################
# 
# PdfImposer - Utility to convert PDF files between diffrents page layouts
# Copyright (C) 2008-2011 Kjö Hansi Glaz <kjo@a4nancy.net.eu.org>
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
# gui.py
#
# This file contains the GTK+ graphic utility.
#
########################################################################

import pygtk
pygtk.require('2.0')
import gtk
import glib
import gobject # >= 2.16 !
gtk.gdk.threads_init()
import gio

import os.path
import threading
import traceback
import gettext

import backend
import pdfimposer
import config
from config import debug

config.gettext_init()
_ = gettext.gettext

class UserInterrupt(backend.BookletImposerError):
    """Exception raised when the user interrupted the conversion

    """
    # XXX: this is probably not the right way to do...

class BookletImposerUI(object):
    """
    
    """
    
    def __init__(self, preferences=None):
        """
        
        """
        if preferences:
            self.__preferences = preferences
        else:
            self.__preferences = backend.ConverterPreferences()
        self.__create_gui()
        if preferences:
            self.__apply_preferences()
        self.__main_window.show()

    def __create_gui(self):
        builder = gtk.Builder()
        builder.add_from_file(os.path.join(config.get_datadir(), "bookletimposer.ui"))
        builder.connect_signals(self)

        self.__main_window = builder.get_object("main_window")
        self.__input_file_chooser_button = \
            builder.get_object("input_file_chooser_button")
        self.__bookeltize_radiobutton = builder.get_object("bookletize_radiobutton")
        self.__linearize_radiobutton = builder.get_object("linearize_radiobutton")
        self.__reduce_radiobutton =  builder.get_object("reduce_radiobutton")
        self.__copy_pages_radiobutton = builder.get_object("copy_pages_radiobutton")
        self.__layout_combobox = builder.get_object("layout_combobox")
        self.__paper_format_combobox = \
            builder.get_object("output_paper_format_combobox")
        self.__output_file_chooser_button = self.__create_output_file_chooser_button(builder)
        self.__about_button = builder.get_object("about_button")
        self.__help_button = builder.get_object("help_button")
        self.__close_button = builder.get_object("close_button")
        self.__apply_button = builder.get_object("apply_button")

        self.__about_dialog = builder.get_object("about_dialog")

        self.__progress_dialog = builder.get_object("progress_dialog")
        self.__label_conversion_title = builder.get_object("conversion_title_label")
        self.__progressbar_conversion = builder.get_object("conversion_progressbar")
        self.__label_conversion_setp = builder.get_object("conversion_step_label")

        self.__try_set_icon(self.__main_window, "bookletimposer.svg")
        self.__fill_paper_formats()
        self.__fill_layouts()

    def __create_output_file_chooser_button(self, builder):
        # Emulate a FileChooserButton for saving
        output_file_chooser_button = \
            builder.get_object("output_file_chooser_button")
        output_file_chooser_button.__filename = None

        def output_file_chooser_button_set_filename(filename):
            output_file_chooser_button.__filename = filename
            output_file_chooser_file_image = \
                builder.get_object("output_file_chooser_file_image")
            output_file_chooser_label = \
                builder.get_object("output_file_chooser_label")
            output_file_chooser_label.set_text(os.path.basename(filename))
            output_file_chooser_file_image.set_visible(True)
        output_file_chooser_button.set_filename = \
            output_file_chooser_button_set_filename

        def output_file_chooser_button_get_filename():
            return self.__output_file_chooser_button.__filename
        output_file_chooser_button.get_filename = \
            output_file_chooser_button_get_filename

        return output_file_chooser_button

    @staticmethod
    def __try_set_icon(widget, icon):
        try:
            widget.set_icon_from_file(os.path.join(config.get_pixmapsdir(), icon))
        except glib.GError:
            debug("Icon not found")

    @staticmethod
    def set_liststore_for_combobox(combobox):
        liststore = gtk.ListStore(gobject.TYPE_STRING)
        combobox.set_model(liststore)
        cell = gtk.CellRendererText()
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, 'text', 0)
        return liststore

    def __fill_paper_formats(self):
        liststore = self.set_liststore_for_combobox(
            self.__paper_format_combobox)
        formats = pdfimposer.AbstractConverter.page_formats.keys()
        formats.sort()
        for format in formats:
            liststore.append([format])
        self.__paper_format_combobox.set_active(1)

    def __fill_layouts(self):
        liststore = self.set_liststore_for_combobox(
            self.__layout_combobox)
        for layout in ["2x1", "2x2", "2x4", "4x4"]:
            liststore.append([layout])
        self.__layout_combobox.set_active(0)

    @staticmethod
    def combobox_select_row(widget, row_value):
        def func(model, path, iter, widget):
            if model.get_value(iter, 0) == row_value:
                widget.set_active_iter(iter)
        widget.get_model().foreach(func, widget)

    def __apply_preferences(self):
        preferences = self.__preferences
        if preferences.infile_name:
            self.__input_file_chooser_button.set_filename(preferences.infile_name)
            self.__apply_button.set_sensitive(True)
        if preferences.conversion_type:
            if  preferences.conversion_type == backend.ConversionType.BOOKLETIZE:
                self.__bookeltize_radiobutton.set_active(True)
            if  preferences.conversion_type == backend.ConversionType.LINEARIZE:
                self.__linearize_radiobutton.set_active(True)
            if  preferences.conversion_type == backend.ConversionType.REDUCE:
                self.__reduce_radiobutton.set_active(True)
        if preferences.copy_pages:
            self.__copy_pages_radiobutton.set_active(preferences.copy_pages)
        if preferences.layout:
            self.combobox_select_row(self.__layout_combobox, preferences.layout)
        if preferences.paper_format:
            self.combobox_select_row(self.__paper_format_combobox,
                                     preferences.paper_format)
        if preferences.outfile_name:
            self.__output_file_chooser_button.set_filename(preferences.outfile_name)

    # CALLBACKS

    def cb_close_main_window(self, widget, event, data=None):
        self.close_application()

    def cb_dialog_close(self, dialog, data=None):
        dialog.hide()

    def cb_infile_set(self, widget, data=None):
        self.__preferences.infile_name = widget.get_filename()
        self.__apply_preferences()
        self.__apply_button.set_sensitive(True)

    def cb_bookletize_toggled(self, widget, data=None):
        if widget.get_active():
            self.__preferences.conversion_type = backend.ConversionType.BOOKLETIZE

    def cb_linearize_toggled(self, widget, data=None):
        if widget.get_active():
            self.__preferences.conversion_type = backend.ConversionType.LINEARIZE

    def cb_reduce_toggled(self, widget, data=None):
        if widget.get_active():
            self.__preferences.conversion_type = backend.ConversionType.REDUCE

    def cb_copy_pages_toggled(self, widget, data=None):
        self.__preferences.copy_pages = widget.get_active()

    def cb_layout_changed(self, widget, data=None):
        self.__preferences.layout = widget.get_model().get_value(
            widget.get_active_iter(), 0)

    def cb_paper_format_changed(self, widget, data=None):
        self.__preferences.paper_format = widget.get_model().get_value(
            widget.get_active_iter(), 0)

    def cb_outfile_clicked(self, widget, data=None):
        fcdialog = gtk.FileChooserDialog(
            title=_("Choose file to save"),
            parent=self.__main_window,
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                     gtk.STOCK_OK, gtk.RESPONSE_OK))
        if widget.get_filename():
            fcdialog.set_filename(widget.get_filename())
        if fcdialog.run() == gtk.RESPONSE_OK:
            if fcdialog.get_filename():
                widget.set_filename(fcdialog.get_filename())
                self.__preferences.outfile_name = fcdialog.get_filename()
        fcdialog.destroy()

    def cb_about_button(self, widget, data=None):
        self.show_about_dialog()

    def cb_close_button(self, widget, data=None):
        self.close_application()
    
    def cb_help_button(self, widget, data=None):
        uri = "ghelp:bookletimposer"
        try:
            gtk.show_uri(screen = None, uri = uri,
                timestamp = gtk.get_current_event_time())
        except gio.Error, error:
            dialog = gtk.MessageDialog(parent=self.__main_window,
                                       flags=gtk.DIALOG_MODAL,
                                       type=gtk.MESSAGE_ERROR,
                                       buttons=gtk.BUTTONS_CLOSE,
                                       message_format=_("Unable to display help: %s")
                                                      % str(error))
            dialog.connect("response", lambda widget, data=None: widget.destroy())
            dialog.run()

    def cb_apply_button(self, widget, data=None):
        self.run_conversion()
        pass

    def cb_progress_stop(self, widget, data=None):
        debug("Stop triggered")
        self.__stop.set()
        self.__label_conversion_setp.set_text(_("Cancel triggered, please wait..."))

    # ACTIONS
    
    def close_application(self):
        gtk.main_quit()

    def show_about_dialog(self):
        self.__about_dialog.show()

    def run_conversion(self):

        def exception_dialog(exception):
            dialog = gtk.MessageDialog(parent=self.__main_window,
                                       flags=gtk.DIALOG_MODAL,
                                       type=gtk.MESSAGE_ERROR,
                                       buttons=gtk.BUTTONS_CLOSE,
                                       message_format=_("Conversion failed"))
            dialog.format_secondary_text(str(exception))

            def cb_close_dialog(widget, data=None):
                widget.destroy()
                self.__progress_dialog.hide()
                self.__main_window.set_sensitive(True)
                return False
            dialog.connect("response", cb_close_dialog)
            dialog.show()
        try:
            converter = self.__preferences.create_converter()
        except Exception, e:
            exception_dialog(e)
            raise

        def cb_update_progress(message, progress):
            # there we are inside the work of the converter,
            # so we can to stop it if the user required to cancel
            # the operation. To achieve that we raise an exception.
            # XXX: that's not elegant at all
            if self.__stop.is_set():
                debug("Stop catched")
                raise UserInterrupt()
            gtk.gdk.threads_enter()
            self.__progressbar_conversion.set_fraction(progress)
            self.__label_conversion_setp.set_text(message)
            gtk.gdk.threads_leave()

        def cb_process_exception(exception):
            gtk.gdk.threads_enter()
            exception_dialog(exception)
            gtk.gdk.threads_leave()
            print traceback.format_exc()

        def cb_interrupt_callback():
            self.__progress_dialog.hide()
            self.__main_window.set_sensitive(True)

        def worker(exception_callback, interrupt_callback):
            try:
                converter.run()
            except UserInterrupt:
                interrupt_callback()
            except Exception, e:
                exception_callback(e)
                raise
            gtk.gdk.threads_enter()
            self.__progress_dialog.hide()
            gtk.gdk.threads_leave()

        self.__main_window.set_sensitive(False)
        self.__label_conversion_title.set_text(_("Converting %s") %
            self.__preferences.infile_name)
        self.__progressbar_conversion.set_fraction(0)
        self.__label_conversion_setp.set_text("")
        self.__progress_dialog.show()
        try:
            converter = self.__preferences.create_converter()
        except Exception, e:
            exception_dialog(e)
            raise
        converter.set_progress_callback(cb_update_progress)
        self.__stop = threading.Event()
        converter_thread = threading.Thread(target=worker,
            args=[cb_process_exception, cb_interrupt_callback])
        converter_thread.start()
        self.__main_window.set_sensitive(True)

if __name__ == "__main__":
    ui = BookletImposerUI()
    gtk.main()
