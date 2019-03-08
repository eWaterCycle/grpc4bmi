import pytest

from grpc4bmi.bmi_client_docker import BmiClientDocker


def write_config(p):
    p.write_text("""data: /data/input/PEQ_Hupsel.dat
parameters:
  cW: 200
  cV: 4
  cG: 5.0e+6
  cQ: 10
  cS: 4
  dG0: 1250
  cD: 1500
  aS: 0.01
  st: loamy_sand
start: 367416 # 2011120000
end: 367616 # 2011120200
step: 1
""")


def write_datafile(p):
    p.write_text(""""date" "P" "ETpot" "Q"
2011113023 0 0 0.0039
2011120100 0 0 0.0044
2011120101 0 0 0.0039
2011120102 0 0 0.0039
2011120103 0 0 0.0044
2011120104 0 0 0.0044
2011120105 0 0 0.0044
2011120106 0.5 0 0.0044
2011120107 0.3 0.0016 0.0044
2011120108 0 0.0078 0.0044
2011120109 0 0.0422 0.0044
2011120110 0 0.0438 0.005
2011120111 0 0.0672 0.005
2011120112 0 0.025 0.005
2011120113 0.2 0.0094 0.005
2011120114 0 0.0031 0.005
2011120115 0.4 0 0.005
2011120116 0 0 0.0055
2011120117 0 0 0.0055
2011120118 0 0 0.0055
2011120119 1 0 0.0061
2011120120 1.2 0 0.0061
2011120121 0.3 0 0.0066
2011120122 0.3 0 0.0072
2011120123 0 0 0.0078
2011120200 0 0 0.0083
2011120201 0 0 0.0089
""")


@pytest.fixture
def walrus_input(tmp_path):
    cfg = tmp_path / 'config.yml'
    write_config(cfg)
    write_datafile(tmp_path / 'PEQ_Hupsel.dat')
    return cfg


@pytest.fixture()
def walrus_model(tmp_path, walrus_input):
    model = BmiClientDocker(image="ewatercycle/walrus-grpc4bmi", image_port=55555, input_dir=tmp_path)
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
