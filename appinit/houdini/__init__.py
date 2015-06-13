import re
import subprocess
import os


def _parse_envvars(env_output):
    res = {}
    for line in env_output.splitlines():
        m = re.match(r'^(\w+)=(.*)$', line)
        if m:
            key, value = m.groups()
            res[key] = value
    return res


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
    before = _parse_envvars(raw_before)
    after = _parse_envvars(raw_after)

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

