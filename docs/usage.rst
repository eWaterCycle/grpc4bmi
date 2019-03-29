Using the client
================

We assume that service is always dedicated to a single client, addressing a BMI model with multiple users at the same time results in undefined behavior. Therefore we have added utilities to launch the BMI server whenever a client is instantiated.

.. _usage:

Python
------

This is for already running server.

Client
......

After setting up the service, we can expose the model in a different python process. This python environment does no longer need the dependencies of the original model, it just needs the grpc4bmi package installed. With python run

.. code-block:: python

    import grpc
    from grpc4bmi.bmi_grpc_client import BmiClient

    mymodel = BmiClient(grpc.insecure_channel("localhost:<PORT>"))

Where ``<PORT>`` is the network port used by the launched service above. For the example model above the component name will be passed from the service to the client by

.. code-block:: python

    print(mymodel.get_component_name())
    Hello world

Subprocess
..........

To launch the model service in a python subprocess, type

.. code-block:: python

    from grpc4bmi.bmi_client_subproc import BmiClientSubProcess

    mymodel = BmiClientSubProcess(<PACKAGE>.<MODULE>.<CLASS>)

To launch ``run-bmi-server`` in a python subprocess and automatically listen to the right port. Note that this requires your client to run in the same python environment as your model.

:ref:`running-python` Python server chapter explains <PACKAGE>.<MODULE>.<CLASS>.

Polyglot CLI
------------

Once you have started a GRPC server you can test it by connecting to it using the `Polyglot - a universal grpc command line client`_.

Polyglot requires Java and the `polglot.yar` file can be downloaded at https://github.com/dinowernli/polyglot/releases

The following commands expects a GRPC server running on localhost on port 55555.

To get the component name use

.. code-block:: sh

    echo '{}' | java -jar polyglot.jar call --endpoint=localhost:55555 --full_method=bmi.BmiService/getComponentName


.. _Polyglot - a universal grpc command line client: https://github.com/grpc-ecosystem/polyglot
