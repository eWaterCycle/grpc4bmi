import pytest


def write_config(p, data_fn):
    p.write_text(f"""data: {data_fn}
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
centroid:
  lon: 6.65443600418465
  lat: 52.06132311280826
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
    df = tmp_path / 'PEQ_Hupsel.dat'
    write_config(cfg, df)
    write_datafile(df)
    return cfg


@pytest.fixture()
def walrus_2input_dirs(tmp_path):
    # Have config in input dir and forcings data file in forcings dir
    forcings_dir = tmp_path / 'forcings'
    forcings_dir.mkdir()
    df = forcings_dir / 'PEQ_Hupsel.dat'
    write_datafile(df)
    input_dir = tmp_path / 'input'
    input_dir.mkdir()
    cfg = input_dir / 'config.yml'
    write_config(cfg, df)
    return {
        'input_dirs': (input_dir, forcings_dir),
        'cfg': str(cfg)
    }
