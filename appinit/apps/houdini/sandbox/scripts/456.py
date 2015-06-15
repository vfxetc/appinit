'''
One of the many hooks for Houdini.
'''

# We can easily be sourced a few times.
_appinit_456_counter = globals().get('_appinit_456_counter', 0) + 1
if _appinit_456_counter == 1:
    print '[appinit] houdini hooked via 456'
    try:
        import appinit
        appinit.init('houdini')
    except Exception as e:
        import warnings
        warnings.warn('[appinit] %s during appinit.init(): %s' % (e.__class__.__name__, e))