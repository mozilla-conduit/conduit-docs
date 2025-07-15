# -*- coding: utf-8 -*-

extensions = [
    'sphinx.ext.todo',
    'sphinxcontrib.mermaid',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'Mozilla Conduit'
copyright = u'2017, Mozilla'

version = u'0'
release = u'0'

language = 'en'

exclude_patterns = ['_build', 'venv', 'README.rst']

pygments_style = 'sphinx'

todo_include_todos = False

html_theme = 'default'

# html_static_path = ['_static']
