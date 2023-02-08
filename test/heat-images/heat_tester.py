from pathlib import Path
from tempfile import tempdir
from textwrap import dedent

import numpy as np

from grpc4bmi.bmi_client_docker import BmiClientDocker
from grpc4bmi.reserve import reserve_values

def test_heat(tmp_path: Path):
    # Config file for Python based heat model
    py_config = dedent("""\
        shape:
        - 6
        - 8
        spacing:
        - 1.0
        - 1.0
        origin:
        - 0.0
        - 0.0
        alpha: 1.0
    """)
    # Config file for C/C++ based heat model
    c_config = '1.5, 8.0, 7, 6'


    image, config_body = (
        # Comment out line you want to run
    # 'heat:py-0.2',py_config
    'heat:py-0.2-legacy',py_config
    # 'heat:py-2.0',py_config
    # 'heat:py-2.0-pb4',py_config
    # 'heat:cxx-bmi20-pb3', c_config
    # 'heat:c-bmi20-pb3', c_config
    )

    config = tmp_path / 'config.yaml'
    config.write_text(config_body)

    print(image)
    model = BmiClientDocker(image, work_dir=str(tmp_path), delay=1)

    model.initialize(str(config))

    print(model.get_component_name())
    print(model.get_output_var_names())

    model.update()

    var_name = 'plate_surface__temperature'
    output = reserve_values(model, var_name)
    values = model.get_value(var_name, output)
    print(values)

    model.finalize()
    # assert 1==0

test_heat(tmp_path=Path('/tmp'))
