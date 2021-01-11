.. _devguide:

===================
Developer Guide
===================

---------------------------------------
Code Style
---------------------------------------
Code style within mocmg is enforced through the use of isort, flake8, and black within GitHub's CI workflow.
Whenever a branch is merged, it must pass checks from each of these utilities in addition to passing all unit and regression tests.

The standards being enforced are: 
- flake8 and black enforce PEP8
- line length max = 100 (black)
- Subset of PEP 8 enforced by black
- isort sort imports alphabetically, and automatically separated into sections and by type

pre-commit

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
black
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
black

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
isort
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
isort
