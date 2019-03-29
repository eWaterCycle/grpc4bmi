R
=

Grpc4bmi allows you to wrap a Hydrological model written in the `R language`_ into a GRPC server.

.. _R language: https://www.r-project.org/


Installing Requirements
-----------------------

The `bmi-r`_ package can be installed using the following `devtools`_ command

.. code-block:: R

    devtools::install_github("eWaterCycle/bmi-r")


Creating
--------

A model must implement the basic model interface (bmi).

This can be done by sub-classing the AbstractBmi class found in the `bmi-r`_ R package.


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

Running
-------

Once the model has an BMI interface it can be run as a GRPC server by installing the `grpc4bmi[R]` Python package with

.. code-block:: sh

    pip install grpc4bmi[R]

The server can be started with

.. code-block:: sh

    run-bmi-server --lang R [--path <R file with BMI model>] --name [<PACKAGE>::]<CLASS> --port <PORT>

For the WALRUS model the command is

.. code-block:: sh

    run-bmi-server --lang R --path ~/git/eWaterCycle/grpc4bmi-examples/walrus/walrus-bmi.r --name WalrusBmi --port 50051

The Python grpc4bmi :ref:`usage` can then be used to connect to the server.
