import errno
import os
import re
import subprocess
import sys

from ...utils import call_entry_points
from ..core import BaseApp


class Houdini(BaseApp):

    name = 'houdini'

    @classmethod
    def iter_installed(cls):
        if sys.platform == 'darwin':

            framework_dir = '/Library/Frameworks/Houdini.framework/Versions'
            try:
                versions = os.listdir(framework_dir)
            except OSError as e:
                if e.errno == errno.ENOENT:
                    return
                raise

            for version in versions:
                app_path = '/Applications/Houdini %s' % version
                if os.path.exists(app_path):
                    yield cls(app_path, version)
        else:
            pass #raise NotImplementedError(sys.platform)

    @classmethod
    def app_from_path(cls, app):
        if sys.platform == 'darwin':
            m = re.match(r'^/Library/Frameworks/Houdini.framework/Versions/(.+?)($|/)', path)
            if m:
                app_path = '/Applications/Houdini %s' % m.group(1)
                if os.path.exists(app_path):
                    return cls(app_path, m.group(1))

    @classmethod
    def get_running_app(cls):
        try:
            import hou
        except ImportError:
            return
        return cls.app_from_path(hou.__file__)

    def export(self, environ):
        environ.setdefault('HOUDINI_PATH', '&')
        environ.add('HOUDINI_PATH', os.path.abspath(os.path.join(
            __file__, '..', 'sandbox',
        )))

    @property
    def HFS(self):
        if sys.platform == 'darwin':
            return '/Library/Frameworks/Houdini.framework/Versions/%s/Resources' % str(self.version)
        else:
            raise NotImplementedError(sys.platform)

    def get_command(self):
        if sys.platform == 'darwin':
            return ['%s/bin/houdini' % self.HFS, '-foreground']
        else:
            raise NotImplementedError(sys.platform)

    def get_python(self):
        if sys.platform == 'darwin':
            return '%s/bin/hython' % self.HFS
        else:
            raise NotImplementedError(sys.platform)




