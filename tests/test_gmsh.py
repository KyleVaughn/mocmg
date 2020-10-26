from unittest import TestCase
from .testingUtils import runCmd


class test_gmsh(TestCase):
    # old unit test system (nose) made capturing output of gmsh difficult,
    # so using subprocess was the solution. nose messed with io fileno
    # Might be a better solution with pytest.
    def test_gmshVerbosityDebug(self):
        out, err = runCmd(["python", "./tests/gmsh/gmsh_verbosity.py", "99"])
        out, err = out.decode("ascii").splitlines(), err.decode("ascii").splitlines()
        self.assertIn("Error   : OpenCASCADE surface with tag 1 already exists", err)
        self.assertIn("Warning : Gmsh has aleady been initialized", err)
        self.assertIn("Info    : Meshing 2D...", out)
        self.assertIn("Debug   : Syncing OCC_Internals with GModel", out)

    def test_gmshVerbosityInfo(self):
        out, err = runCmd(["python", "./tests/gmsh/gmsh_verbosity.py", "5"])
        out, err = out.decode("ascii").splitlines(), err.decode("ascii").splitlines()
        self.assertIn("Error   : OpenCASCADE surface with tag 1 already exists", err)
        self.assertIn("Info    : Meshing 2D...", out)
        self.assertNotIn("Debug   : Syncing OCC_Internals with GModel", out)

    def test_gmshVerbosityWarning(self):
        out, err = runCmd(["python", "./tests/gmsh/gmsh_verbosity.py", "2"])
        out, err = out.decode("ascii").splitlines(), err.decode("ascii").splitlines()
        self.assertIn("Error   : OpenCASCADE surface with tag 1 already exists", err)
        self.assertFalse(out)

    def test_gmshVerbosityError(self):
        out, err = runCmd(["python", "./tests/gmsh/gmsh_verbosity.py", "1"])
        out, err = out.decode("ascii").splitlines(), err.decode("ascii").splitlines()
        self.assertIn("Error   : OpenCASCADE surface with tag 1 already exists", err)
        self.assertFalse(out)

    def test_gmshVerbositySilent(self):
        out, err = runCmd(["python", "./tests/gmsh/gmsh_verbosity.py", "0"])
        out, err = out.decode("ascii").splitlines(), err.decode("ascii").splitlines()
        self.assertNotIn("Error   : OpenCASCADE surface with tag 1 already exists", err)
        self.assertFalse(out)
