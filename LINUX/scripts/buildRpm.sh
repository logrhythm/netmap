#!/bin/bash
set -e
PACKAGE=netmap

if [[ $# -gt 3 || $# -lt 2 ]] ; then
    echo 'Usage:  sh buildRpm <VERSION> <BUILD_NUMBER> <NETMAP-GIT-USER<optional>>'
    exit 0
fi
 
VERSION="$1"
BUILD="$2"

if [ $# -eq 3 ]; then
   USER=$3
else
   USER="LogRhythm"
fi
echo "USER IS $USER";

echo "Building netmap for  USER: $USER, NETMAP VERSION: $VERSION"

PWD=`pwd`
CWD=$PWD/$PACKAGE
DISTDIR=$CWD/dist/$PACKAGE
PATH=$PATH:/usr/local/probe/bin

rm -rf ~/rpmbuild
rpmdev-setuptree

KERNEL=`uname -r`
sed -e 's/@KERNEL_VERSION@/'${KERNEL%.x86_64}'/g'  packaging/netmap.spec > ~/rpmbuild/SPECS/netmap.spec

cd ..
rm -f $PACKAGE-$VERSION*.tar.gz
tar czf $PACKAGE-$VERSION.$BUILD.tar.gz ./*
cp $PACKAGE-$VERSION.$BUILD.tar.gz ~/rpmbuild/SOURCES
cd ~/rpmbuild
rpmbuild -v -bb --define="version ${VERSION}" --define="netmapuser {$USER}" --define="buildnumber {$BUILD}" --target=x86_64 ~/rpmbuild/SPECS/$PACKAGE.spec
