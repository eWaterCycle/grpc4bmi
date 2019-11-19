import pytest

from grpc4bmi.bmi_client_docker import BmiClientDocker, LogsException
from grpc4bmi.reserve import reserve_grid_padding, reserve_values


@pytest.fixture()
def walrus_model(tmp_path, walrus_input):
    model = BmiClientDocker(image="ewatercycle/walrus-grpc4bmi:v0.3.1", image_port=55555, input_dir=str(tmp_path))
    yield model
    del model


@pytest.fixture()
def walrus_model_with_extra_volume(tmp_path, walrus_input_on_extra_volume):
    (input_dir, extra_volumes) = walrus_input_on_extra_volume
    model = BmiClientDocker(image="ewatercycle/walrus-grpc4bmi:v0.3.1",
                            image_port=55555,
                            input_dir=str(input_dir),
                            extra_volumes=extra_volumes)
    yield model
    del model


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

    def test_get_value_ref(self, walrus_model):
        with pytest.raises(NotImplementedError):
            walrus_model.get_value_ref('Q')

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
