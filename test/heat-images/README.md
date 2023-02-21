# Heat container images

Heat is a simple model that solves the diffusion equation on a uniform rectangular plate with Dirichlet boundary conditions.

Heat is implemented in [different languages](https://github.com/csdms?q=bmi-example&type=all&language=&sort=).

This directory has the heat model wrapped up in a Docker container image with different combinations of

- language
- bmi version
- grpc4bmi version
- Python Protobuf version

| Directory           | Language | BMI version | grpc4bmi version     | Python protobuf version |
| ------------------- | -------- | ----------- | -------------------- | ----------------------- |
| c-bmi20             | C        | 2.0         | 0.3.x                |                         |
| cxx-bmi20           | C++      | 2.0         | 0.3.x                |                         |
| python-bmi02        | Python   | 0.2         | 0.2.x                | 3                       |
| python-bmi02-legacy | Python   | 0.2         | 0.3.x in legacy mode | 3                       |
| python-bmi20        | Python   | 2.0         | 0.3.x                | 3                       |
| python-bmi20-pb4    | Python   | 2.0         | 0.3.x                | 4                       |

The images can be build with

```shell
docker compose build
```

The images can be tested using [heat_tester.py](heat_tester.py).

To test Python Protobuf version client/server communication, the heat_tester.py (aka client) should be run with grpc4bmi installed from branch:

1. latest-protobuf, uses Python protobuf v4
2. bmi2, uses Python protobuf v3
