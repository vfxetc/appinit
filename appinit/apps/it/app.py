import glob
import os
import re
import sys

from ..core import BaseApp


class IT(BaseApp):

    name = 'it'

    @classmethod
    def iter_installed(cls):
        if sys.platform == 'darwin':
            for path in glob.glob('/Applications/Pixar/RenderManStudio-*/bin/it.app'):
                app = cls.app_from_path(path)
                if app:
                    yield app
        else:
            pass #raise NotImplementedError(sys.platform)

    @classmethod
    def app_from_path(cls, path):
        if sys.platform == 'darwin':
            m = re.match(r'^/Applications/Pixar/RenderManStudio-(.+?)/bin/it\.app', path)
            if m:
                return cls(m.group(0), m.group(1))

    @classmethod
    def get_running_app(cls):
        if os.path.basename(sys.executable) == 'it':
            return cls.app_from_path(sys.executable)

    def export(self, environ):
        environ.add('RMS_SCRIPT_PATHS', os.path.abspath(os.path.join(
            __file__, '..', 'sandbox'
        )))

    def get_command(self):
        if sys.platform == 'darwin':
            return ['%s/Contents/MacOS/it' % self.path]
        else:
            raise NotImplementedError(sys.platform)

    def get_python(self):
        pass

    def get_site_packages(self):
        if sys.platform == 'darwin':
            # app:           /Applications/Pixar/RenderManStudio-19.0-maya2015/bin/it.app/Contents/MacOS/it
            # site-packages: /Applications/Pixar/RenderManStudio-19.0-maya2015/lib/python2.7/site-packages
            return os.path.abspath(os.path.join(self.path, '..', '..', 'lib', 'python2.7', 'site-packages'))

