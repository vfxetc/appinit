Applications
============

Maya
----

Maya will typically find all ``userSetup.py`` scripts on the ``sys.path``,
and ``execfile`` them all.

Ergo, one method of hooking Maya is by such a module on the ``$PYTHONPATH``
envvar.

Maya also supplies it's own Python interpreter, so we may install a ``*.pth``
file which exploits some functionality within the `site module <https://docs.python.org/2/library/site.html>`_ in which any lines beginning with ``import``
are executed.


Houdini
-------

Houdini will search the ``$HOUDINI_PATH`` envvar for ``pythonX.Y`` directories
(typically ``python2.7`` in current versions) to add to ``sys.path``. If those
directories contain ``pythonrc.py`` scripts, the will be ``execfile``-ed.

.. warning::

    The ``$HOUDINI_PATH`` **must** contain ``"&"`` to represent the base path.

.. note::

    Houdini does not ``execfile`` all ``pythonrc.py`` files it finds
    on ``sys.path``, just those in ``pythonX.Y`` directories.

    It will also execute ``.pythonrc.py`` scripts, but we don't hook those.

    Houdini also (reports to) respond to ``123.py`` and ``456.py`` files on
    startup without a scene, and opening or clearing a scene (respectively),
    but we don't attach to those.