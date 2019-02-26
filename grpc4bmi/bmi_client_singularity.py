import errno
import os
from os.path import abspath, expanduser
import shutil
import subprocess
import sys
import time

from grpc4bmi.bmi_grpc_client import BmiClient


class BmiClientSingularity(BmiClient):
    """
    BMI GRPC client for singularity server processes:
    During initialization launches a singularity container with run-bmi-server as its command.
    Also it exposes a

    >>> from grpc4bmi.bmi_client_singularity import BmiClientSingularity
    >>> image = 'docker://ewatercycle/wflow-grpc4bmi:latest'
    >>> client = BmiClientSingularity(image, input_dir='wflow_rhine_sbm', output_dir='wflow_output')
    >>> client.initialize('wflow_rhine_sbm/wflow_sbm.ini')
    >>> client.update_until(client.get_end_time())
    >>> del client

    """
    INPUT_MOUNT_POINT = "/data/input"
    OUTPUT_MOUNT_POINT = "/data/output"

    def __init__(self, image, port=None, input_dir=None, output_dir=None):
        host = 'localhost'
        if port is None:
            port = BmiClient.get_unique_port(host)
        args = [
            "singularity",
            "exec",
        ]
        if input_dir is not None:
            self.input_dir = abspath(input_dir)
            args += ["--bind", input_dir + ':' + BmiClientSingularity.INPUT_MOUNT_POINT]
        if output_dir is not None:
            self.output_dir = abspath(output_dir)
            try:
                # Create output dir ourselves or singularity will complain
                os.mkdir(self.output_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            args += ["--bind", output_dir + ':' + BmiClientSingularity.OUTPUT_MOUNT_POINT]
        args += [
            image,
            "run-bmi-server",
            "--port", str(port)
        ]
        self.pipe = subprocess.Popen(args, stderr=sys.stderr, stdout=sys.stdout)
        # TODO wait for bmi-server to be up and running
        time.sleep(1)
        super(BmiClientSingularity, self).__init__(BmiClient.create_grpc_channel(port=port, host=host))

    def __del__(self):
        self.pipe.terminate()
        self.pipe.wait()

    def initialize(self, filename):
        fn = filename
        is_filename_inside_input_dir = abspath(self.input_dir) < abspath(filename)
        if is_filename_inside_input_dir:
            # Replace input dir outside container by input dir inside container
            fn = abspath(filename).replace(abspath(self.input_dir), BmiClientSingularity.INPUT_MOUNT_POINT)
        is_filename_inside_home_dir = expanduser('~') < abspath(filename)
        if is_filename_inside_home_dir:
            # Singularity has home dir mounted, so valid filename should be available inside container
            # Make absolute because current working dir can be different inside image
            fn = abspath(filename)
        if not is_filename_inside_input_dir and not is_filename_inside_home_dir and self.input_dir is not None:
            # Copying filename inside input dir
            shutil.copy(filename, self.input_dir)
            fname = os.path.basename(filename)
            fn = os.path.join(BmiClientSingularity.OUTPUT_MOUNT_POINT, fname)
        super(BmiClientSingularity, self).initialize(fn)

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
