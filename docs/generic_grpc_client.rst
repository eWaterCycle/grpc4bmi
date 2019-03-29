Test server with universal grpc command line client
===================================================

Once you have started a GRPC server you can test it is running by using the `Polyglot - a universal grpc command line client`_.

Polyglot requires Java and the `polglot.yar` file can be downloaded at https://github.com/dinowernli/polyglot/releases

The following commands expects a GRPC server running on localhost on port 55555.

To get the component name use

.. code-block::

   echo '{}' | java -jar polyglot.jar call --endpoint=localhost:55555 --full_method=bmi.BmiService/getComponentName

.. _Polyglot - a universal grpc command line client: https://github.com/grpc-ecosystem/polyglot
