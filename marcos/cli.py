import argparse
import logging
from pathlib import Path

from marcos import local_config
from marcos.__about__ import __version__
from marcos.plot_csv import plot_csv
from marcos.tests.test_marga_model import test_model

logger = logging.getLogger(__name__)


def main():
    args = _parse_args()

    # Verbosity
    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)s> %(message)s",
        )
    else:
        logging.basicConfig(
            level=logging.WARNING,
            format="%(asctime)s | %(message)s",
            datefmt="%H:%M:%S",
        )
    logger.info(
        "Logging level set to %s", logging.getLevelName(logger.getEffectiveLevel())
    )

    # Configuration File
    if args.config:
        local_config.reload_config([args.config.resolve()])

    # Commands
    if hasattr(args, "csv"):
        logger.info("Plotting csv...")
        plot_csv(args.csv)

    if hasattr(args, "test"):
        if args.test == "marga":
            logger.info("Testing marga model...")
            test_model()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CLI Client Interface for MaRCoS")

    # Some default stuff
    parser.add_argument(
        "--version",
        action="version",
        version=f"MaRCoS {__version__}",
    )
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    parser.add_argument(
        "-c",
        "--config",
        help="path to the *.toml configuration file",
        metavar="local_config.toml",
        type=Path,
    )

    subparsers = parser.add_subparsers(
        help="available subcommands",
        title="subcommands",
        description="specifying a subcommand is required",
        required=True,
    )

    # Plot Command
    plot_parser = subparsers.add_parser(
        "plot",
        help="plot supplied data",
        description="Plot the cycle accurate simulation output from the marga simulator",
    )
    plot_parser.add_argument(
        "csv",
        type=Path,
        help="Path to the *.csv output file from the marga simulator",
        metavar="marga_sim.csv",
    )

    # Test Commands
    test_parser = subparsers.add_parser(
        "test",
        help="run various tests against the server or simulator",
        description="Run a test and compare the output with expected values",
    )
    test_parser.add_argument(
        "test",
        help="Choose a test to run",
        choices=["marga", "noise", "server"],
        metavar="choice",
    )

    return parser.parse_args()
