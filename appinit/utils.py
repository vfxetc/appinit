import re


def parse_env_output(env_output):
    res = {}
    for line in env_output.splitlines():
        m = re.match(r'^(\w+)=(.*)$', line)
        if m:
            key, value = m.groups()
            res[key] = value
    return res


def diff_envvars(before, after, reduce=True):
    diff = {}
    for key, a_value in after.iteritems():
        b_value = before.get(key)
        if b_value is None:
            diff[key] = a_value
            continue
        if a_value != b_value:
            diff[key] = a_value.replace(b_value, '$' + key) if reduce else a_value
    return diff
