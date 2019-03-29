R model
=======

Grpc4bmi allows you to wrap a Hydrological model written in the `R language`_ into a GRPC server.

.. _R language: https://www.r-project.org/

BMI interface
-------------

A model must implement the basic model interface (bmi).

This can be done by sub-classing the AbstractBmi class found in the `bmi-r`_ R package.

The `bmi-r`_ package can be installed using the following `devtools`_ command

.. code-block:: R

    devtools::install_github("eWaterCycle/bmi-r")


A model (in the example called `mymodel`) can than be given a basic model interface with something like

.. code-block:: R

    library(R6)
    library(bmi)
    library(mymodel)

    MyModelBmi <- R6Class(
        inherit = AbstractBmi,
        public = list(
            getComponentName = function() return('mymodel'),
            bmi_initialize = function(config_file) {
                # TODO Construct & initialize mymodel model
            },
            update = function() {
                # TODO evolve mymodel model to next time step
            },
            # TODO implement all other bmi functions
        )
    )


For an example of a BMI interface of the `Wageningen Lowland Runoff Simulator (WALRUS)`_ see `walrus-bmi.r`_

.. _bmi-r: https://github.com/eWaterCycle/bmi-r
.. _devtools: https://devtools.r-lib.org/
.. _Wageningen Lowland Runoff Simulator (WALRUS): https://github.com/ClaudiaBrauer/WALRUS
.. _walrus-bmi.r: https://github.com/eWaterCycle/grpc4bmi-examples/blob/master/walrus/walrus-bmi.r

GRPC server of BMI model
------------------------

Once the model has an BMI interface it can be run as a GRPC server by installing the `grpc4bmi[R]` Python package with

.. code-block:: sh

    pip install grpc4bmi[R]

The server can be started with

.. code-block:: sh

    run-bmi-server --lang R [--path <R file with BMI model>] --name [<PACKAGE>::]<CLASS> --port <PORT>

For the WALRUS model the command is

.. code-block:: sh

    run-bmi-server --lang R --path ~/git/eWaterCycle/grpc4bmi-examples/walrus/walrus-bmi.r --name WalrusBmi --port 50051

The Python grpc4bmi :ref:`python-grpc4bmi-client` can then be used to connect to the server.

Containerized GRPC server
-------------------------

To easily run a GRPC server it is handy to put it in a container like a `Docker`_ image.

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

    docker build -t mymodel-grpc4bmi .

The Docker image can be published at `Docker Hub`_ by creating a repository and pushing it with

.. code-block:: sh

   docker push mymodel-grpc4bmi

The WALRUS model is published at https://cloud.docker.com/u/ewatercycle/repository/docker/ewatercycle/walrus-grpc4bmi.

The Docker image can then be started with :class:`grpc4bmi.bmi_client_docker.BmiClientDocker` or :class:`grpc4bmi.bmi_client_singularity.BmiClientSingularity`.

.. _Docker: https://docs.docker.com/
.. _Dockerfile: https://github.com/eWaterCycle/grpc4bmi-examples/blob/master/walrus/Dockerfile
.. _Docker Hub: https://hub.docker.com/
