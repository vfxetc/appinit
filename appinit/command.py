import argparse
import os
import sys
import subprocess

from . import utils
from .apps.core import iter_installed_apps
from .environ import LaunchctlEnviron, Environ


def get_environ(apps, base=None, cls=None):
    environ = (cls or Environ)(base or {})
    for app in iter_installed_apps(apps):
        app.export(environ)
    environ.add('PYTHONPATH', os.path.abspath(os.path.join(
        __file__, '..', '..',
    )))
    return environ


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='commands')


def argument(*args, **kwargs):
    return args, kwargs

def command(*args, **kwargs):
    def _decorator(func):

        func.__parse_known_args = kwargs.pop('parse_known_args', False)
        name = kwargs.pop('name', func.__name__)
        name = name.replace('_', '-').replace('--', '_')
        defaults = kwargs.pop('defaults', {}).copy()
        defaults.setdefault('_func', func)
        parser = subparsers.add_parser(name, **kwargs)
        parser.set_defaults(**defaults)

        for arg_args, arg_kwargs in args:
            parser.add_argument(*arg_args, **arg_kwargs)

        return func

    return _decorator


@command(
    argument('apps', nargs='*'),
    help='print installed versions of given app',
)
def list(args):
    for app in iter_installed_apps(args.apps):
        print '%s==%s' % (app.name, app.version)


@command(
    argument('app'),
    help='print executable of given app',
)
def which(args):
    app = next(iter_installed_apps(args.app), None)
    if not app:
        return 1
    print app.get_command()[0]


@command(
    argument('apps', nargs='*'),
    help='print shell script for creating environment',
)
def export(args):
    environ = get_environ(args.apps)
    for k, v in sorted(environ.get_diff(reduce=True).iteritems()):
        print 'export %s="%s"' % (k, v)


@command(
    argument('-c', '--clean', action='store_true'),
    argument('-U', '--uninstall', action='store_true'),
    argument('-n', '--dry-run', action='store_true'),
    argument('apps', nargs='*'),
    help='set envvars in OS X launchctl for entire login session')
def hook_launchctl(args):
    environ = get_environ(args.apps, base={}, cls=None if args.clean else LaunchctlEnviron)
    for k, v in sorted(environ.get_diff(reduce=False).iteritems()):
        if args.uninstall:
            cmd = ['launchctl', 'unsetenv', k]
        else:
            cmd = ['launchctl', 'setenv', k, v]
        print ' '.join(cmd)
        if not args.dry_run:
            subprocess.check_call(cmd)


@command(
    argument('apps', nargs='*'),
    help='print location of Python site-packages',
)
def site_packages(args):
    res = 0
    for app in iter_installed_apps(args.apps):
        path = app.get_site_packages()
        if path:
            print path
        else:
            res = 1
    return res


@command(
    argument('-U', '--uninstall', action='store_true'),
    argument('-n', '--dry-run', action='store_true'),
    argument('apps', nargs='*'),
    help='install zzz_appinit.pth into Python site-packages',
)
def hook_site_packages(args):
    import sitehooks
    res = 0
    for app in iter_installed_apps(args.apps):
        path = app.get_site_packages()
        if path:
            if args.uninstall:
                sitehooks.uninstall(path,
                    module='appinit',
                    dry_run=args.dry_run, verbose=True
                )
            else:
                sitehooks.install(path,
                    module='appinit', func='init', postfix=app.name, args=(app.name, ),
                    dry_run=args.dry_run, verbose=True
                )
        else:
            res = 1
    return res


@command(
    argument('-w', '--which', action='store_true',
        help='print path to Python instead of running it'),
    argument('app'),
    name='python',
    help='run Python interpreter for app',
    parse_known_args=True,
    defaults={'python': True, 'background': False},
)
@command(
    argument('-w', '--which', action='store_true',
        help='print path to executable instead of running it'),
    argument('-b', '--background', action='store_true',
        help='run app in the background (via double fork)'),
    argument('app'),
    name='run',
    help='run app',
    parse_known_args=True,
    defaults={'python': False},
)
def exec_(args, unknown):

    app = next(iter_installed_apps(args.app), None)
    if not app:
        return 1

    if args.python:
        command = [app.get_python()]
    else:
        command = app.get_command()
    if not command:
        return 2

    command.extend(unknown)
    if args.which:
        print ' '.join(command)
        return

    if args.background:
        utils.daemonize()

    environ = get_environ(app, os.environ)
    os.execve(command[0], command, environ)


def main(argv=None):

    from . import _vendor
    _vendor.install()
    import pkg_resources

    args, unparsed = parser.parse_known_args(argv)
    func = args._func
    if func.__parse_known_args:
        res = func(args, unparsed)
    else:
        args = parser.parse_args(argv)
        func = args._func
        res = func(args)

    exit(res or 0)

