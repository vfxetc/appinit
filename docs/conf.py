import os
import sys


project = 'appinit'
copyright = '2015, Mike Boers'
author = 'Mike Boers'
version = '0.1' # base version
release = '0.1.0' # full release


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'alabaster'
html_static_path = ['_static']

man_pages = [
    (master_doc, 'appinit', u'appinit Documentation',
     [author], 1)
]
