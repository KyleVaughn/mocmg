.. _install:

Installation
===================

To download and install mocmg, you will need to first install the required software, then follow the instructions for installation with pip.

Requirements
---------------------------------------

Installation of mocmg requires: 

- `git <https://git-scm.com/>`_, 
- `Python <https://www.python.org/>`_ (version 3.6 or greater), 
- and `pip <https://pip.pypa.io/en/stable/>`_.

Optional testing of the installation may be performed using `pytest <https://docs.pytest.org/en/stable/>`_.

Installation on Linux/Mac with pip
----------------------------------------

To install mocmg, you first need to download the source code from `GitHub <https://github.com/KyleVaughn/mocmg>`_. 

.. code-block:: sh

    git clone https://github.com/KyleVaughn/mocmg.git

pip is the package installer for Python. 
Using pip to install mocmg will also install the following dependencies if they are not found:

.. code-block:: sh

    numpy
    scipy
    h5py
    gmsh-dev

To install mocmg from the directory containing the mocmg git repository:

.. code-block:: sh

   pip3 install mocmg/ 

.. note:: Due to local installation of packages with pip, you may need to add the 
          install location to your PATH before you can use mocmg, pytest, etc. 
          Please check the pip install warnings to see if you need to add this location to your PATH
          (typically /home/<user>/.local/bin).

Testing
----------------------------------------

Once installation is complete, testing can be performed using `pytest <https://docs.pytest.org/en/stable/>`_. While in the root mocmg directory:

.. code-block:: sh

   pytest

If all tests were either passed or skipped, your install was successful and you shouldn't have
any problems using mocmg. If any of the tests failed, your installation requires troubleshooting
and may not work as intended.
