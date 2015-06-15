import glob
import os
import re
import sys

from ..core import BaseApp


class Mari(BaseApp):

    name = 'mari'

    @classmethod
    def iter_installed(cls):
        if sys.platform == 'darwin':
            for path in glob.glob('/Applications/Mari*'):
                app = cls.app_from_path(path)
                if app:
                    yield app
        else:
            raise NotImplementedError(sys.platform)

    @classmethod
    def app_from_path(cls, path):
        if sys.platform == 'darwin':
            m = re.match(r'^/Applications/Mari([\dv.]+)($|/)', path)
            if m:
                return cls(m.group(0), m.group(1))

    @classmethod
    def get_running_app(cls):
        try:
            import Marixxx.cmds
        except ImportError:
            return
        return cls.app_from_path(Mari.utils.__file__)

    def export(self, environ):
        environ.add('MARI_SCRIPT_PATH', os.path.abspath(os.path.join(
            __file__, '..', 'sandbox'
        )))

    def get_command(self):
        if sys.platform == 'darwin':
            return ['%s/Contents/MacOS/Mari%s' % (self.path, self.version)]
        else:
            raise NotImplementedError(sys.platform)

    def get_python(self):
        if sys.platform == 'darwin':
            return '%s/Contents/MacOS/python' % self.path
        else:
            raise NotImplementedError(sys.platform)

    def get_site_packages(self):
        if sys.platform == 'darwin':
            return '%s/Contents/Frameworks/Python.framework/Versions/Current/lib/python2.7/site-packages' % self.path



def standalone_initialize():
    """Called during Mari startup to initialize standalone mode."""
    # NOTE: Initializing before the GUI is setup will segfault it, so we have to
    # be a little careful to not do that.
    # OS X Mari.app -> /Applications/Autodesk/Mari2015/Mari.app/Contents/MacOS/Mari
    # OS X Python -> /Applications/Autodesk/Mari2015/Mari.app/Contents/bin/../Frameworks/Python.framework/Versions/Current/Resources/Python.app/Contents/MacOS/Python
    if os.path.basename(sys.executable).lower().startswith('python'):
        from Mari import standalone
        standalone.initialize()
