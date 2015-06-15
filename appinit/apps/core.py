import re


def _iter_entry_points(app_name=None):
    from .. import _vendor
    _vendor.install()
    import pkg_resources
    return pkg_resources.iter_entry_points('appinit_apps', app_name)

def iter_app_classes():
    for ep in _iter_entry_points():
        yield ep.load()


class Version(tuple):

    def __new__(cls, input_):
        if isinstance(input_, basestring):
            str_value = input_
            input_ = map(int, re.split(r'\D', input_))
        elif isinstance(input_, int):
            str_value = str(input_)
            input_ = (input_, )
        else:
            str_value = '.'.join(input_)
        self = super(Version, cls).__new__(cls, input_)
        self._str_value = str_value
        return self

    def __str__(self):
        return self._str_value


class BaseApp(object):

    name = '????'

    @classmethod
    def iter_installed(cls):
        return iter(())

    @classmethod
    def get_running_app(cls):
        pass

    def __init__(self, path=None, version=None):
        self.path = path
        self.version = Version(version)

    def get_envvars(self):
        return {}
    
    def get_python(self):
        return None

    def get_site_packages(self):
        pass
    
    def get_command(self):
        raise NotImplementedError()


class AppSelector(object):

    def __init__(self, spec):
        if spec is None:
            self.name = self.operation = self.version = None
        else:
            m = re.match(r'^(\w+)(?:(==)([\w.]+))?$', spec)
            if not m:
                raise ValueError('invalid app spec %r' % spec)
            self.name, self.operation, version = m.groups()
            self.version = Version(version) if version else None

    def iter_installed(self):
        for cls_ep in _iter_entry_points(self.name):
            cls = cls_ep.load()
            for app in cls.iter_installed():
                if self.version is None:
                    yield app
                elif self.operator == '==' and self.version == app.version:
                    yield app
                else:
                    # Arguably this should be in the constructor, but this is
                    # more certain to catch errors.
                    raise ValueError('unknown version operator %s' % self.operator)


def iter_installed_apps(selectors=None):
    selectors = selectors or None
    if not isinstance(selectors, (list, tuple)):
        selectors = [selectors]
    for selector in selectors:
        if isinstance(selector, BaseApp):
            yield selector
            continue
        selector = AppSelector(selector)
        for app in selector.iter_installed():
            yield app

