import warnings

from .utils import call_entry_points


def init(name):
    name_parts = name.split('.')
    for i in xrange(len(name_parts) + 1):
        ep_parts = ['appinit'] + name_parts[:i]
        call_entry_points('.'.join(ep_parts))


def sitehook():
    from .apps.core import iter_app_classes
    for cls in iter_app_classes():
        app = cls.get_running_app()
        if app:
            init(app.name)
            return

