import warnings


_inited = False

def init(app_name):

    global _inited
    if _inited:
        return
    _inited = True # don't want for it to complete; only allow to error once

    print '[appinit] calling hooks for %s:' % app_name

    from . import _vendor
    _vendor.install()
    import pkg_resources

    entrypoints = list(pkg_resources.iter_entry_points('appinit_{}'.format(app_name)))
    entrypoints.sort(key=str)

    for ep in entrypoints:
        print '[appinit]    ', ep
        try:
            func = ep.load()
            func(app_name)
        except Exception as e:
            warnings.warn('[appinit] %s during %s: %s' % (
                e.__class__.__name__,
                ep,
                e
            ))

