
# We can easily be sourced a few times.
_appinit_counter = globals().get('_appinit_counter', 0) + 1
if _appinit_counter == 1:
    print '[appinit] IT hooked via it.ini'
    try:
        import appinit
        appinit.init('it')
    except Exception as e:
        import warnings
        warnings.warn('[appinit] exception %s during init: %s' % (e.__class__.__name__, e))
