.. _usage:

Using the client
================

We assume that service is always dedicated to a single client, addressing a BMI model with multiple users at the same time results in undefined behavior.

.. _python-grpc4bmi-client:

Python BMI Client
.................

For a given running BMI service process connected to networking port ``<PORT>``, we can start communicating with this server by instantiating the ``BmiClient`` python class:

.. code-block:: python

    import grpc
    from grpc4bmi.bmi_grpc_client import BmiClient

    mymodel = BmiClient(grpc.insecure_channel("localhost:<PORT>"))


For the example model launched in :ref:`python-example`, the component name can be retrieved following the usual BMI syntax,

.. code-block:: python

    print(mymodel.get_component_name())
    Hello world


Python Subprocess
.................

This python class launches a BMI server upon creation,

.. code-block:: python

    from grpc4bmi.bmi_client_subproc import BmiClientSubProcess

    model = BmiClientSubProcess(<PACKAGE>.<MODULE>.<CLASS>)


The code above will execute ``run-bmi-server`` in a python subprocess and automatically listen to the appropriate port. Note that this requires your client to run in the same python environment as your model.

:ref:`running-python` Python server explains the roles of ``<PACKAGE>``, ``<MODULE>`` and ``<CLASS>``.

Polyglot CLI
------------

Once you have started a GRPC server you can test it by connecting to it using the `Polyglot - a universal grpc command line client`_.

Polyglot requires Java and the `polglot.yar` file can be downloaded at https://github.com/dinowernli/polyglot/releases

The following commands expects a GRPC server running on localhost on port 55555.

To get the component name use

.. code-block:: sh

    echo '{}' | java -jar polyglot.jar call --endpoint=localhost:55555 --full_method=bmi.BmiService/getComponentName


.. _Polyglot - a universal grpc command line client: https://github.com/grpc-ecosystem/polyglot
