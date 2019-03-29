.. _pythonservice:

Python
======

If you have a BMI-compliant model written in python, grpc4bmi provides a quick way to set up a BMI service.

Installing Requirements
-----------------------

The grpc4bmi Python package should be installed, see :ref:`pip-install` chapter.


Creating
--------


.. _running-python:

Running
-------

The installation of the grpc4bmi package installs the ``run-bmi-server`` command. You can run your model as a service by typing

.. code-block:: sh

    $ run-bmi-server --name <PACKAGE>.<MODULE>.<CLASS>

where ``<PACKAGE>``, ``<MODULE>`` are the python package and module containing your python BMI model, which should contain a python class ``<CLASS>`` that implements Bmi. The script assumes that this class does not take any constructor arguments. Upon running, the server will report which networking port it has decided to use on the terminal. This port will later be needed by BMI clients to communicate with your service. The port can also be specified by adding the option ``--port <PORT>`` or pre-define the environment variable ``BMI_PORT``.


Example
-------

As an example, suppose we have a package

.. code-block:: sh

    $ mypackage
    $ - __init__.py
    $ - mymodule.py

and inside the ``mymodule.py`` the bmi implementation

.. code-block:: python

    from bmi import Bmi

    class MyBmi(Bmi):
        def __init__(self):
            ...
        def get_component_name(self):
            return "Hello world"

Then the correct call would be.

.. code-block:: sh

    $ run-bmi-server --name my_package.my_module.MyBmi

.. _python-grpc4bmi-client:

