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

. fsbuild/plugin.post.sh
