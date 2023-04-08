# MaRCoS

[![python - version][python-badge]][python] [![project - hatch][hatch-badge]][hatch] [![linting - Ruff][ruff-badge]][ruff] [![code style - Black][black-badge]][black] [![types - Mypy][mypy-badge]][mypy]

-----

Python-based MaRCoS GUI and associated tests.


**Table of Contents**

- [MaRCoS](#marcos)
  - [Installation](#installation)
  - [Documentation](#documentation)
  - [Setup Guide](#setup-guide)
  - [File descriptions](#file-descriptions)
  - [License](#license)

## Installation

TODO: The Python package is not yet released.

```console
pip install marcos
```

## Documentation

See the [MaRCoS wiki](https://github.com/vnegnev/marcos_extras/wiki) for info; specifically the [Using MaRCoS](https://github.com/vnegnev/marcos_extras/wiki/using_marcos) and the [Marcos internals](https://github.com/vnegnev/marcos_extras/wiki/marcos_internals) pages.

## Setup Guide

- Install `msgpack` for Python manually or via the package manager of your choice.
- Clone the repo and copy `local_config.py.example` to `local_config.py`.
- Edit `local_config.py` to suit your network and hardware setup.
- Run `test_server.py` and make sure no errors are returned.
- Run `test_noise.py` to generate some simple pulses and view their properties on an oscilloscope.
- Import experiment.py in your higher-level MRI scripts.
  
## File descriptions

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