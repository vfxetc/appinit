
- name:
    - appinit
    - vfxinit
    - cgapp
    - vfxapp
    - launcher
    - applauncher

- `appinit --background maya`

- entrypoints to run after the app has setup:
    appinit_NAME_{gui,python}_{pre,post}_launch
    appinit_maya -> anything post launch
    appinit_maya_gui -> GUI post launch

- document structure of entrypoints

- run houdini in foreground

- do we provide enough hooks to find the rest of appinit just from the hook,
  or do we assume that the user must put all of that on the path(s) too?

- hook onto Nuke

