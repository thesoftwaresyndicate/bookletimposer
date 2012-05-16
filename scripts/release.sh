#!/bin/sh

if [ -z "$1" ] ; then
    echo "usage: $0 [version]"
    exit 1
else
    newversion="$1"
fi
version=$(/bin/grep "version=" setup.py | sed -E "s/^.*version='(.*)',/\1/g")
echo "Updating version number from $version to $newversion"
sed -i -E "s,__version__ = \"$version\",__version__ = \"$newversion\",g" bin/bookletimposer
sed -i -E "s,Version=$version,Version=$newversion,g" data/bookletimposer.desktop
sed -i -E "s,<property name=\"version\">$version</property>,<property name=\"version\">$newversion</property>,g" data/bookletimposer.ui
sed -i -E "s,version='$version',version='$newversion',g" setup.py
sed -i -E "3a $newversion\n\
$(echo $newversion | sed -E 's/./-/g')\n\
\n\
" CHANGELOG
editor CHANGELOG


