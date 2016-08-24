import contextlib
import functools
import os
import re
import sys
import traceback
import warnings


def only_once(func):
    """Decorator to call the wrapped function only once."""
    res = []
    @functools.wraps(func)
    def _only_once(*args, **kwargs):
        if not res:
            res.append(func(*args, **kwargs))
        return res[0]
    return _only_once


@contextlib.contextmanager
def warn_on_error(extra='', reraise=True, print_exc=False):
    try:
        yield
    except BaseException as e:
        warnings.warn('%s%s: %s' % (
            e.__class__.__name__,
            ' ' + extra if extra else '',
            e
        ))
        if print_exc:
            traceback.print_exc()
        if reraise:
            raise


_called_entry_points = set()
def call_entry_points(cls, force=False, verbose=True):
    
    if not force and cls in _called_entry_points:
        return
    _called_entry_points.add(cls)

    if verbose:
        print >> sys.stderr, '[appinit] calling hooks for %s' % cls

    from . import _vendor
    _vendor.install()
    import pkg_resources
    
    for ep in sorted(pkg_resources.iter_entry_points(cls), key=lambda ep: ep.name):
        with warn_on_error('during entry point %s' % ep, reraise=False, print_exc=True):
            if verbose:
                print >> sys.stderr, '[appinit]    ', ep
            func = ep.load()
            func()


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


def daemonize(chdir='/', umask=0002):

    if os.fork(): # fork, and kill the parent
        os._exit(0)

    # take over the session
    os.setsid()

    if os.fork(): # fork, and kill the parent again; we are finally detached
        os._exit(0)

    if chdir is not None:
        os.chdir(chdir)
    if umask is not None:
        os.umask(umask)
