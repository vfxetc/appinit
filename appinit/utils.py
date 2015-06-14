import re


def parse_env_output(env_output):
    res = {}
    for line in env_output.splitlines():
        m = re.match(r'^(\w+)=(.*)$', line)
        if m:
            key, value = m.groups()
            res[key] = value
    return res
