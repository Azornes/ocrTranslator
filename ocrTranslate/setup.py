from distutils.core import setup
import py2exe, sys, os

# TODO create working executable

# sys.argv.append('py2exe')

# setup(
#    options = {'py2exe': {'bundle_files': 3}},
#    windows = [{'script': "main.py"}],
#    zipfile = None,
# )

setup(console=['main.py'])
