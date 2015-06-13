'''
On startup, Maya searches `sys.path` for `userSetup.py`,
and `execfile`s them all. In Python, you must call `maya.standalone.initialize()`
for this behaviour.

This is such a file.

Unfortunately, it gets exec-ed instead of imported, so we have no access
to handy values such as __file__ to figure out where we are. You must 
also be careful as everything that runs here does so in the global
state. So, be cautious, and clean up after yourself!

'''

print 'appinit/maya/sandbox/userSetup.py'

# We can easily be sourced a few times.
_appinit_counter = globals().get('_appinit_counter', 0) + 1
