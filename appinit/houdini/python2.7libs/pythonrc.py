'''
On startup of either the GUI or Python shell, Houdini searches $HOUDINI_PATH
for `pythonX.Ylibs/pythonrc.py`, and `execfile`s them all.

This is such a file.

Unfortunately, it gets exec-ed instead of imported, so we have no access
to handy values such as __file__ to figure out where we are. You must 
also be careful as everything that runs here does so in the global
state. So, be cautious, and clean up after yourself!

'''

print 'appinit/houdini/python2.7libs/pythonrc.py'

# We can easily be sourced a few times.
_appinit_counter = globals().get('_appinit_counter', 0) + 1
