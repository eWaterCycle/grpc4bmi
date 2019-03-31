.. _building-docker-image:

Building a docker image
=======================

The biggest advantage of using grpc4bmi is that you can embed the model code in a container like a `Docker`_ image. The grpc bridge allows you to address it from the host machine with the python BMI.

To establish this, install your BMI model and grpc4bmi inside the container, and let ``run-bmi-server`` act as the entry point of the docker image.


Python
------

The docker file for the model container simply contains the installation instructions of grpc4bmi and the BMI-enabled model itself, and as entrypoint the ``run-bmi-server`` command. For the :ref:`python example <python-example>` the Docker file will read

.. code-block:: Dockerfile

    FROM ubuntu:bionic
    MAINTAINER your name <your email address>

    # Install grpc4bmi
    RUN pip install git+https://github.com/eWaterCycle/grpc4bmi.git#egg=grpc4bmi

    # Install here your BMI model:
    RUN git clone <MODEL-URL> /opt/mymodeldir

    # Run bmi server
    ENTRYPOINT ["run-bmi-server", "--name", "mypackage.mymodule.MyBmi", "--path", "/opt/mymodeldir"]

    # Expose the magic grpc4bmi port
    EXPOSE 55555

The port 55555 is the internal port in the Docker container that the model communicates over. It is the default port for ``run_bmi_server`` and also the default port that all clients listen to.

R
-

The Docker image can be made by writing a `Dockerfile` file like

.. code-block:: Dockerfile

    FROM r-base
    LABEL maintainer="Your name <your email address>"

    RUN apt update && apt install -t unstable -y python3-dev python3-pip git && \
      pip3 install git+https://github.com/eWaterCycle/grpc4bmi.git#egg=grpc4bmi[R]

    RUN install.r remotes && installGithub.r eWaterCycle/bmi-r
    RUN install.r <R mymodel library from CRAN>

    # Copy BMI interface of model into Docker image
    RUN mkdir /opt/
    COPY mymodel-bmi.r /opt/

    # Config file and forcing file will be mounted at /data
    RUN mkdir /data
    WORKDIR /data
    VOLUME /data

    ENV BMI_PORT=55555

    CMD ["run-bmi-server", "--lang", "R", "--path", "/opt/mymodel-bmi.r", "--name", "mymodel"]

    EXPOSE 55555


The WALRUS model has a `Dockerfile`_  file which can be used as an example.

.. _Dockerfile: https://github.com/eWaterCycle/grpc4bmi-examples/blob/master/walrus/Dockerfile

C/C++/Fortran
-------------

For native languages you need to compile you BMI model inside the container let your bmi server runner binary program act as the entry point. The protobuf, grpc and grpc4bmi libraries need to be installed in your docker image, which means that the :ref:`installation instructions <install_cpp>` must be adopted in your Docker file. Then, include the installation of the model itself and the bmi run binary that you have written (as described :ref:`here <example_cpp>`). Finally the entry point in the docker file should be the launch of this binary and you should expose port 55555. For the C++ example :ref:`C++ example <example_cpp>`

.. code-block:: Dockerfile

    # ...download, compile and install grpc and grpc4bmi...
    # ...download, compile and install my_bmi_model...
    # Run bmi server
    ENTRYPOINT ["my_bmi_server"]

    # Expose the magic grpc4bmi port
    EXPOSE 55555

Building and Publishing
-----------------------

The Docker image can be build with

.. code-block:: sh

    docker build -t <image name> .

The Docker image can be published at `Docker Hub`_ by creating a repository and pushing it with

.. code-block:: sh

   docker push <image name>

The example WALRUS model is published at https://cloud.docker.com/u/ewatercycle/repository/docker/ewatercycle/walrus-grpc4bmi.

The Docker image can then be started with the grpc4bmi :ref:`docker client <docker_client>`.

.. _Docker: https://docs.docker.com/
.. _Docker Hub: https://hub.docker.com/
