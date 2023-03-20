.. _pythonservice:

Python
======

If you have a BMI-compliant model written in python, grpc4bmi provides a quick way to set up a BMI service.

Installing Requirements
-----------------------

The grpc4bmi Python package should be :ref:`installed <pip-install>`.


Creating
--------

To obtain a python BMI for your model, install the `Python bmi package (bmipy) <https://pypi.org/project/bmipy/>`_ and implement the :class:`bmipy.Bmi` abstract base class for your model. For exposing this model as a GRPC service, it is necessary to have a constructor without arguments: all initialization state will be presented to the model via the configuration file in the ``initialize`` method.

.. _running-python:

Running
-------

The installation of the grpc4bmi package installs the ``run-bmi-server`` command. You can run your model as a service by typing

.. code-block:: sh

    $ run-bmi-server --name <PACKAGE>.<MODULE>.<CLASS>

where ``<PACKAGE>``, ``<MODULE>`` are the python package and module containing your python BMI model, which should contain a python class ``<CLASS>`` that implements Bmi. The script assumes that this class does not take any constructor arguments. Upon running, the server will report which networking port it has decided to use on the terminal. This port will later be needed by BMI clients to communicate with your service.
The port can also be specified by adding the option ``--port <PORT>`` or pre-define the environment variable ``BMI_PORT`` (the latter takes precedence over the former).
An extra system path can be specified by adding the option ``--path <PATH>`` or pre-define the environment variable ``BMI_PATH``.


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

    from bmipy import Bmi

    class MyBmi(Bmi):
        def __init__(self):
            ...
        def get_component_name(self):
            return "Hello world"

Then we launch this toy model as a service by executing

.. code-block:: sh

    $ run-bmi-server --name mypackage.mymodule.MyBmi

This will report the chosen port number in the standard output stream. It can be used to connect to the service via the BMI :ref:`grpc python client <python-grpc4bmi-client>`.

Legacy version
--------------

The grpc4bmi by default uses the `v2.0 version of the Basic Model Interface (BMI) <https://pypi.org/project/bmipy/2.0/>`_ on the client and server side.
Grpc4bmi has support for `legacy version 0.2 of BMI <https://pypi.org/project/basic-modeling-interface/0.2/>`_ on the server side.

A legacy model can be launched with

.. code-block:: sh

    $ run-bmi-server --bmi-version 0.2 --name mypackage.mymodule.MyLegacyBmi

The functions only present in BMI v0.2 will not be callable:

- update_frac
- get_grid_connectivity
- get_grid_offset

The functions only present in BMI v2.0 will throw not implemented errors:

- get_var_location
- get_grid_node_count
- get_grid_edge_count
- get_grid_face_count
- get_grid_edge_nodes
- get_grid_face_nodes
- get_grid_face_edges
- get_grid_nodes_per_face
