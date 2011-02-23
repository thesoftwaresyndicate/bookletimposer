#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup, Extension
from DistUtilsExtra.command import *

import glob
import re
import os.path
import distutils.cmd

class build_uiheaders(distutils.cmd.Command):
    description = "generate the headers required to use gettext whit gtkbuilder"
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        for uifile in glob.glob(os.path.join('data', '*.ui')):
            #XXX: do not write files outside of the build directory
            self.spawn (["intltool-extract",
                         "--type=gettext/glade",
                         uifile])

class build_man(distutils.cmd.Command):
    description = 'build man page from t2t'
    user_options= [
        ('build-dir=', 'd', "directory to build to"),
        ('man-sources=', None, 'list of man sources in the source tree')
        ]

    def initialize_options(self):
        self.build_dir = None
        self.man_sources = None
        self.build_base = None

    def finalize_options(self):
        self.set_undefined_options('build', ('build_base', 'build_base'))
        if self.build_dir is None:
            self.build_dir=os.path.join(self.build_base, 'man')
        if self.man_sources is None:
            self.man_sources = glob.glob('doc/*.1.t2t')

    def create_manbuilddir(self):
        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)

    def get_manpage_name(self, mansource):
        return re.sub('.t2t$', '', os.path.basename(mansource))

    def get_manpage_path(self, mansource):
        return os.path.join(self.build_dir, self.get_manpage_name(mansource))

    def build_manpage(self, mansource_path):
        manpage_path = self.get_manpage_path(mansource_path)
        self.spawn(['txt2tags', '-o', manpage_path, mansource_path])
        return manpage_path

    def run(self):
        self.announce('Building manpages...')
        self.create_manbuilddir()
        manpages_data = []
        for man_source in self.man_sources:
            manpage_name = self.get_manpage_name(man_source)
            manpage_path = self.build_manpage(man_source)
            section = manpage_name[-1:]
            installed_path = os.path.join('man', 'man%s' % section)
            manpages_data.append((installed_path, [manpage_path]))
        data_files = self.distribution.data_files
        data_files.extend(manpages_data)

class clean_man(distutils.command.clean.clean):
    description = "clean up files generated by build_man"
    def run(self):
        self.build_dir = os.path.join("build", "man")
        if os.path.isdir(self.build_dir):
            remove_tree(self.build_dir)
        distutils.command.clean.clean.run(self)

build_extra.build_extra.sub_commands.insert(0, ("build_uiheaders", None))
build_extra.build_extra.sub_commands.append(("build_man", None))

setup(name='bookletimposer',
      version='0.1~beta1',
      url="http://kjo.herbesfolles.org/bookletimposer/",
      author="Kjö Hansi Glaz",
      author_email="kjo@a4nancy.net.eu.org",
      packages=['bookletimposer',],
      py_modules=['pdfimposer'],
      package_dir={'': 'lib'},
      scripts=['bin/bookletimposer',],
      data_files=[
                  ('share/bookletimposer', ["data/bookletimposer.ui"]),
                  ('share/pixmaps', ['data/bookletimposer.svg']),
                  ('share/applications', ['data/bookletimposer.desktop']),
                  ('share/doc/bookletimposer', ['README']),
                  ],
      requires = ['gtk', 'pyPdf (>0.12)'],
      cmdclass = { "build" : build_extra.build_extra,
                   "build_uiheaders" :  build_uiheaders,
                   "build_i18n" :  build_i18n.build_i18n,
                   "build_help" :  build_help.build_help,
                   "build_icons" :  build_icons.build_icons,
                   "build_man" :  build_man}
      )
