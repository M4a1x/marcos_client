# MaRCoS

[![python - version][python-badge]][python] [![project - hatch][hatch-badge]][hatch] [![linting - Ruff][ruff-badge]][ruff] [![code style - Black][black-badge]][black] [![types - Mypy][mypy-badge]][mypy]

-----

Python-based MaRCoS CLI, associated tests and APIs.


**Table of Contents**

- [MaRCoS](#marcos)
  - [Installation](#installation)
  - [Documentation](#documentation)
  - [Setup Guide](#setup-guide)
  - [Roadmap](#roadmap)
  - [\[OUTDATED - only for reference\]: File descriptions](#outdated---only-for-reference-file-descriptions)
  - [License](#license)

## Installation

TODO: The Python package is not yet released.

```console
pip install marcos
```

## Documentation

See the [MaRCoS wiki](https://github.com/vnegnev/marcos_extras/wiki) for info; specifically the [Using MaRCoS](https://github.com/vnegnev/marcos_extras/wiki/using_marcos) and the [Marcos internals](https://github.com/vnegnev/marcos_extras/wiki/marcos_internals) pages.

## Setup Guide

If you want to write your own scripts the _recommended_ procedure is as follows (i.e. using a Python virtual environment managed by `hatch`)
1. Install `hatch` for dependency management (either as user or site wide):
    1. `python -m ensurepip`
    2. `python -m pip install -U pip`
    3. `python -m pip install -U hatch`
2. Create a new project, e.g. in your home folder:
    1. `cd ~`
    2. `hatch new my_experiments`
3. Add `marcos` as a dependency:
    1. `cd my_experiments`
    2. `nano pyproject.toml`
    3. Find the line that says `dependencies=[]` and change it to `dependencies = ["marcos @ git+https://github.com/M4a1x/marcos_client.git"]`. Save with `<Ctrl-O>`. Exit with `<Ctrl-X>`.
4. Create your first script here: `~/my_experiments/my_experiment/first_experiment.py` With your favourite text editor with content:
    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    from marcos import Experiment


    def my_first_experiment():
        exp = Experiment(lo_freq=5, rx_t=3.125)

        exp.add_flodict({"tx0": (np.array([50, 130]), np.array([0.5, 0]))})
        exp.add_flodict({"rx0_en": (np.array([200, 400]), np.array([1, 0]))})

        exp.plot_sequence()
        plt.show()

        # Execute the sequence
        rxd, msgs = exp.run()
        exp.close_server(only_if_sim=True)

    if __name__ == "__main__":
        my_first_experiment()
    ```
5. Start the `marga` simulator. See wiki/README.md for details
6. Run your first script:
   1. `cd ~/my_experiments`
   2. `hatch run my_experiments/first_experiment.py`

## Roadmap
- API for configuration (`local_config.py`/`local_config.toml`)
- Create `local_config.toml` through CLI
- Include `test_server.py` into CLI (Should return no errors)
- Include `test_noise.py` into CLI (Generates simple pulses to view on an oscilloscope)
  
## [OUTDATED - only for reference]: File descriptions

- `csvs/` : CSV files used by test_flocra_model.py
- `experiment.py` : basic API for controlling the MaRCoS server
- `examples.py` : examples of how to use experiment.py and other libraries [WIP]
- `local_config.py.example` : template file for local configuration; create a copy and name it local_config.py to configure your local setup
- `server_comms.py` : low-level communication library for the MaRCoS server; use if you wish to write your own API
- `test_flocra.py` : hand-written (low-level) examples/tests of the Flocra system
- `test_flocra_model.py` : unit tests of the MaRCoS server + Verilator model of the Flocra HDL
- `test_ocra_pulseq.py` : tests of the [ocra-pulseq](https://github.com/lcbMGH/ocra-pulseq) interface [WIP]
- `test_server.py` : unit tests of the standalone MaRCoS server operation
- `vlsualiser.py` : [WIP] plot expected ocra assembly file outputs (for very basic files)


## License

`marcos` is distributed under the terms of the [GPL-3.0-or-later](https://spdx.org/licenses/GPL-3.0-or-later.html) license.

[python-badge]: https://img.shields.io/badge/python->=3.7-blue
[python]: https://www.python.org/downloads/
[hatch]: https://github.com/pypa/hatch
[hatch-badge]: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
[ruff]: https://github.com/charliermarsh/ruff
[ruff-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json
[black]: https://github.com/psf/black
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[mypy]: https://github.com/python/mypy
[mypy-badge]: https://img.shields.io/badge/types-Mypy-blue.svg