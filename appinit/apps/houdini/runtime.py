from ... import init

import hou


_idle_funcs = []
def call_once_on_idle(func):
    """Register a function to be called once in Houdini's idle loop."""
    if not hasattr(hou, 'ui'):
        raise RuntimeError('Houdini has no ui')
    _idle_funcs.append(func)
    hou.ui.addEventLoopCallback(_on_idle)

def _on_idle():
    while _idle_funcs:
        func = _idle_funcs.pop(0)
        func()
    hou.ui.removeEventLoopCallback(_on_idle)

def _defer_gui_idle_trigger():
    """Called by appinit_houdini entrypoint to setup the gui_idle trigger."""
    try:
        call_once_on_idle(lambda: init('houdini.gui'))
    except RuntimeError:
        pass

