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


**1. Create new release and tag it

Edit setup.py and update the version number to new version.  Then tag the release and push it to GitHub.

.. code-block:: bat

    git tag -a -m "Version x.y.z" vx.y.z
    git push --tags

**2. Build source and binary distributions**

.. code-block:: bat

    python setup.py sdist bdist_wheel


**3. Check distributions for errors

.. code-block:: bat
    python -m twine check dist/*

**4. Upload new distribution versions to PyPI.org**

.. code-block:: bat

    python -m twine upload dist/*

