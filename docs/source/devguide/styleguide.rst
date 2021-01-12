.. _devguide_styleguide:

Style Guide for mocmg
=====================

In order to keep the mocmg code base consistent in style, this guide specifies
a number of rules which should be adhered to when modifying or adding new code to mocmg.

Docstrings
---------------------------------------
mocmg utilizes `Google style docstrings <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_. 
Using `Sphinx <https://www.sphinx-doc.org/en/master/>`_ these docstrings are gathered to form both user
and developer documentation of the API and code as a whole, found on 
`mocmg`s Read the Docs <https://mocmg.readthedocs.io/en/latest/>`_.

PEP 8
---------------------------------------

mocmg is written entirely in Python and strives to follow the `PEP 8 style guide <https://www.python.org/dev/peps/pep-0008/>`_. 
The key place where mocmg departs from PEP 8 is the choice of a maximum line length of 100 characters. 
The argument for this choice is similar to Linus Trovalds' argument `here <https://lkml.org/lkml/2020/5/29/1038>`_.



Enforcement of PEP 8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PEP 8 is enforced within mocmg through the use of isort, black, and flake8 within GitHub's CI workflow.
Whenever a branch is merged, it must pass checks from each of these utilities in addition to 
passing all unit and regression tests.
To make sure your code passes each of these tests prior to a pull request, it is recommended that
you use `pre-commit <https://pre-commit.com/>`_.


Quick Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To setup pre-commit to run isort, black, and flake8 on each commit, use the following commands from 
within the mocmg root directory:

.. code-block:: sh

    pip3 install pre-commit
    pre-commit install



isort
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     

`isort <https://pypi.org/project/isort/>`_ is a Python utility/library to sort imports 
alphabetically, and automatically separated into sections and by type.

black
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`black <https://pypi.org/project/black/>`_ is a Python code formatter.


flake8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`flake8 <https://pypi.org/project/flake8/>`_ is a wrapper around PyFlakes, pycodestyle, and 
Ned Batchelder's McCabe script. It checks code to find violations of PEP 8, invalid docstrings, 
overly complex code, etc.

Error codes come from various packages, so this table can be helpful in understanding error codes from flake8:

+------------+-----------------------------------------------------------------------------------------+
| Error code |   Description                                                                           |
+============+=========================================================================================+
|      F     | Error/violations reported by pyflakes.                                                  |
|            | `F error codes <https://flake8.pycqa.org/en/latest/user/error-codes.html>`_.            |
+------------+-----------------------------------------------------------------------------------------+
|    E/W     | Errors and warnings reproted by pycodestyle                                             |
|            | `E/W error codes <https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes>`_.    |
+------------+-----------------------------------------------------------------------------------------+
|      C     | Violations of McCabe (cyclomatic) complexity limit. The default limit is 10.            |
|            | `Cyclomatic complexity <https://en.wikipedia.org/wiki/Cyclomatic_complexity>`_.         |
+------------+-----------------------------------------------------------------------------------------+
|      B     | Violations from `bug bear <https://pypi.org/project/flake8-bugbear/>`_.                 |
+------------+-----------------------------------------------------------------------------------------+
|      D     | Improperly formatted docstrings.                                                        |
|            | `D error codes <http://www.pydocstyle.org/en/5.1.1/error_codes.html>`_.                 |
+------------+-----------------------------------------------------------------------------------------+
|    RST     | Docstrings are not valid reStructuredText and will break the documentation.             |
|            | `RST error codes <https://pypi.org/project/flake8-rst-docstrings/>`_.                   |
+------------+-----------------------------------------------------------------------------------------+
|      N     | PEP 8 naming convention problem.                                                        |
|            | `N error codes <https://pypi.org/project/pep8-naming/>`_.                               |
+------------+-----------------------------------------------------------------------------------------+
