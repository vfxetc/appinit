import sys

# We can easily be sourced a few times.
_appinit_mari_gui_counter = globals().get('_appinit_mari_gui_counter', 0) + 1
if _appinit_mari_gui_counter == 1:
    print >> sys.stderr, '[appinit] mari hooked via menu'
    try:
        import appinit
        appinit.init('mari.gui')
    except Exception as e:
        import warnings
        warnings.warn('[appinit] exception %s during init: %s' % (e.__class__.__name__, e))
