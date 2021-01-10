.. _devguide:

===================
Developer Guide
===================

---------------------------------------
Code Style
---------------------------------------
Code style withing mocmg is enforced through the use of isort, flake8, and black in GitHub's CI workflow.
Whenever a branch is merged, it must pass checks from each of these utilities in addition to passing all unit and regression tests.

The 
- flake8 and black enforce PEP8
- line length max = 100 (black)
- Subset of PEP 8 enforced by black
- isort sort imports alphabetically, and automatically separated into sections and by type

pre-commit

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
black
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
flake8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
isort
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
