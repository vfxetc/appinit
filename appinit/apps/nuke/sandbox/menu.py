import sys

# We can easily be sourced a few times.
_appinit_nuke_gui_counter = globals().get('_appinit_nuke_gui_counter', 0) + 1
if _appinit_nuke_gui_counter == 1:
    print >> sys.stderr, '[appinit] nuke hooked via menu'
    try:
        import appinit
        appinit.init('nuke.gui')
    except Exception as e:
        import warnings
        warnings.warn('[appinit] exception %s during init: %s' % (e.__class__.__name__, e))
