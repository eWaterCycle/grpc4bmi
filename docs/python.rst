.. _pythonservice:

Python BMI service
==================

If you have a BMI-compliant model written in python, grpc4bmi provides a quick way to set up a BMI service.

Installation
------------
If your model uses some virtual environment with installed dependencies (e.g. Anaconda or virtualenv), activate this environment before installing grpc4bmi.

Install the grpc4bmi python package with pip:

.. code-block:: sh

    $ pip install grpc4bmi

This will install the latest release of the package; for the most recent github revision type instead

.. code-block:: sh

    $ pip install git+https://github.com/eWaterCycle/grpc4bmi.git#egg=grpc4bmi

Deployment
----------
Service
.......
The installation of the package exposes the script ``run-bmi-server``. You can run your model as a service by typing

.. code-block:: sh

    $ run-bmi-server --name <PACKAGE>.<MODULE>.<CLASS>

where ``<PACKAGE>``, ``<MODULE>`` are the python package and module containing your python BMI model, which should contain a python class ``<CLASS>`` that implements Bmi. The script assumes that this class does not take any constructor arguments. Upon running, the server will report which networking port it has decided to use on the terminal. This port will later be needed by BMI clients to communicate with your service. The port can also be specified by adding the option ``--port <PORT>`` or pre-define the environment variable ``BMI_PORT``.

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

Service-Client deployment
-------------------------
We assume that service is always dedicated to a single client, addressing a BMI model with multiple users at the same time results in undefined behavior. Therefore we have added utilities to launch the BMI server whenever a client is instantiated.

Subprocess
..........
To launch the model service in a python subprocess, type

.. code-block:: python

    from grpc4bmi.bmi_client_subproc import BmiClientSubProcess

    mymodel = BmiClientSubProcess(<PACKAGE>.<MODULE>.<CLASS>)

To launch ``run-bmi-server`` in a python subprocess and automatically listen to the right port. Note that this requires your client to run in the same python environment as your model.

Docker
......

Singularity
...........