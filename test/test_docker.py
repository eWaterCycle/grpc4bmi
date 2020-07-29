from io import BytesIO

import docker
import pytest

from grpc4bmi.bmi_client_docker import BmiClientDocker, DeadDockerContainerException
from grpc4bmi.reserve import reserve_grid_padding, reserve_values

walrus_docker_image = 'ewatercycle/walrus-grpc4bmi:v0.3.1'


@pytest.fixture()
def walrus_model(tmp_path, walrus_input):
    model = BmiClientDocker(image=walrus_docker_image, image_port=55555, input_dir=str(tmp_path))
    yield model
    del model


@pytest.fixture()
def walrus_model_with_extra_volume(tmp_path, walrus_input_on_extra_volume):
    (input_dir, extra_volumes) = walrus_input_on_extra_volume
    model = BmiClientDocker(image=walrus_docker_image,
                            image_port=55555,
                            input_dir=str(input_dir),
                            extra_volumes=extra_volumes)
    yield model
    del model


@pytest.fixture()
def exit_container():
    client = docker.from_env()
    prog = "import sys;print('my stderr log message', file=sys.stderr);print('my stdout log message');sys.exit(25)"
    dockerfile = BytesIO(f'FROM {walrus_docker_image}\nCMD ["python3", "-c", "{prog}" ]\n'.encode())
    image, logs = client.images.build(fileobj=dockerfile)
    yield image.id
    client.images.remove(image.id, force=True)


class TestBmiClientDocker:
    def test_component_name(self, walrus_model):
        assert walrus_model.get_component_name() == 'WALRUS'

    def test_get_grid_origin(self, walrus_input, walrus_model):
        walrus_model.initialize(str(walrus_input))
        grid_id = walrus_model.get_var_grid('Q')

        result = reserve_grid_padding(walrus_model, grid_id)
        assert len(walrus_model.get_grid_origin(grid_id, result)) == 2

    def test_initialize(self, walrus_input, walrus_model):
        walrus_model.initialize(str(walrus_input))
        assert walrus_model.get_current_time() == walrus_model.get_start_time()

    def test_get_value_ptr(self, walrus_model):
        with pytest.raises(NotImplementedError):
            walrus_model.get_value_ptr('Q')

    def test_extra_volume(self, walrus_model_with_extra_volume):
        walrus_model_with_extra_volume.initialize('/data/input/config.yml')
        walrus_model_with_extra_volume.update()

        # After initialization and update the forcings have been read from the extra volume
        result = reserve_values(walrus_model_with_extra_volume, 'Q')
        assert len(walrus_model_with_extra_volume.get_value('Q', result)) == 1

    def test_get_var_location(self, walrus_model):
        assert walrus_model.get_var_location('Q') == 'node'

    def test_logs(self, walrus_model):
        lg = walrus_model.logs()
        assert b"Loading required package:" in lg

    def test_inputdir_absent(self, tmp_path):
        dirthatdoesnotexist = 'dirthatdoesnotexist'
        input_dir = tmp_path / dirthatdoesnotexist
        with pytest.raises(NotADirectoryError, match=dirthatdoesnotexist):
            BmiClientDocker(image=walrus_docker_image, image_port=55555, input_dir=str(input_dir))

    def test_container_start_failure(self, exit_container):
        expected = r"Failed to start Docker container with image"
        with pytest.raises(DeadDockerContainerException, match=expected) as excinfo:
            BmiClientDocker(image=exit_container)

        assert excinfo.value.exitcode == 25
        assert b'my stderr' in excinfo.value.logs
        assert b'my stdout' in excinfo.value.logs
