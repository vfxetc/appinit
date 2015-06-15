import warnings

from .utils import call_entry_points


def init(ep_name):
    call_entry_points('appinit_%s' % ep_name)


def sitehook():
    from .apps.core import iter_app_classes
    for cls in iter_app_classes():
        app = cls.get_running_app()
        if app:
            init(app.name)
            return

