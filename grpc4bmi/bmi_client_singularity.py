import os
import time
from os.path import abspath
import subprocess
import logging

import semver

from grpc4bmi.bmi_grpc_client import BmiClient

REQUIRED_SINGULARITY_VERSION = '>=3.6.0'


def check_singularity_version():
    p = subprocess.Popen(['singularity', 'version'], stdout=subprocess.PIPE)
    (stdout, _stderr) = p.communicate()
    if p.returncode != 0:
        raise Exception('Unable to determine singularity version')
    if not semver.match(stdout.decode('utf-8').replace('_', '-'), REQUIRED_SINGULARITY_VERSION):
        raise Exception(f'Wrong version of singularity found, require version {REQUIRED_SINGULARITY_VERSION}')
    return True


class BmiClientSingularity(BmiClient):
    """BMI GRPC client for singularity server processes
    During initialization launches a singularity container with run-bmi-server as its command.
    The client picks a random port and expects the container to run the server on that port.
    The port is passed to the container using the BMI_PORT environment variable.

    Args:
        image: Singularity image. For Docker Hub image use `docker://*`.
        input_dirs (Iterable[str]): Input directories on host computer.

            All of them will be mounted read-only inside Singularity container on same path as outside container.

        work_dir (Optional[str]): Working directory for model.

            Directory is mounted inside container and changed into.
            If absent then Singularity defaults to using current working directory outside container also inside.

        timeout (int): Seconds to wait for gRPC client to connect to server
        delay (int): Seconds to wait for Singularity container to startup, before connecting to it

    **Example 1: Config file already inside image**

    MARRMoT has an example config file inside its Docker image.

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        client = BmiClientSingularity(image='docker://ewatercycle/marrmot-grpc4bmi:latest')
        client.initialize('/opt/MARRMoT/BMI/Config/BMI_testcase_m01_BuffaloRiver_TN_USA.mat')
        client.update_until(client.get_end_time())
        del client

    **Example 2: Config file in input directory**

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        # Generate config file called 'config.mat' in `/tmp/input` directory
        client = BmiClientSingularity(image='docker://ewatercycle/marrmot-grpc4bmi:latest',
                                      input_dirs=['/tmp/input'])
        client.initialize('/tmp/input/config.mat')
        client.update_until(client.get_end_time())
        del client

    **Example 3: Read only input directory with config file in work directory**

    The forcing data is in a shared read-only location like `/shared/forcings/walrus`.
    In the config file (`/tmp/work/walrus.yml`) point to a forcing data file (``/shared/forcings/walrus/PEQ_Hupsel.dat``).

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        client = BmiClientSingularity(image='docker://ewatercycle/walrus-grpc4bmi:v0.2.0',
                                      input_dirs=['/shared/forcings/walrus'],
                                      work_dir='/tmp/work')
        client.initialize('walrus.yml')
        client.update_until(client.get_end_time())
        del client

    **Example 4: Model writes in sub directory of input directory**

    The input directories are mounted read-only so use writable work directory instead.
    When input directory is read-only to the user then
    the input dir should be copied to a work directory (`/scratch/wflow`) so model can write.

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        client = BmiClientSingularity(image='docker://ewatercycle/wflow-grpc4bmi:latest',
                                      work_dir='/scratch/wflow')
        client.initialize('wflow_sbm.ini')
        client.update_until(client.get_end_time())
        del client

    **Example 5: Inputs are in multiple directories**

    A model has its forcings (`/shared/forcings/muese/`), parameters (`/shared/model/wflow/staticmaps`)
    and config file (`/tmp/work/wflow_sbm.ini`) in different locations.
    The config file should be set to point to the forcing and parameters files.

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        client = BmiClientSingularity(image='docker://ewatercycle/wflow-grpc4bmi:latest',
                                      input_dirs=['/shared/forcings/muese', '/shared/model/wflow/staticmaps'],
                                      work_dir='/tmp/work')
        client.initialize('wflow_sbm.ini')
        client.update_until(client.get_end_time())
        del client

    **Example 6: Run model twice with their own work directory**

    While running 2 or models at the same time you do not want the any config or output to be mixed.

    .. code-block:: python

        from grpc4bmi.bmi_client_singularity import BmiClientSingularity
        client_muese = BmiClientSingularity(image='docker://ewatercycle/wflow-grpc4bmi:latest',
                                            work_dir='/scratch/wflow-muese')
        client_muese.initialize('wflow_sbm.muese.ini')
        client_rhine = BmiClientSingularity(image='docker://ewatercycle/wflow-grpc4bmi:latest',
                                            work_dir='/scratch/wflow-rhine')
        client_rhine.initialize('wflow_sbm.rhine.ini')
        ...
        # Run models and set/get values
        ...
        del client_muese
        del client_rhine

    """
    def __init__(self, image, input_dirs=tuple(), work_dir=None, timeout=None, delay=0):
        check_singularity_version()
        host = 'localhost'
        port = BmiClient.get_unique_port(host)
        args = [
            "singularity",
            "run",
            "--env", f"BMI_PORT={port}"
        ]
        for raw_input_dir in input_dirs:
            input_dir = abspath(raw_input_dir)
            if not os.path.isdir(input_dir):
                raise NotADirectoryError(input_dir)
            args += ["--bind", f'{input_dir}:{input_dir}:ro']
        if work_dir is not None:
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
        self.container = subprocess.Popen(args, preexec_fn=os.setsid)
        time.sleep(delay)
        super(BmiClientSingularity, self).__init__(BmiClient.create_grpc_channel(port=port, host=host), timeout=timeout)

    def __del__(self):
        if hasattr(self, "container"):
            self.container.terminate()
            self.container.wait()

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
