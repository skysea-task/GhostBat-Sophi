import sys
import os
from subprocess import getoutput

def restart_program():
  getoutput("rm -rf log.txt")
  script = os.path.abspath(sys.argv[0])
  project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
  if project_root not in sys.path:
    sys.path.insert(0, project_root)
  python = sys.executable
  os.execl(python, python, script, *sys.argv[1:])
