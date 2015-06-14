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
        else:
            raise NotImplementedError(sys.platform)

    def export(self, environ):
        environ.append('PYTHONPATH', os.path.abspath(os.path.join(
            __file__, '..', 'sandbox'
        )))

    def get_executable(self):
        if sys.platform == 'darwin':
            return '%s/Contents/MacOS/Maya' % self.path
        else:
            raise NotImplementedError(sys.platform)

    def get_python(self):
        if sys.platform == 'darwin':
            return '%s/Contents/bin/mayapy' % self.path
        else:
            raise NotImplementedError(sys.platform)

    def get_site_packages(self):
        if sys.platform == 'darwin':
            return '%s/Contents/Frameworks/Python.framework/Versions/Current/lib/python2.7/site-packages' % self.path




def standalone_initialize(appname):
    """Called during Maya startup to initialize standalone mode."""
    # NOTE: Initializing before the GUI is setup will segfault it, so we have to
    # be a little careful to not do that.
    # OS X Maya.app -> /Applications/Autodesk/maya2015/Maya.app/Contents/MacOS/Maya
    # OS X Python -> /Applications/Autodesk/maya2015/Maya.app/Contents/bin/../Frameworks/Python.framework/Versions/Current/Resources/Python.app/Contents/MacOS/Python
    if os.path.basename(sys.executable).lower().startswith('python'):
        from maya import standalone
        standalone.initialize()
