import os
import sys

def install():
    path = os.path.dirname(__file__)
    if not path in sys.path:
        sys.path.append(path)
