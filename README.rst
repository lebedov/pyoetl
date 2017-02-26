.. -*- rst -*-

PyOETL
======

Package Description
-------------------
PyOETL is a Python interface to the OrientDB ETL tool. It can be invoked from 
the command line just like the ``oetl.sh`` script included in OrientDB, but has 
some additional features:

- can process multiple JSON input files; 
- can be invoked from outside of the OrientDB installation directory; 
- provides a Python class that can be used 
  to invoke the ETL tool from within a Python program.

.. image:: https://img.shields.io/pypi/v/pyoetl.svg
    :target: https://pypi.python.org/pypi/pyoetl
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/dm/pyoetl.svg
    :target: https://pypi.python.org/pypi/pyoetl
    :alt: Downloads

Installation
------------
The package may be installed as follows: ::

    pip install pyoetl

Usage
-----
The ``ORIENTDB_DIR`` environmental variable must be set to the installation 
directory of OrientDB.

Invoke PyOETL from the command line as follows: ::

    pyoetl input_cfg_file.json

Author
------
See the included `AUTHORS.rst
<https://github.com/lebedov/pyoetl/blob/master/AUTHORS.rst>`_ file for more
information.

License
-------
This software is licensed under the `BSD License
<http://www.opensource.org/licenses/bsd-license>`_.  See the included
`LICENSE.rst <https://github.com/lebedov/pyoetl/blob/master/LICENSE.rst>`_ file
for more information.
