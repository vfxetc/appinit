import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-l', '--list', action='store_true',
    help='print installed versions of given app')

parser.add_argument('--python', action='store_true',
    help='run Python interpreter for app')

parser.add_argument('app_name')

def main(argv=None):

    from . import _vendor
    _vendor.install()
    import pkg_resources

    args = parser.parse_args(argv)

    # Grab the named app.
    app_ep = next(pkg_resources.iter_entry_points('appinit_apps', args.app_name), None)
    if not app_ep:
        print >> sys.stderr, 'no appinit app named %r' % args.app_name
        exit(1)
    app_cls = app_ep.load()

    if args.list:
        installed = list(app_cls.iter_installed())
        if not installed:
            print >> sys.stderr, 'no known versions of %s' % args.app_name
        for app in sorted(installed, key=lambda a: a.version):
            print app.version, app.path
        return

    print >> sys.stderr, 'nothing else implemented'



