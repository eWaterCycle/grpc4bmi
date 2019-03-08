import pytest

from grpc4bmi.bmi_client_singularity import BmiClientSingularity


@pytest.fixture()
def walrus_model(tmp_path, walrus_input):
    model = BmiClientSingularity(image="docker://ewatercycle/walrus-grpc4bmi", input_dir=tmp_path)
    yield model
    del model


class TestBmiClientDocker:
    def test_component_name(self, walrus_model):
        assert walrus_model.get_component_name() == 'WALRUS'

    def test_initialize(self, walrus_input, walrus_model):
        walrus_model.initialize(walrus_input)
        assert walrus_model.get_current_time() == walrus_model.get_start_time()

    def test_get_value_ref(self, walrus_model):
        with pytest.raises(NotImplementedError):
            walrus_model.get_value_ref('Q')
