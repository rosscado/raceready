'''Exports `app` and other packaged modules for use by the test modules
Use in test modules with import statements like `from context import app`
See https://docs.python-guide.org/writing/structure/#test-suite
See https://docs.pytest.org/en/latest/goodpractices.html#test-discovery
'''
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../apps')))

from apps import app
