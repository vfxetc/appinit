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
            frameworks = '/Library/Frameworks/Houdini.framework/Versions'
            for version in os.listdir(frameworks):
                app_path = '/Applications/Houdini %s' % version
                if os.path.exists(app_path):
                    yield cls(app_path, version)
        else:
            raise NotImplementedError(sys.platform)

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
        environ.add('HOUDINI_PATH', os.path.dirname(os.path.abspath(__file__)))

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



_idle_funcs = []
def call_once_on_idle(func):
    _idle_funcs.append(func)
    import hou
    hou.ui.addEventLoopCallback(_on_idle)

def _on_idle():
    while _idle_funcs:
        func = _idle_funcs.pop(0)
        func()
    import hou
    hou.ui.removeEventLoopCallback(_on_idle)

def _defer_gui_init():
    call_once_on_idle(lambda: call_entry_points('appinit_houdini_gui_idle'))

