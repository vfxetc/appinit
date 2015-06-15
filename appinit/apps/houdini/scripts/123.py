'''
One of the many hooks for Houdini.
'''

# We can easily be sourced a few times.
_appinit_123_counter = globals().get('_appinit_123_counter', 0) + 1
if _appinit_123_counter == 1:
    print '[appinit] houdini hooked via 123'
    try:
        import appinit
        appinit.init('houdini_gui')
    except Exception as e:
        import warnings
        warnings.warn('[appinit] %s during appinit.init(): %s' % (e.__class__.__name__, e))


# Run the original too, since there is some important stuff in there.
hou.hscript('source 123.cmd')
