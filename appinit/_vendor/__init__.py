import os
import sys

from ..utils import only_once

@only_once
def install():
    path = os.path.dirname(__file__)
    if not path in sys.path:
        sys.path.append(path)
