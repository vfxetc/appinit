import subprocess
import collections

from . import utils


class Mixin(object):

    def __init__(self, *args, **kwargs):
        super(Mixin, self).__init__(*args, **kwargs)
        self._original = self.copy()

    def add(self, key, value):
        try:
            existing = self[key]
            if value not in existing.split(':'):
                self[key] = '%s:%s' % (existing, value)
        except KeyError:
            self[key] = value

    def append(self, key, value):
        try:
            self[key] = '%s:%s' % (self[key], value)
        except KeyError:
            self[key] = value
    
    def prepend(self, key, value):
        try:
            self[key] = '%s:%s' % (value, self[key])
        except KeyError:
            self[key] = value

    def remove(self, name, value, strict=True):
        existing = self.get(name, None)
        if not existing:
            raise KeyError(name)
        before = existing.split(':')
        after = [x for x in before if x != value]
        if before == after:
            if strict:
                raise ValueError(value)
            return 0
        self[name] = ':'.join(after)
        return len(before) - len(after)

    def get_diff(self, reduce=True):
        return utils.diff_envvars(self._original, self, reduce=reduce)


class Environ(Mixin, dict):
    pass


class UserDict(collections.MutableMapping):

    def __init__(self, data=None):
        super(UserDict, self).__init__()
        self._data = dict(data or {})

    def __getitem__(self, key):
        return self._data[key]
    def __setitem__(self, key, value):
        self._data[key] = value
    def __delitem__(self, key):
        del self._data[key]
    def __iter__(self):
        return iter(self._data)
    def __len__(self):
        return len(self._data)
    
    def copy(self):
        return self._data.copy()


class LaunchctlEnviron(Mixin, UserDict):

    def __getitem__(self, key):
        try:
            return super(LaunchctlEnviron, self).__getitem__(key)
        except KeyError:
            out = subprocess.check_output(['launchctl', 'getenv', key]).strip()
            if out:
                self[key] = out
                return out
            raise


if __name__ == '__main__':
    x = LaunchctlEnviron()
    print 'PYTHONPATH' in x
    print x['PYTHONPATH']
