import os
import re
import subprocess
import sys

from ...utils import parse_env_output
from ..core import BaseApp


class Houdini(BaseApp):

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

    def export(self, environ):
        environ.setdefault('HOUDINI_PATH', '&')
        environ.append('HOUDINI_PATH', os.path.dirname(os.path.abspath(__file__)))

    @property
    def HFS(self):
        if sys.platform == 'darwin':
            return '/Library/Frameworks/Houdini.framework/Versions/%s/Resources' % self.version
        else:
            raise NotImplementedError(sys.platform)

    def get_executable(self):
        if sys.platform == 'darwin':
            return '%s/bin/houdini' % self.HFS
        else:
            raise NotImplementedError(sys.platform)

    def get_python(self):
        if sys.platform == 'darwin':
            return '%s/bin/hython' % self.HFS
        else:
            raise NotImplementedError(sys.platform)



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

    diff = {}
    for key, a_value in after.iteritems():
        b_value = before.get(key)
        if b_value is None:
            diff[key] = a_value
            continue
        if a_value != b_value:
            diff[key] = a_value.replace(b_value, '$' + key)

    return diff


if __name__ == '__main__':
    for k, v in sorted(get_envvars().iteritems()):
        print k, v

