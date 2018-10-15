import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name="grpc4bmi",
      version="0.2",
      author="Gijs van den Oord",
      author_email="g.vandenoord@esciencecenter.nl",
      description="Run your BMI implementation in a separate process and expose it as BMI-python with GRPC",
      license="Apache License, Version 2.0",
      url="https://github.com/eWaterCycle/grpc4bmi",
      packages=find_packages(),
      include_package_data=True,
      long_description=read("README.md"),
      entry_points={"console_scripts": [
          "run-bmi-server =  grpc4bmi.run_server:main"
      ]},
      install_requires=[
          "grpcio",
          "grpcio-reflection",
          "protobuf",
          "numpy",
          'futures; python_version == "2.7"',
          "docker",
          "basic-modeling-interface",
      ],
      extras_require={
          'R': ['rpy2'],
      },
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Science/Research",
                   "Programming Language :: Python",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3.5",
                   "Topic :: Utilities",
                   "Topic :: Scientific/Engineering",
                   "License :: OSI Approved :: Apache Software License"
                   ],
      )
