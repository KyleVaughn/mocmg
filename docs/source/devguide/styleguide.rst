.. _devguide_styleguide:

Style Guide for mocmg
=====================

In order to keep the mocmg code base consistent in style, this guide specifies
a number of rules which should be adhered to when modifying or adding new code to mocmg.


PEP 8
---------------------------------------

mocmg is written entirely in Python and strives to follow the `PEP 8 style guide <https://www.python.org/dev/peps/pep-0008/>`_. 
The key place mocmg departs from PEP 8 is the choice of a maximum line length of 100 characters. 
The argument for this choice is similar to Linus Trovalds' argument `here <https://lkml.org/lkml/2020/5/29/1038>`_.


Enforcement of PEP 8
---------------------------------------
PEP 8 is enforced within mocmg through the use of isort, black, and flake8 within GitHub's CI workflow.
Whenever a branch is merged, it must pass checks from each of these utilities in addition to 
passing all unit and regression tests.
To make sure your code passes each of these tests prior to a pull request, it is recommended that
you use `pre-commit <https://pre-commit.com/>`_.


Quick Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To setup pre-commit to run isort, black, and flake8 on each commit (from the mocmg root directory):

.. code-block:: sh

    pip3 install pre-commit isort black flake8 
    pip3 install flake8-docstrings flake8-rst-docstrings flake8-bugbear pep8-naming
    pre-commit install

pre-commit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pre-commit can be used to run isort, black, and flake8 on each new or changed file prior to a commit.
In the event that you don't want to use pre-commit, you can get the same effect by running isort,
black, and flake8 on each file.

To setup pre-commit, from the mocmg root directory:

.. code-block:: sh

    pip3 install pre-commit
    pre-commit install


pre-commit will then use .pre-commit-config.yaml to specify which packages to run. 


black
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

black


flake8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Error/violation specifications

- F: Error/violations reported by pyflakes, a tool which parses source files and finds invalid Python code.
  Codes can be found `here. <https://flake8.pycqa.org/en/latest/user/error-codes.html>`_

- E/W: Errors and warnings reproted by pycodestyle, a tool to check your Python code against some of the style conventions in PEP 8.
  Codes can be found `here <https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes>`_

- C: Violations of McCabe complexity limit. The default limit is 10.

- B: Violations from `bug bear <https://pypi.org/project/flake8-bugbear/>`_

- D: Docstrings `doc <http://www.pydocstyle.org/en/5.1.1/error_codes.html>`_ `RST <https://pypi.org/project/flake8-rst-docstrings/>`_ Ignore google docstring

- Some errors ignored for compatibility with black. See `here <https://black.readthedocs.io/en/stable/the_black_code_style.html#line-length>`_


bugbear
docstrings
rst-docstrings
pep8-naming


isort
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

isort



testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To examine test coverage:

.. code-block:: sh

   pytest --cov-report term-missing --cov-branch --cov=mocmg tests/

