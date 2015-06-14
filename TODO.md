
- name:
    - appinit
    - vfxinit
    - cgapp
    - vfxapp
    - launcher
    - applauncher

- `appinit maya==2015` ??
- `appinit --export maya houdini` to export envvars for multiple?
    - could say everything after `--` is args for the actual command:
        appinit maya --python -- script.py
    - could move to optparse which would require the options before the
      arguments

- verbosity via APPINIT_VERBOSE:
    - currently in:
        - appinit:init()
        - sitehook/zzz_appinit.pth
        - maya/userSetup.py
        - houdinit/pythonrc.py
    - move as much of the messages into appinit:init so that everything
      doesn't need to keep implementing the same verbosity logic

- entrypoints to run after the app has setup:
    appinit_NAME_{gui,python}_{pre,post}_launch
    appinit_maya -> anything post launch
    appinit_maya_gui -> GUI post launch

- document structure of entrypoints

- do we provide enough hooks to find the rest of appinit just from the hook,
  or do we assume that the user must put all of that on the path(s) too?

- hook onto Nuke

