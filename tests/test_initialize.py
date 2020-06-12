import gmsh
import subprocess
from unittest import TestCase

# Need to find inexpensive example where gmsh gives a warning. When found, use instead of current

class test_gmsh(TestCase):

    # nosetests makes capturing output of gmsh difficult, so using subprocess is the solution for now.
    def test_gmshVerbosityDebug(self):
        output = subprocess.check_output(['python','./tests/gmsh/gmsh_verbosity99.py']).decode('ascii').splitlines()
        self.assertIn('Info    : Meshing 2D...', output)
        self.assertIn('Debug   : Destroying model ', output)

    def test_gmshVerbosityInfo(self):
        output = subprocess.check_output(['python','./tests/gmsh/gmsh_verbosity5.py']).decode('ascii').splitlines()
        self.assertIn('Info    : Meshing 2D...', output)
        self.assertNotIn('Debug   : Destroying model ', output)

    def test_gmshVerbosityWarning(self):
        output = subprocess.check_output(['python','./tests/gmsh/gmsh_verbosity5.py']).decode('ascii').splitlines()
        self.assertIn('Info    : Meshing 2D...', output)
        self.assertNotIn('Debug   : Destroying model ', output)
