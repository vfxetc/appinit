
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
    --install-sitehook -> install a .pth

    --background -> run in background
    --python -> run python for this app instead (and initialize it, if possible)

- entrypoints to run after the app has setup:
    appinit_NAME_{gui,python}_{pre,post}_launch
    appinit_maya -> anything post launch
    appinit_maya_gui -> GUI post launch

- document structure of entrypoints

- run houdini in foreground

- do we provide enough hooks to find the rest of appinit just from the hook,
  or do we assume that the user must put all of that on the path(s) too?

- hook onto Nuke

