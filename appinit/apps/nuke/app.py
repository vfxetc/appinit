import glob
import os
import re
import sys

from ..core import BaseApp


class Nuke(BaseApp):

    name = 'nuke'

    @classmethod
    def iter_installed(cls):
        if sys.platform == 'darwin':
            for path in glob.glob('/Applications/Nuke*/Nuke*.app'):
                app = cls.app_from_path(path)
                if app:
                    yield app
        else:
            pass #raise NotImplementedError(sys.platform)

    @classmethod
    def app_from_path(cls, path):
        if sys.platform == 'darwin':
            m = re.match(r'^/Applications/Nuke([\dv.]+)/Nuke\1.app($|/)', path)
            if m:
                return cls(m.group(0), m.group(1))

    @classmethod
    def get_running_app(cls):
        try:
            import nukexxx.cmds
        except ImportError:
            return
        return cls.app_from_path(Nuke.utils.__file__)

    def export(self, environ):
        environ.add('NUKE_PATH', os.path.abspath(os.path.join(
            __file__, '..', 'sandbox'
        )))

    def get_command(self):
        if sys.platform == 'darwin':
            return ['%s/Contents/MacOS/Nuke%s' % (self.path, self.version)]
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
    """Called during Nuke startup to initialize standalone mode."""
    # NOTE: Initializing before the GUI is setup will segfault it, so we have to
    # be a little careful to not do that.
    # OS X Nuke.app -> /Applications/Autodesk/Nuke2015/Nuke.app/Contents/MacOS/Nuke
    # OS X Python -> /Applications/Autodesk/Nuke2015/Nuke.app/Contents/bin/../Frameworks/Python.framework/Versions/Current/Resources/Python.app/Contents/MacOS/Python
    if os.path.basename(sys.executable).lower().startswith('python'):
        from Nuke import standalone
        standalone.initialize()
