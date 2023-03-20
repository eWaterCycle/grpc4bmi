Using the container clients
===========================

.. _docker_client:

Docker
------

Grpc4bmi can run containers with `Docker engine`_.

Use the :class:`grpc4bmi.bmi_client_docker.BmiClientDocker` class to start a Docker container and get a client to interact with the model running inside the container.

For example the PCR-GLOBWB model can be started in a Docker container with

.. code-block:: python

    from grpc4bmi.bmi_client_docker import BmiClientDocker

    model = BmiClientDocker(image='ewatercycle/pcrg-grpc4bmi:latest', image_port=55555,
                            work_dir="./input")
    # Interact with model
    model.initialize('config.cfg')

    # Stop container
    del model

.. _Docker engine: https://docs.docker.com/

.. _Singularity-section:

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
    input_dir = '<directory with models input data files>'
    work_dir = '<directory where model can write output files>'
    client = BmiClientSingularity(image, work_dir, input_dirs=[input_dir])

     # Interact with model
    client.initialize('<absolute path to config file in the input directory>')

    # Stop container
    del client

For example for the wflow Docker image the commands would be the following

.. code-block:: python

    from grpc4bmi.bmi_client_singularity import BmiClientSingularity

    image = 'docker://ewatercycle/wflow-grpc4bmi:latest'
    work_dir = '/tmp/run1'
    client = BmiClientSingularity(image, work_dir, input_dirs=['/scratch/input/wflow_rhine_sbm'])

     # Interact with model
    client.initialize('/scratch/input/wflow_rhine_sbm/wflow_sbm_bmi.ini')

    # Stop container
    del client


.. _Singularity: https://www.sylabs.io/guides/latest/user-guide/

Apptainer
---------

Grpc4bmi can run containers on `Apptainer`_.

Apptainer is an open source fork of singularity.

Apptainer behaves very similar to singularity so everything described in :ref:`Singularity-section` chapter also goes for Apptainer.
You will need to replace the `singularity` command with `apptainer` and :class:`grpc4bmi.bmi_client_singularity.BmiClientSingularity` class with
:class:`grpc4bmi.bmi_client_apptainer.BmiClientApptainer` class.

.. _Apptainer: https://apptainer.org/docs/user/main/

Sharing files between host computer and container
-------------------------------------------------

Containers run in an isolated file system and by default can not read/write any files on host computer.
To get a directory on your host computer inside a container you have mount them with `input_dirs` and
`work_dir` arguments of :py:class:`grpc4bmi.bmi_client_docker.BmiClientDocker` and
:py:class:`grpc4bmi.bmi_client_singularity.BmiClientSingularity`.

See :py:class:`grpc4bmi.bmi_client_singularity.BmiClientSingularity` for examples using `input_dirs` and `work_dir`.

Support for legacy container images
-----------------------------------

A legacy container image is an image with grpc4bmi version < 0.3 inside,
which uses BMI v0.2.
The grpc4bmi version >= 0.3 uses BMI v2.0.
These legacy container images can be called with grpc4bmi>=0.3,
but some methods will not work, see :ref:`Legacy version` for list.
