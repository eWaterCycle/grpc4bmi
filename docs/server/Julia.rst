Julia
=====

Grpc4bmi allows you to wrap a Hydrological model written in the `Julia language`_ into a GRPC server.

.. _Julia language: https://julialang.org/

Creating
--------

The model should implement `BasicModelInterface.jl`_.

.. _BasicModelInterface.jl: https://github.com/Deltares/BasicModelInterface.jl

See `Wflow.jl`_ for an example.

.. _Wflow.jl: https://deltares.github.io/Wflow.jl/dev/

Running
-------

Once the model has an BMI interface it can be run as a GRPC server by installing the `grpc4bmi[julia]` Python package with

.. code-block:: bash

    pip install grpc4bmi[julia]

The model Julia package must be installed in the Julia environment managed by juliacall,
for Wflow use

.. code-block:: bash

    python3 -c 'from grpc4bmi.bmi_julia_model import install;install("Wflow")'

The server can be started with

.. code-block:: sh

    run-bmi-server --lang julia --name <MODEL-NAME> --port <PORT>

For example with [Wflow.jl](https://github.com/Deltares/Wflow.jl/) use

.. code-block:: sh

    run-bmi-server --lang julia --name Wflow.Model --port 55555

The Python grpc4bmi :ref:`usage` can then be used to connect to the server.
