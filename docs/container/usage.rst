Using the container clients
===========================

.. _docker_client:

Docker
------

Grpc4bmi can run containers with `Docker engine`_.

Use the :class:`grpc4bmi.bmi_client_docker.BmiClientDocker` class to start a Docker container and get a client to interact with the model running inside the container.



For example the PCR-GLOBWB model can be started in a Docker container with

.. code-block:: python

    model = BmiClientDocker(image='ewatercycle/pcrg-grpc4bmi:latest', image_port=55555,
                            input_dir="./input",
                            output_dir="./output")
    # Interact with model
    model.initialize('config.cfg')

    # Stop container
    del model

.. _Docker engine: https://docs.docker.com/

Singularity
-----------

Grpc4bmi can run containers on `Singularity`_.

The Docker images build :ref:`previously <building-docker-image>` can be either run directly or converted to singularity image file and run.

To run a Docker image directly use `docker://<docker image name>` as singularity image name.

To convert a Docker image to a singularity image file use

.. code-block:: sh

    singularity build  docker://<docker image name> <singularity image filename>


Use the :class:`grpc4bmi.bmi_client_singularity.BmiClientSingularity` class to start a Singularity container and get a client to interact with the model running inside the container.

.. code-block:: python

    from grpc4bmi.bmi_client_singularity import BmiClientSingularity
    image = '<docker image name of grpc4bmi server of a bmi model>'
    client = BmiClientSingularity(image, input_dir='<directory with models input data files>')

For example for the wflow Docker image the commands would be the following

.. code-block:: python

    from grpc4bmi.bmi_client_singularity import BmiClientSingularity
    image = 'docker://ewatercycle/wflow-grpc4bmi:latest'
    client = BmiClientSingularity(image, input_dir='wflow_rhine_sbm', output_dir='wflow_output')

.. _Singularity: https://www.sylabs.io/guides/latest/user-guide/
