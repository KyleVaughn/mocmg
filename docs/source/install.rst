.. _install:

===================
Installation
===================

To download and install mocmg, you will need to first install the required software, then follow the instructions for installation with pip.

---------------------------------------
Requirements
---------------------------------------
Installation of mocmg requires `git <https://git-scm.com/>`_, 
`Python <https://www.python.org/>`_ (version 3.6 or greater), 
and `pip <https://pip.pypa.io/en/stable/>`_.
Optional testing of the installation may be performed using `pytest <https://docs.pytest.org/en/stable/>`_.

----------------------------------------
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

----------------------------------------
Testing
----------------------------------------

Once installation is complete, testing can be performed using `pytest <https://docs.pytest.org/en/stable/>`_. While in the root mocmg directory:

.. code-block:: sh

   pytest

To examine test coverage:

.. code-block:: sh

   pytest --cov-report term-missing --cov-branch --cov=mocmg tests/
