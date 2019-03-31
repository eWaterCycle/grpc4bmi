C/C++/Fortran
=============

.. _install_cpp:

Installing Requirements
-----------------------
For native programming languages it is necessary to install and compile the C++ bindings of GRPC and protobuf on your system:

.. code-block:: sh

    git clone -b $(curl -L https://grpc.io/release) --depth=1 https://github.com/grpc/grpc
    cd grpc && git submodule update --init --recursive
    sudo make install && cd third_party/protobuf && sudo make install

You will also need to compile the bmi-c and grpc4bmi

.. code-block:: sh

    git clone --depth=1 https://github.com/eWaterCycle/grpc4bmi.git
    cd grpc4bmi && git submodule update --init --recursive
    cd cpp/bmi-c && mkdir -p build && cd build
    cmake .. && sudo make install
    mkdir -p ../../build && cd ../../build && cmake .. && sudo make install


Creating
--------

The grpc4bmi package comes with a C++ abstract base class that contains the BMI functions. The `header file <https://github.com/eWaterCycle/grpc4bmi/blob/master/cpp/bmi_class.h>`_ will
be copied to your system include path upon the installation steps above. Write an implementation of the ``Bmi`` class using your model time step code and data structures. You don't have to worry about global variables in your model code: with grpc4bmi every model instance runs in its own memory space. For the same reason, the ``get_value_ptr`` and ``set_value_ptr`` methods can be safely ignored, they are never called through the grpc process bridge.

Running
-------

Since native language lack reflection, it is necessary to make your own ``run_bmi_server`` program. We provide a function ``run_bmi_server(Bmi*, int*, char*)`` in the ``bmi_grpc_server.h`` header that can be called with your model instance (see the example below). To compile your server binary, it is necessary to link against grpc4bmi and protobuf libraries.

.. _example_cpp:

Example
-------

To create a BMI to your model, write a header file in which you declare the overridden functions of the base class ``Bmi`` in the included file ``bmi_class.h``.

my_bmi_model.h:

.. code-block:: cpp

    #include <bmi_class.h>

    class MyBmiModel: public Bmi
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
