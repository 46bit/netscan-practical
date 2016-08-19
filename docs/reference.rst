.. _ref_reference:

**********************
Command Line Reference
**********************

This program requires database connection parameters to connect to a MySql database. 
The default values are given below; these may be overidden by values in a dbinfer.ini file 
in the same directory as the executable, or by the following command line arguments.

The command line options are:

+---+-------------+-------------+----------------------------------------------------------+
| -u| --user      | string      | user name to access database (default 'cyber-practicals')|
+---+-------------+-------------+----------------------------------------------------------+
| -p| --password  | string      | user password (default '1kjg4GIiu5')                     |
+---+-------------+-------------+----------------------------------------------------------+
| -h| --host      | string      | host IP address , or 'localhost' (default 'localhost')   |
+---+-------------+-------------+----------------------------------------------------------+
| -d| --database  | string      | database name (default 'examresults')                    |
+---+-------------+-------------+----------------------------------------------------------+
| ? or help                     | print usage message                                      |
+---+-------------+-------------+----------------------------------------------------------+


If the program is invoked from the command line it provides a command shell which allows a range of
queries and optional inference restriction policies over a pre-built test table. 

Commands supported by the shell are:

.. tabularcolumns:: |l|L|l|l|L|

+--------+----+----------+-------+--------------------------------------------------------------+
| config | Configure how queries are processed, the command takes the following options:        |
|        +----+----------+-------+--------------------------------------------------------------+
|        |  -u| --user   | string| Specify the user as 'guest' or 'staff'                       |
|        |    |          |       | (guests have statistical access, staff have full access).    |
|        +----+----------+-------+--------------------------------------------------------------+
|        |  -p| --policy | string| A single character which specifies the inference             |
|        |    |          |       | restriction policy. ``k``: restrict queries where 1 row is   |
|        |    |          |       | greater than 30% of any field. ``l``: lattice restriction.   |
|        |    |          |       | ``n``: no policy.                                            |
|        +----+----------+-------+--------------------------------------------------------------+
|        |  -v| --verbose| string| To enable or disable verbose printing.                       |
|        |    |          |       | 't' or 'true', 'f' or 'false respectively.                   |
+--------+----+----------+-------+--------------------------------------------------------------+
| exit   | Close the program.                                                                   |
+--------+--------------------------------------------------------------------------------------+
| query  | The text following the command is a complete WHERE clause, see :ref:`ref_examples`.  | 
|        | In staff mode rows are printed, in guest mode a statistical summary is printed       |
|        | giving the number of rows selected and the mean of the result fields in those rows.  |
+--------+--------------------------------------------------------------------------------------+
| rebuild| Rebuid the test database.                                                            |
+--------+--------------------------------------------------------------------------------------+


The field names in the database table are: ``id``: unique row key, ``first`` and 
``last`` names, ``gender``, then exam grades in the range 1-5 in fields corresponding to study modules: 
``threat``, ``network``, ``crypto`` and ``forensic``.

.. _ref_api:

*********************
Program API Reference
*********************

The API interface provides the same functions as the command line. ``rebuild()`` is a module function,
other actions are provided as methods wihin a :class:`DbInfer` class. Note that there is no *exit* method,
instead there is a ``close()`` method, which closes the dabase connection which is otherwise held open 
by the :class:`DbInfer` object; configuration is provided by separate methods: ``setUser``,
``setPolicy`` and ``setVerbose``. 

.. module:: dbinfer
.. moduleauthor:: Howard Chivers

.. _ref_module_functions:

----------------
Module Functions
----------------

.. function::	rebuild(...)

    Rebuilds the database table. Arguments to the function are optional database connection 
    specifications, if they are not provided the default values are used unless 
    alternative values have been provided in a ``dbinfer.ini`` file. 
    
    Optional arguments are:
    
	:user: (default *cyber-practicals*)
	:password: (default *1kjg4GIiu5*)
	:host: (default *localhost*)
	:database: (default *examresults*)

--------------
Module Classes
--------------

.. class::	DbInfer(...)

    The :class:`DbInfer` class provides query functions on the test database. 
    See :ref:`ref_algorithms` for more detail, including output provided by verbose mode.
    
    The class init takes the same optional attributes as the ``rebuild()`` function and they
    are used in the same way. A :class:`DbInfer` object opens a connection to the database 
    and this remains open until ``close()`` is called.   

    The methods of this class raise a ``ValueError`` exception if an input parameter is invalid.

    The methods of this class are:

        .. method:: setUser(user) 

        The user must be ``'guest'`` or ``'staff'``.  (Default 'guest') Queries when a *staff* 
        user is set may include user name fields (``first``, or ``last``) and will return whole rows. Queries 
        after the *guest* user is set return a single row with mean values for the exam grades
        calculated from all rows that match the query.

        .. method:: setPolicy(policy)
 
        The policy may be ``'k'``:restrict queries where 1 row is greater than 30% of any field, 
        ``'l'``: lattice restriction, or ``'n'``: no policy. See :ref:`ref_algorithms` for more detail
        on how these policies are applied.
        
        .. method:: setVerbose(bool)
 
        The parameter must be ``True`` or ``False``, and sets the verbose mode accordingly. Examples of
        verbose output are give in :ref:`ref_algorithms`, they include how policies are applied to rows
        and reporting text in a query which is detected as an illegal field or keyword.
        
        .. method:: query(where)
        
        This queries the database; the parameter is the logical condition of an SQL WHERE clause. See 
        :ref:`ref_examples` for more detail on such clauses. 
        
        The field names in the database table are: ``id``: unique row identifier, ``first`` and 
        ``last`` names, ``gender``, then exam grades in the range 1-5 in fields corresponding to study modules: 
        ``threat``, ``network``, ``crypto`` and ``forensic``.
        
        The query returns (count, list) where the count is the number of rows selected and the list is a 
        list of tuples. If *staff* user is selected each tuple is a complete row with fields in the order given above; 
        *guest* queries a single tuple in the list contains the means of the module grades. 
        
        .. method:: close()
        
        Close the database connection gracefully. After this has been executed no further operations will 
        be possible using this object.



