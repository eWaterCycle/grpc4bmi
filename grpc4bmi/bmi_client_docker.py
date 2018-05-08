import docker

from grpc4bmi.bmi_grpc_client import BmiClient


class BmiClientDocker(BmiClient):

    def __init__(self, image, host=None, input_dir=None, output_dir=None):
        client = docker.from_env()
        port = BmiClient.get_unique_port()
        volumes = {}
        if input_dir is not None:
            volumes[input_dir] = {"bind": "/data/input", "mode": "ro"}
        if output_dir is not None:
            volumes[output_dir] = {"bind": "/data/output", "mode": "rw"}
        self.container = client.containers.run(image, ports={"50051/tcp": port},
                                               volumes=volumes,
                                               detach=True)
        super(BmiClientDocker, self).__init__(BmiClient.create_grpc_channel(port=port, host=host))

    def __del__(self):
        self.container.stop()

    def get_value_ref(self, var_name):
        raise NotImplementedError("Cannot exchange memory references across process boundary")
