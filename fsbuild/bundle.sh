#!/bin/sh

set -e

. fsbuild/plugin.pre.sh

PLUGIN_APPIFY=0
PLUGIN_STANDALONE=0
PLUGIN_SKIP_APPIFY=1
PLUGIN_SKIP_STANDALONE=1

echo "Copying data files..."
mkdir -p "$PLUGIN_REALDATADIR"
cp -a Data/* "$PLUGIN_REALDATADIR"

mkdir -p $PLUGIN_READMEDIR
cp README.md $PLUGIN_READMEDIR/ReadMe.txt
unix2dos $PLUGIN_READMEDIR/ReadMe.txt

mkdir -p $PLUGIN_LICENSESDIR
# cp LICENSE $PLUGIN_READMEDIR/Licenses/SDL2.txt
cp -a Licenses/* $PLUGIN_LICENSESDIR/
unix2dos $PLUGIN_LICENSESDIR/*

. fsbuild/plugin.post.sh
