
# We can easily be sourced a few times.
_appinit_nuke_counter = globals().get('_appinit_nuke_counter', 0) + 1
if _appinit_nuke_counter == 1:
    print '[appinit] nuke hooked via init'
    try:
        import appinit
        appinit.init('nuke')
    except Exception as e:
        import warnings
        warnings.warn('[appinit] exception %s during init: %s' % (e.__class__.__name__, e))
