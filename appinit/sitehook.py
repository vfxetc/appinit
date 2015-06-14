import os
import sys


def on_sitehook(appname):

    print '[appinit] sitehook(s) for {!r}:'.format(appname)

    from . import _vendor
    _vendor.install()
    import pkg_resources

    for ep in pkg_resources.iter_entry_points('appinit_{}_sitehook'.format(appname)):
        print '[appinit]     ', ep
        func = ep.load()
        func(appname)
