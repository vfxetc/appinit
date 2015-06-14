Triggering the hooks
====================

There are a number of ways that you can trigger the hooks. Any one of
them is sufficient, but you may safely trigger multiple.


1. Launch directly
------------------

You can launch your programs directly via the `appinit` command::

    $ appinit maya
    # Maya launches here.

    $ appinit --python houdini
    # Houdini's Python runs here.


2. "Activate" your terminal session
-----------------------------------

You can export the environment variables that appinit uses so that your
current session will use the hooks::

    eval $(appinit --export maya)


3. "Activate" your login session
--------------------------------

For OS X only, you can export the environment variables so that your
current login session will use the hooks::

    appinit --launchctl maya


4. Hook `site-packages`
-----------------------

For Maya, you can install a `*.pth` hook into Maya's `site-packages`
directory which will trigger the hooks::

    appinit --install-sitehook maya


5. Manually
-----------

You can manually trigger the hook in Python via :func:`appinit.init_app(app_name)`.


