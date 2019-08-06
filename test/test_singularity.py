import pytest

from grpc4bmi.bmi_client_singularity import BmiClientSingularity
from grpc4bmi.reserve import reserve_grid_padding


@pytest.fixture()
def walrus_model(tmp_path, walrus_input):
    model = BmiClientSingularity(image="docker://ewatercycle/walrus-grpc4bmi:v0.3.1", input_dir=str(tmp_path))
    yield model
    del model


class TestBmiClientDocker:
    def test_component_name(self, walrus_model):
        assert walrus_model.get_component_name() == 'WALRUS'

    def test_initialize(self, walrus_input, walrus_model):
        walrus_model.initialize(str(walrus_input))
        assert walrus_model.get_current_time() == walrus_model.get_start_time()

    def test_get_value_ref(self, walrus_model):
        with pytest.raises(NotImplementedError):
            walrus_model.get_value_ref('Q')

    def test_get_grid_origin(self, walrus_input, walrus_model):
        walrus_model.initialize(str(walrus_input))
        grid_id = walrus_model.get_var_grid('Q')

        assert len(walrus_model.get_grid_origin(grid_id, reserve_grid_padding(walrus_model, grid_id))) == 2
