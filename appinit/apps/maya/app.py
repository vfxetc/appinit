import glob
import os
import re
import sys

from ..core import BaseApp


class Maya(BaseApp):

    name = 'maya'

    @classmethod
    def iter_installed(cls):
        if sys.platform == 'darwin':
            for path in glob.glob('/Applications/Autodesk/maya20*/Maya.app'):
                app = cls.app_from_path(path)
                if app:
                    yield app
        elif sys.platform == 'linux2':
            for path in glob.glob('/usr/autodesk/maya20*'):
                app = cls.app_from_path(path)
                if app:
                    yield app
        else:
            pass #raise NotImplementedError(sys.platform)

    @classmethod
    def app_from_path(cls, path):
        if sys.platform == 'darwin':
            m = re.match(r'^/Applications/Autodesk/maya(\d{4}(?:\.\d+)?)/Maya.app($|/)', path)
            if m:
                return cls(m.group(0), m.group(1))
        if sys.platform == 'linux2':
            m = re.search(r'maya(\d{4}(?:\.\d+)?)(/|$)', path)
            if m:
                return cls(path, m.group(1))

    @classmethod
    def get_running_app(cls):
        try:
            import maya.cmds
            import maya.utils
        except ImportError:
            return
        return cls.app_from_path(maya.utils.__file__)

    def export(self, environ):
        environ.add('PYTHONPATH', os.path.abspath(os.path.join(
            __file__, '..', 'sandbox'
        )))

    def get_command(self):
        if sys.platform == 'darwin':
            return ['%s/Contents/MacOS/Maya' % self.path]
        elif sys.platform == 'linux2':
            return ['%s/bin/maya%s' % (self.path, self.version)]
        else:
            raise NotImplementedError(sys.platform)

    def get_python(self):
        if sys.platform == 'darwin':
            return '%s/Contents/bin/mayapy' % self.path
        elif sys.platform == 'linux2':
            return '%s/bin/mayapy' % self.path
            raise NotImplementedError(sys.platform)

    def get_site_packages(self):
        if sys.platform == 'darwin':
            return '%s/Contents/Frameworks/Python.framework/Versions/Current/lib/python2.7/site-packages' % self.path
        elif sys.platform.startswith('linux'):
            return '%s/lib/python2.7/site-packages' % self.path



def standalone_initialize():
    """Called during Maya startup to initialize standalone mode."""
    # NOTE: Initializing before the GUI is setup will segfault it, so we have to
    # be a little careful to not do that.
    # OS X Maya.app -> /Applications/Autodesk/maya2015/Maya.app/Contents/MacOS/Maya
    # OS X Python -> /Applications/Autodesk/maya2015/Maya.app/Contents/bin/../Frameworks/Python.framework/Versions/Current/Resources/Python.app/Contents/MacOS/Python
    if os.path.basename(sys.executable).lower().startswith('python'):
        from maya import standalone
        standalone.initialize()

def gui_initialize():
    if not os.path.basename(sys.executable).lower().startswith('python'):
        from ... import init
        init('maya.gui')