.. _devguide_testing:

Testing
=====================
Unit tests and regression tests. Update when regression tests are separated.

Requirements
---------------------
Running the test suite requires `pytest <https://docs.pytest.org/en/stable/>`_.
It is assumed that you have installed mocmg, hence it is assumed that all of the packages
outlined in :ref:`install`.

.. note:: As long as you have all of the required packages, you don't need to reinstall mocmg
          after changes to the code in order to run tests that reflect the code's current 
          state. Save time. Don't reinstall unless you need to.

Running Tests
--------------------
To run the test suite, navigate to the root mocmg directory and run:

.. code-block:: sh

   pytest

To collect information about source line coverage, 
you must have the `pytest-cov <https://pypi.org/project/pytest-cov/>`_ package installed and run:

.. code-block:: sh

   pytest --cov-report term-missing --cov-branch --cov=mocmg tests/
