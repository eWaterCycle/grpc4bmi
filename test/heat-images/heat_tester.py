from pathlib import Path
from tempfile import tempdir
from textwrap import dedent

import numpy as np

from grpc4bmi.bmi_client_docker import BmiClientDocker

def test_heat(tmp_path: Path):
    config = tmp_path / 'config.yaml'
    config.write_text(dedent("""\
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
    """))

    image = 'heat:py-0.2'
    # image = 'heat:py-2.0'
    # image = 'heat:py-2.0-pb4'
    model = BmiClientDocker(image, work_dir=str(tmp_path), delay=1)

    model.initialize(str(config))

    print(model.get_component_name())
    print(model.get_output_var_names())

    model.update()

    values = model.get_value('plate_surface__temperature', np.zeros(48))
    print(values)

    model.finalize()
    # assert 1==0

test_heat(tmp_path=Path('/tmp/b'))
