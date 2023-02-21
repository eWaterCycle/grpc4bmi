# Heat container images

Heat is a simple model that solves the diffusion equation on a uniform rectangular plate with Dirichlet boundary conditions.

Heat is implemented in [different languages](https://github.com/csdms?q=bmi-example&type=all&language=&sort=).

This directory has the heat model wrapped up in a Docker container image with different combinations of
* language
  * python, https://github.com/csdms/bmi-example-python
  * c,  https://github.com/csdms/bmi-example-c
  * c++, https://github.com/csdms/bmi-example-cxx
* bmi version
  * 0.2
  * 2.0
* grpc4bmi version
  * 0.2.x
  * 0.3.x in legacy mode
  * 0.3.x
* Python Protobuf version
  * 3
  * 4

Each combination has its own sub-directory.

The images can be build with

```shell
docker compose build
```

The images can be tested using [heat_tester.py](heat_tester.py).
