.. _pythonservice:

Python
======

If you have a BMI-compliant model written in python, grpc4bmi provides a quick way to set up a BMI service.

Installing Requirements
-----------------------

The grpc4bmi Python package should be :ref:`installed <pip-install>`.


Creating
--------

To obtain a python BMI for your model, install the `python bmi package <https://github.com/csdms/bmi-python>`_ and implement the ``Bmi`` abstract base class for your model. For exposing this model as a GRPC service, it is necessary to have a constructor without arguments: all initialization state will be presented to the model via the configuration file in the ``initialize`` method.

.. _running-python:

Running
-------

The installation of the grpc4bmi package installs the ``run-bmi-server`` command. You can run your model as a service by typing

.. code-block:: sh

    $ run-bmi-server --name <PACKAGE>.<MODULE>.<CLASS>

where ``<PACKAGE>``, ``<MODULE>`` are the python package and module containing your python BMI model, which should contain a python class ``<CLASS>`` that implements Bmi. The script assumes that this class does not take any constructor arguments. Upon running, the server will report which networking port it has decided to use on the terminal. This port will later be needed by BMI clients to communicate with your service. The port can also be specified by adding the option ``--port <PORT>`` or pre-define the environment variable ``BMI_PORT``.


.. _python-example:

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

Then we launch this toy model as a service by executing

.. code-block:: sh

    $ run-bmi-server --name mypackage.mymodule.MyBmi

This will report the chosen port number in the standard output stream. It can be used to connect to the service via the BMI :ref:`grpc python client <python-grpc4bmi-client>`.