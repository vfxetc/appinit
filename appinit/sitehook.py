import glob
import os
import sys


_sitehook_template = '''
print '[appinit]', %r, 'hooked via site-packages'
import sys
sys.path.append(%r)
try:
    import appinit
    appinit.init(%r)
except Exception as e:
    warnings.warn('[appinit] exception %%s during site hook: %%s' %% (e.__class__.__name__, e))
'''.strip().replace('   ', '\t')


def install_site_hook(site_packages, app_name, verbose=False, dry_run=False):
    hook_path = os.path.join(site_packages, 'zzz_appinit.pth')
    import_path = os.path.abspath(os.path.join(__file__, '..', '..'))
    if verbose:
        print 'installing:', hook_path
        print 'which will import appinit from:', import_path
    if dry_run:
        return
    hook_source = _sitehook_template % (app_name, import_path, app_name)
    with open(hook_path, 'w') as fh:
        fh.write('import warnings; exec %r\n' % hook_source)

def uninstall_site_hook(site_packages, verbose=False, dry_run=False):
    for hook_path in glob.glob(os.path.join(site_packages, '*appinit*.pth')):
        if verbose:
            print 'uninstalling:', hook_path
        if dry_run:
            continue
        os.unlink(hook_path)

