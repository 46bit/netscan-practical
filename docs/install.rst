
.. _ref_install:

============
Installation
============

dbinfer is usually pre-installed as part of an experiment VM, this section should only be of interest
to developers or lecturers who wish to configure their own systems.

dbinfer is compatible with Python 3, it is not available for Python 2. Python 3 must installed and
*pip* enabled before you begin installation.

dbinfer is distributed as a packaged souce file, it can be installed using PIP as follows::

    pip install --upgrade --no-index <filename>

If you are installing an alpha or beta copy it is also necessary to use the ``--pre`` option,
many Linux systems will require you to expicitly use python 3, since they support both, e.g.::

    python3 -m pip install --upgrade --no-index --pre <filename>

Configuration
^^^^^^^^^^^^^
dbinfer will have been installed to the site-packages library for python 3.

If the database connection requirements are not the same as the program defaults (see :ref:`ref_reference`)
place a file named **dbinfer.ini** in the directory with the scripts;
it should have a single section (params) and a lines that specify any new connection parameters, for example::

    [params]
    host = 127.0.0.1

It is possible to configure new default values for the other connection parameters in the same way.

After installation it is necessary to build the database table to be used for the experiment, open the dbinfer
command line and use the *rebuild* command::

    >dbinfer
    dbinfer> rebuild
    (1, 'Matilda', 'Adams', 'F', 4, 3, 1, 3)
    (2, 'Oliver', 'Alexander', 'M', 4, 2, 4, 3)
    (3, 'Eva', 'Allen', 'F', 4, 3, 3, 3)
    ...
    dbinfer> exit
    Database Closed

The data for this table is in the *results.csv* file in a *data* subdirectory of the installed module;
it can be substituted with other data if required but the schema is fixed.










