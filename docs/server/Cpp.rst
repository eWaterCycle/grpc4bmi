C/C++/Fortran
=============

Installing Requirements
-----------------------
For native programming languages it is necessary to install and compile the C++ bindings of GRPC and protobuf on your system:

.. code-block:: sh

    $ git clone -b $(curl -L https://grpc.io/release) --depth=1 https://github.com/grpc/grpc
    $ cd grpc && git submodule update --init --recursive
    $ sudo make install && cd third_party/protobuf && sudo make install

You will also need to compile the bmi-c and grpc4bmi

.. code-block:: sh

    $ git clone --depth=1 https://github.com/eWaterCycle/grpc4bmi.git
    $ cd grpc4bmi && git submodule update --init --recursive
    $ cd cpp/bmi-c && mkdir -p build && cd build
    $ cmake .. && sudo make install
    $ mkdir -p ../../build && cd ../../build && cmake .. && sudo make install


Creating
--------

The grpc4bmi package comes with a C++ abstract base class that contains the BMI functions. The `header file <https://github.com/eWaterCycle/grpc4bmi/blob/master/cpp/bmi_class.h>`_ will
be copied to your system include path upon the installation steps above.

Running
-------

Example
-------