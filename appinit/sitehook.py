import os
import sys


def on_sitehook(app_name):

    print '[appinit] sitehook(s) for {!r}:'.format(app_name)

    from . import _vendor
    _vendor.install()
    import pkg_resources

    for ep in pkg_resources.iter_entry_points('appinit_{}_sitehooks'.format(app_name)):
        print '[appinit]     ', ep
        func = ep.load()
        func(app_name)


_sitehook_template = '''
try:
    import appinit.sitehook
    appinit.sitehook.on_sitehook(%r)
except Exception as e:
    warnings.warn('[appinit] %%s during sitehook: %%s' %% (e.__class__.__name__, e))
'''.strip().replace('   ', '\t')

def install_sitehook(site_packages_dir, app_name):
    hook_path = os.path.join(site_packages_dir, 'zzz_appinit_sitehook.pth')
    hook_source = _sitehook_template % app_name
    with open(hook_path, 'w') as fh:
        fh.write('import warnings; exec %r\n' % hook_source)
