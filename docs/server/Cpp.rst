C/C++/Fortran
=============

.. _install_cpp:

Installing Requirements
-----------------------
For native programming languages it is necessary to install and compile the C++ bindings of GRPC and protobuf on your system:

.. code-block:: sh

    git clone -b $(curl -L https://grpc.io/release) --depth=1 https://github.com/grpc/grpc
    cd grpc
    git submodule update --init --recursive
    wget -q -O cmake-linux.sh https://github.com/Kitware/CMake/releases/download/v3.16.5/cmake-3.16.5-Linux-x86_64.sh
    sudo sh cmake-linux.sh -- --skip-license --prefix=/usr/local
    rm cmake-linux.sh
    mkdir cmake/build && cd cmake/build
    /usr/local/bin/cmake ../.. -DgRPC_INSTALL=ON -DgRPC_SSL_PROVIDER=package -DgRPC_BUILD_TESTS=OFF -DBUILD_SHARED_LIBS=ON
    sudo make -j4 install
    sudo ldconfig

You will also need the install the BMI C and C++ headers

.. code-block:: sh

    git clone -b v2.0 https://github.com/csdms/bmi-cxx.git bmi-cxx
    cd bmi-cxx && mkdir build && cd build cmake .. && make install

    git clone -b v2.1 https://github.com/csdms/bmi-c.git bmi-c
    cd bmi-c && mkdir build && cd build cmake .. && make install

You will also need to compile grpc4bmi

.. code-block:: sh

    git clone --depth=1 https://github.com/eWaterCycle/grpc4bmi.git
    cd grpc4bmi && git submodule update --init
    cd cpp
    mkdir -p build && cd build && cmake .. && sudo make install


Creating
--------

The grpc4bmi package requires a model implementing the BMI interface in 
`C with bmi.h <https://github.com/csdms/bmi-c/blob/v2.1/bmi.h>`_ 
or `C++ with bmi.hxx <https://github.com/csdms/bmi-cxx/blob/v2.0/bmi.hxx>`_. 
The header files will
be copied to your system include path upon the installation steps above. 
Write an implementation of the ``Bmi`` class using your model time step code and data structures. 
You don't have to worry about global variables in your model code: 
with grpc4bmi every model instance runs in its own memory space. 
For the same reason, the ``get_value_ptr`` and ``set_value_ptr`` methods can be safely ignored, 
they are never called through the grpc network protocol.

Running
-------

Since native language lack reflection, it is necessary to make your own ``run_bmi_server`` program. 
We provide a function ``run_bmi_server(Bmi*, int*, char*)`` in the ``bmi_grpc_server.h`` header 
that can be called with your model instance (see the example below). To compile your server binary, 
it is necessary to link against grpc4bmi and protobuf libraries.
The program will accept a single optional argument which is the port the server will run on.
The port can also be specified using the BMI_PORT environment variable. The default port is 50051.

.. _example_cpp:

Example in C
------------

To create a BMI to your model, write a header file in which you declare the overridden functions of the base class ``Bmi`` in the included file ``bmi.h``.

my_bmi_model.h:

.. code-block:: cpp

    #include <bmi.h>

    class MyBmiModel: public bmi::Bmi
    {
        public:
            MyBmiModel();
            int initialize(const char* config_file) override;
            ...
            int get_component_name(char* name) const override;
    };

Write your implementation of the basic modeling interface in the corresponding source file

my_bmi_model.cc:

.. code-block:: cpp

    #include <my_bmi_model.h>
    #include <cstring>

    MyBmiModel::MyBmiModel(){}
    int MyBmiModel::initialize(const char* config_file)
    {
        /* ...initialize the model from config_file... */
        return BMI_SUCCESS;
    }
    ...
    int MyBmiModel::get_component_name(char* name) const
    {
        strcpy(name, "Hello world");
        return BMI_SUCCESS;
    }

Now the BMI server can be simply be implemented as

run_my_bmi_model.cc:

.. code-block:: cpp

    #include "bmi_grpc_server.h"
    #include "my_bmi_model.h"

    int main(int argc, char* argv[])
    {
        Bmi* model = new HypeBmi();
        run_bmi_server(model, argc, argv);
        delete model;
        return 0;
    }

This binary will need to be linked against grpc4bmi and the protobuf libraries:

.. code-block:: sh

    g++ -o my_bmi_server run_my_bmi_model.o my_bmi_model.o `pkg-config --libs protobuf grpc++ grpc` -Wl,--no-as-needed -lgrpc++_reflection -ldl -lgrpc4bmi



Fortran
.......

In case you have a Fortran model, we advice to write the corresponding functions in Fortran first and export them to the implementation, e.g.

my_bmi_model.f90:

.. code-block:: fortran

    subroutine get_component_name(name) bind(c, name="get_component_name_f")
        use, intrinsic ::iso_c_binding
        implicit none
        character(kind=c_char), intent(out) :: name(*)
        name(1:11)="Hello world"
        name(12)=c_null_char

Now it is possible to call this function from the BMI C implementation as follows,

my_bmi_model.cc:

.. code-block:: cpp

    extern "C" void get_component_name_f(char*)
    int MyBmiModel::get_component_name(char* name) const
    {
        get_component_name_f(name);
        return BMI_SUCCESS;
    }
