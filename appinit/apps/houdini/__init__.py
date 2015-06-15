import os
import re
import subprocess
import sys

from ...utils import parse_env_output, call_entry_points
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


def get_envvars():
    """Get the difference in environment that the houdini_setup script provides."""

    # TODO: Move to function which finds resources given a version.
    resources_dir = '/Library/Frameworks/Houdini.framework/Versions/Current/Resources'
    
    # It might be cleaner to write something other than `env` which we are
    # effortlessly able to perfectly interpret, but the chances of something
    # effecting the envvars in play in a manner that breaks our parsing AND
    # is still valid is vanishingly small.

    delimiter = os.urandom(8).encode('hex')
    proc = subprocess.Popen(['bash', '-c', '''
        env
        echo {0}
        source houdini_setup_bash -q
        echo {0}
        env
    '''.format(delimiter)], cwd=resources_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = proc.communicate()
    raw_before, _, raw_after = out.split(delimiter)
    before = parse_env_output(raw_before)
    after = parse_env_output(raw_after)


    return diff_envvars(before, after)


if __name__ == '__main__':
    for k, v in sorted(get_envvars().iteritems()):
        print k, v

