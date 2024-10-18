#!/bin/bash
set -e
PACKAGE=netmap

if [ $# -ne 2 ] ; then
    echo 'Usage:  sh buildRpm <VERSION> <BUILD_NUMBER>'
    exit 0
fi
 
VERSION="$1"
BUILD="$2"

echo "Building netmap version: $VERSION $BUILD"

rm -rf ~/rpmbuild
rpmdev-setuptree

#KERNEL=`uname -r`
KERNEL="5.14.0-427.31.1.el9_4.x86_64"
sed -e 's/@KERNEL_VERSION@/'${KERNEL%.x86_64}'/g'  packaging/netmap.spec > ~/rpmbuild/SPECS/netmap.spec

cd ..
tar czf $PACKAGE-$VERSION.$BUILD.tar.gz ./*
mv $PACKAGE-$VERSION.$BUILD.tar.gz ~/rpmbuild/SOURCES
cd ~/rpmbuild
rpmbuild -v -bb --define="version ${VERSION}" --define="buildnumber {$BUILD}" --target=x86_64 ~/rpmbuild/SPECS/$PACKAGE.spec
