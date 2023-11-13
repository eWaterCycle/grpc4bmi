OpenAPI
=======

Your model might be written in a language which does not have gRPC support. 
In this case, you can use the OpenAPI specifcation to wrap your model in a JSON web service.

Generate spec
-------------

The OpenAPI spec can be generated from the gRPC spec using the `protoc-gen-openapiv2` plugin.
The plugin can be found at https://github.com/grpc-ecosystem/grpc-gateway/

```bash
protoc -I . --openapiv2_out . \
--openapiv2_opt=output_format=yaml \
--openapiv2_opt=generate_unbound_methods=true \
./proto/grpc4bmi/bmi.proto 
```

Generate Python client
----------------------

```bash
npx --package @openapitools/openapi-generator-cli openapi-generator-cli generate -i proto/grpc4bmi/bmi.swagger.yaml -g python -o openapi/python-client
```

Consuming
---------

To consume a web service using the BMI OpenAPI specification, you can use the Python client:

```python
from grpc4bmi.bmi_openapi_client import BmiOpenApiClient
model = BmiOpenApiClient(host='localhost', port=50051, timeout=10)
model.initialize(config_file)
model.update()
```

To spin up a web service inside a container and s client in one go you can use

```python
from grpc4bmi.bmi_openapi_client import BmiOpenApiApptainerClient, BmiOpenApiDockerClient

model = BmiOpenApiApptainerClient(
    image='wflowjl.sif', work_dir='/tmp/workdir', input_dirs=[]
)
model = BmiOpenApiDockerClient(
    image='ghcr.io/eWatercycle/wflowjl', work_dir='/tmp/workdir', input_dirs=[]
)
```

Providing
---------

To provide a web service using the BMI OpenAPI specification you will need to create a web service in the language in which you have your model.

Python
~~~~~~

Generate the server stubs with:

```shell
npx --package @openapitools/openapi-generator-cli openapi-generator-cli generate -i proto/grpc4bmi/bmi.swagger.yaml -g python-fastapi -o openapi/python-server
```

Inside each stub call your corresponding BMI method of your model.

As Python is supported by gRPC, you should not need to use the OpenAPI for Python.

Julia
~~~~~

Generate the server stubs with:

```shell
npx --package @openapitools/openapi-generator-cli openapi-generator-cli generate -i proto/grpc4bmi/bmi.swagger.yaml -g julia-server -o openapi/julia-server
```

Inside each stub call your corresponding BMI method of your model.
