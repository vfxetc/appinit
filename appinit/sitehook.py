import os
import sys


_sitehook_template = '''
try:
    import appinit
    appinit.init(%r)
except Exception as e:
    warnings.warn('[appinit] exception %%s during init: %%s' %% (e.__class__.__name__, e))
'''.strip().replace('   ', '\t')


def install_site_hook(site_packages, app_name):
    hook_path = os.path.join(site_packages, 'zzz_appinit.pth')
    hook_source = _sitehook_template % app_name
    with open(hook_path, 'w') as fh:
        fh.write('import warnings; exec %r\n' % hook_source)

def uninstall_site_hook(site_packages):
    hook_path = os.path.join(site_packages, 'zzz_appinit.pth')
    if os.path.exists(hook_path):
        os.unlink(hook_path)

