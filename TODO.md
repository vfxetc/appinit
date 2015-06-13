
- name:
    - appinit
    - vfxinit
    - cgapp
    - vfxapp
    - launcher
    - applauncher

- `appinit [options] APPNAME`

    --launchctl -> launchctl setenv $WHATEVER; works for this login session
    --export -> print for eval in shell
    --install-pth -> install a .pth (for Maya, at least)

    --background -> run in background
    --python -> run python for this app instead (and initialize it, if possible)

- entrypoints to run after the app has setup:
    appinit_NAME_{gui,python}_{pre,post}_launch
    appinit_maya -> anything post launch
    appinit_maya_gui -> GUI post launch

- hook onto Maya setup BEFORE `maya.standalone.initialize()`
    - install a .pth file?

- do we provide enough hooks to find the rest of appinit just from the hook,
  or do we assume that the user must put all of that on the path(s) too?

- houdini
    - HOUDINI_PATH requires "&" to represent original path
    - startup:
        a) responds to first 123.py on startup WITHOUT a hip file (not reproduced here)
        b) responds to first 456.py when a file is loaded or the session
           is cleared (not reproduced (here)
        b) searches $HOUDINI_PATH for ALL (confirmed):
            - python2.{6,7}libs/pythonrc.py
            - python2.{6,7}libs/.pythonrc.py
            - houdini/scripts/python/pythonrc.py (for b/c; not reproduced here)
    - plugins?

- maya
    - responds to ALL userSetup.py on PYTHONPATH
    - plugins?

- nuke
    ???

