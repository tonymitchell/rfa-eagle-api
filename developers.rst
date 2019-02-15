Developers Guide
================

Details on how to setup your local development environment

Setup local environment (on Windows)
------------------------------------

**1. Create virtual environment and activate it**

Windows

.. code-block:: bat

    py -m venv venv
    venv\Scripts\activate

Linux

.. code-block:: bat

    python -m venv venv
    source venv\bin\activate


**2. Install build/deployment tools**

.. code-block:: bat

    pip install --upgrade pylint pytest setuptools wheel twine

**3. Install library in developer mode**

.. code-block:: bat
    
    python setup.py develop

**4. Run Tests (Optional)**

.. code-block:: bat
    
    python setup.py test


Deploying the library to PyPI
-----------------------------

See https://packaging.python.org/tutorials/packaging-projects/ for details.

**1. Build source and binary distributions**

.. code-block:: bat

    python setup.py sdist bdist_wheel


**2. Check distributions for errors

.. code-block:: bat
    python -m twine check dist/*

**3. Upload new distribution versions to PyPI.org**

.. code-block:: bat

    python -m twine upload dist/*