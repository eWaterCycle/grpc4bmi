Using the container clients
===========================

Docker
------

Singularity
-----------

.. code-block:: python

    from grpc4bmi.bmi_client_singularity import BmiClientSingularity
    image = '<docker image name of grpc4bmi server of a bmi model>'
    client = BmiClientSingularity(image, input_dir='<directory with models input data files>')

For example for the wflow Docker image the commands would be the following

.. code-block:: python

    from grpc4bmi.bmi_client_singularity import BmiClientSingularity
    image = 'docker://ewatercycle/wflow-grpc4bmi:latest'
    client = BmiClientSingularity(image, input_dir='wflow_rhine_sbm', output_dir='wflow_output')
