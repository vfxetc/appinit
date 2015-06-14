import glob
import os
import re
import sys

from ..core import BaseApp


class Maya(BaseApp):

    @classmethod
    def iter_installed(cls):
        if sys.platform == 'darwin':
            for path in glob.glob('/Applications/Autodesk/maya20*/Maya.app'):
                m = re.search(r'/maya(20\d{2})/', path)
                version = int(m.group(1))
                yield cls(path, version)



def on_sitehook(appname):
    
    # NOTE: Initializing before the GUI is setup will segfault it, so we have to
    # be a little careful to not do that.
    # OS X Maya.app -> /Applications/Autodesk/maya2015/Maya.app/Contents/MacOS/Maya
    # OS X Python -> /Applications/Autodesk/maya2015/Maya.app/Contents/bin/../Frameworks/Python.framework/Versions/Current/Resources/Python.app/Contents/MacOS/Python
    if os.path.basename(sys.executable).lower().startswith('python'):
        from maya import standalone
        standalone.initialize()
