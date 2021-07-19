import logging
import os
import subprocess
import time
from os.path import abspath
from typing import Iterable, BinaryIO, TextIO, Union

import semver
from typeguard import check_argument_types, qualified_name

from grpc4bmi.bmi_grpc_client import BmiClient

REQUIRED_SINGULARITY_VERSION = '3.6.0'


def check_singularity_version():
    p = subprocess.Popen(['singularity', 'version'], stdout=subprocess.PIPE)
    (stdout, _stderr) = p.communicate()
    if p.returncode != 0:
        raise Exception('Unable to determine singularity version')
    local_version = semver.VersionInfo.parse(stdout.decode('utf-8').replace('_', '-'))
    if local_version < REQUIRED_SINGULARITY_VERSION:
        raise Exception(f'Wrong version ({local_version}) of singularity found, '
                        f'require version {REQUIRED_SINGULARITY_VERSION}')
    return True


class DeadSingularityContainerException(ChildProcessError):
    """
    Exception for when a Singularity container has died.

    Args:
        message (str): Human readable error message
        exitcode (int): The non-zero exit code of the container

    """
    def __init__(self, message, exitcode, *args):
        super().__init__(message, *args)
        #: Exit code of container
        self.exitcode = exitcode


class BmiClientSingularity(BmiClient):
    """BMI GRPC client for singularity server processes
    During initialization launches a singularity container with run-bmi-server as its command.
    The client picks a random port and expects the container to run the server on that port.
    The port is passed to the container using the BMI_PORT environment variable.

    Args:
        image: Singularity image.

            For Docker Hub image use `docker://*` or convert it to a Singularity image file.

            To convert Docker image
            `ewatercycle/walrus-grpc4bmi <https://hub.docker.com/layers/ewatercycle/walrus-grpc4bmi>`_
            with `v0.2.0` tag to `./ewatercycle-walrus-grpc4bmi_v0.2.0.sif` Singularity image file use:

            .. code-block:: console

              singularity pull ewatercycle-walrus-grpc4bmi_v0.2.0.sif docker://ewatercycle/walrus-grpc4bmi:v0.2.0

        input_dirs (Iterable[str]): Directories for input files of model.

            All of directories will be mounted read-only inside Singularity container on same path as outside container.

        work_dir (str): Working directory for model.

            Directory is mounted inside container and changed into.

            To create a random work directory you could use

            .. code-block:: python

              from tempfile import TemporaryDirectory
              from grpc4bmi.bmi_client_singularity import BmiClientSingularity

              work_dir = TemporaryDirectory()

              image = 'ewatercycle-walrus-grpc4bmi_v0.2.0.sif'
              client =  BmiClientSingularity(image, work_dir.name)

              # Write config to work_dir and interact with client

              # After checking output in work_dir, clean up
              work_dir.cleanup()

        delay (int): Seconds to wait for Singularity container to startup, before connecting to it

            Increase when container takes a long time to startup.

        timeout (int): Seconds to wait for gRPC client to connect to server.

            By default will try forever to connect to gRPC server inside container.
            Set to low number to escape endless wait.

        stderr (Union[None, BinaryIO, TextIO, int]): Redirect stderr of singularity container.

            By default will inherit stderr file handle from current Python process.
            Can be set to a file object to log stdout to a file.
            Or can be set to `subprocess.DEVNULL` to redirect to null device never to be seen again.
            Or can be set to `subprocess.STDOUT` to redirect the stderr to stdout.

        stdout (Union[None, BinaryIO, TextIO, int]): Redirect stdout of singularity container.

            By default will inherit stdout file handle from current Python process.
            Can be set to a file object to log stdout to a file.
            Or can be set to `subprocess.DEVNULL` to redirect to null device never to be seen again.

    **Example 1: Config file already inside image**

    MARRMoT has an `example config file <https://github.com/wknoben/MARRMoT/blob/master/BMI/Config/BMI_testcase_m01_BuffaloRiver_TN_USA.mat>`_ inside its Docker image.

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        client = BmiClientSingularity(image='docker://ewatercycle/marrmot-grpc4bmi:latest')
        client.initialize('/opt/MARRMoT/BMI/Config/BMI_testcase_m01_BuffaloRiver_TN_USA.mat')
        client.update_until(client.get_end_time())
        del client

    **Example 2: Config file in input directory**

    The config file and all other files the model needs are in a directory (`/tmp/input`).
    Use `/tmp/work` to capture any output files like logs generated by model.

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        # Generate config file called 'config.mat' in `/tmp/input` directory
        client = BmiClientSingularity(image='docker://ewatercycle/marrmot-grpc4bmi:latest',
                                      input_dirs=['/tmp/input'],
                                      work_dir='/tmp/work')
        client.initialize('/tmp/input/config.mat')
        client.update_until(client.get_end_time())
        del client

    **Example 3: Read only input directory with config file in work directory**

    The forcing data is in a shared read-only location like `/shared/forcings/walrus`.
    In the config file (`/tmp/work/walrus.yml`) point to a forcing data file (`/shared/forcings/walrus/PEQ_Hupsel.dat`).

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        client = BmiClientSingularity(image='ewatercycle-walrus-grpc4bmi_v0.2.0.sif',
                                      input_dirs=['/shared/forcings/walrus'],
                                      work_dir='/tmp/work')
        client.initialize('walrus.yml')
        client.update_until(client.get_end_time())
        del client

    **Example 4: Model writes in sub directory of input directory**

    Some models, for example wflow, write output in a sub-directory of the input directory.
    If the input directory is set with the `input_dirs` argument then the model will be unable to write its output as
    input directories are mounted read-only. That will most likely cause the model to die.
    A workaround is to use the `work_dir` argument with input directory as value instead.
    This will make the whole input directory writable so the model can do its thing.

    When input directory is on a shared disk where you do not have write permission then
    the input dir should be copied to a work directory (`/scratch/wflow`) so model can write.

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        client = BmiClientSingularity(image='docker://ewatercycle/wflow-grpc4bmi:latest',
                                      work_dir='/scratch/wflow')
        client.initialize('wflow_sbm.ini')
        client.update_until(client.get_end_time())
        del client

    **Example 5: Inputs are in multiple directories**

    A model has its forcings (`/shared/forcings/muese`), parameters (`/shared/model/wflow/staticmaps`)
    and config file (`/tmp/work/wflow_sbm.ini`) in different locations.
    The config file should be set to point to the forcing and parameters files.

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        client = BmiClientSingularity(image='docker://ewatercycle/wflow-grpc4bmi:latest',
                                      input_dirs=['/shared/forcings/muese',
                                                  '/shared/model/wflow/staticmaps'],
                                      work_dir='/tmp/work')
        client.initialize('wflow_sbm.ini')
        client.update_until(client.get_end_time())
        del client

    **Example 6: Run model twice with their own work directory**

    While running 2 or models at the same time you do not want the any config or output to be mixed.

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        client_muese = BmiClientSingularity(image='docker://ewatercycle/wflow-grpc4bmi:latest',
                                            work_dir='/scratch/wflow-meuse')
        client_muese.initialize('wflow_sbm.meuse.ini')
        client_rhine = BmiClientSingularity(image='docker://ewatercycle/wflow-grpc4bmi:latest',
                                            work_dir='/scratch/wflow-rhine')
        client_rhine.initialize('wflow_sbm.rhine.ini')
        ...
        # Run models and set/get values
        ...
        del client_muese
        del client_rhine

    """

    def __init__(self, image: str, work_dir: str, input_dirs: Iterable[str] = tuple(), delay=0, timeout=None,
                 stderr: Union[None, BinaryIO, TextIO, int] = None,
                 stdout: Union[None, BinaryIO, TextIO, int] = None
                 ):
        assert check_argument_types()
        if type(input_dirs) == str:
            msg = f'type of argument "input_dirs" must be collections.abc.Iterable; ' \
                  f'got {qualified_name(input_dirs)} instead'
            raise TypeError(msg)
        check_singularity_version()
        host = 'localhost'
        port = BmiClient.get_unique_port(host)
        args = [
            "singularity",
            "run",
            "--contain",
            "--env", f"BMI_PORT={port}"
        ]

        for raw_input_dir in input_dirs:
            input_dir = abspath(raw_input_dir)
            if not os.path.isdir(input_dir):
                raise NotADirectoryError(input_dir)
            args += ["--bind", f'{input_dir}:{input_dir}:ro']
        self.work_dir = abspath(work_dir)
        if self.work_dir in set([abspath(d) for d in input_dirs]):
            raise ValueError('Found work_dir equal to one of the input directories. Please drop that input dir.')
        if not os.path.isdir(self.work_dir):
            raise NotADirectoryError(self.work_dir)
        args += ["--bind", f'{self.work_dir}:{self.work_dir}:rw']
        # Change into working directory
        args += ["--pwd", self.work_dir]
        args.append(image)
        logging.info(f'Running {image} singularity container on port {port}')
        self.container = subprocess.Popen(args, preexec_fn=os.setsid, stderr=stderr, stdout=stdout)
        time.sleep(delay)
        returncode = self.container.poll()
        if returncode is not None:
            raise DeadSingularityContainerException(f'singularity container {image} prematurely exited with code {returncode}', returncode)
        super(BmiClientSingularity, self).__init__(BmiClient.create_grpc_channel(port=port, host=host), timeout=timeout)

    def __del__(self):
        if hasattr(self, "container"):
            self.container.terminate()
            self.container.wait()

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
