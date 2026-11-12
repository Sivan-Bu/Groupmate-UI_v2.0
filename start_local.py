"""Interactive local launcher. Credentials remain in this process environment."""
import getpass
import os
from pathlib import Path
import runpy
import sys

if sys.version_info < (3, 10):
    raise SystemExit('Python 3.10 or newer is required.')
os.chdir(Path(__file__).resolve().parent)
if not os.environ.get('GROUPMATE_OWNER_SECRET'):
    secret = getpass.getpass('Teacher password (keep the same password on later runs): ')
    if not secret:
        raise SystemExit('A teacher password is required.')
    os.environ['GROUPMATE_OWNER_SECRET'] = secret
if not os.environ.get('GROUPMATE_XIPU_WORKFLOW_KEY'):
    key = getpass.getpass('Authorized XIPU workflow key (Enter to run without AI): ')
    if key:
        os.environ['GROUPMATE_XIPU_WORKFLOW_KEY'] = key
print('Open http://127.0.0.1:8765/ in your browser. Ctrl+C stops the server.')
sys.argv = ['groupmate.server', '--host', '127.0.0.1', '--port', '8765']
runpy.run_module('groupmate.server', run_name='__main__')
