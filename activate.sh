
# This is just a testing ground for us until we figure out all of the import
# logic of the various applications.

here="$(cd "$(dirname "${BASH_SOURCES[0]}")"; pwd)"
export HOUDINI_PATH="${HOUDINI_PATH-&}:$here/appinit/houdini"

# We wish this could be Maya-specific, but it is not.
export PYTHONPATH="$here/appinit/maya/sandbox"
