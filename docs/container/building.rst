Building a docker image
=======================

To easily run a GRPC server it is handy to put it in a container like a `Docker`_ image.

The grpc bridge between processes allows you to containerize your model and address it from the host machine with the python BMI. For this we use the mapping feature of network ports that docker provides.

To establish this, install your BMI model in a docker container. Then follow the installation steps above to install grpc4bmi inside the container, and let ``run-bmi-server`` act as the entry point of the docker image.


Python
------
R
------

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

The Docker image can be build with

.. code-block:: sh

    docker build -t <image name> .

.. _Dockerfile: https://github.com/eWaterCycle/grpc4bmi-examples/blob/master/walrus/Dockerfile

C/C++/Fortran
-------------

Publishing
----------

The Docker image can be published at `Docker Hub`_ by creating a repository and pushing it with

.. code-block:: sh

   docker push <image name>

The example WALRUS model is published at https://cloud.docker.com/u/ewatercycle/repository/docker/ewatercycle/walrus-grpc4bmi.

The Docker image can then be started with :class:`grpc4bmi.bmi_client_docker.BmiClientDocker` or :class:`grpc4bmi.bmi_client_singularity.BmiClientSingularity`.

.. _Docker: https://docs.docker.com/
.. _Docker Hub: https://hub.docker.com/
