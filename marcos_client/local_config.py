from pathlib import Path

try:
    import tomllib  # Python Version >= 3.11
except ModuleNotFoundError:
    import tomli as tomllib

configpath = Path(__file__).parent / "local_config.toml"
with configpath.open(mode="rb") as fp:
    config = tomllib.load(fp)
