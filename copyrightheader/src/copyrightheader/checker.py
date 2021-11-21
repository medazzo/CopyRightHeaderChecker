"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = copyrightheader.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""
import argparse
import logging
import sys

import pkg_resources  # part of setuptools

from copyrightheader.analyser import Analyser
from copyrightheader.configuration import Conf

__author__ = "Mohamed Azzouni"
__copyright__ = "Mohamed Azzouni"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    """this functions will setup parameter and parser for argument"""
    version = pkg_resources.require("copyrightheader")[0].version
    parser = argparse.ArgumentParser(
        description="Checks sources code files for Copyright Header, use yours.",
        prog="checker",
    )
    parser.add_argument("--version", action="version", version=version)
    subparsers = parser.add_subparsers(help="main action")
    process_info = subparsers.add_parser("info", help="display informations")
    process_info.add_argument(
        "-d",
        "--display",
        dest="display",
        choices=["all", "short"],
        required=True,
        help="print informations",
    )
    process_parser = subparsers.add_parser("process", help="process checker")
    process_parser.add_argument(
        "-r",
        "--report",
        dest="report",
        action="store_true",
        help="print a detailed report for what has done",
    )
    process_parser.add_argument(
        "-u",
        "--update",
        dest="update",
        action="store_true",
        help="update files in sources path",
    )
    process_parser.add_argument(
        "-f",
        "--forceOldHeader",
        dest="forceOldHeader",
        action="store_true",
        help="replace old header if found in files ",
    )
    process_parser.add_argument(
        "-n",
        "--nameCompany",
        dest="nameCompany",
        required=True,
        help="company name to be used in copyright header",
    )
    process_parser.add_argument(
        "-a",
        "--addressCompany",
        dest="addressCompany",
        required=True,
        help="company address to be used in copyright header",
    )
    process_parser.add_argument(
        "-c",
        "--countryCompany",
        dest="countryCompany",
        required=True,
        help="company country to be used in copyright header",
    )
    process_parser.add_argument(
        "-y",
        "--yearCompany",
        dest="yearCompany",
        required=True,
        help="years to be used in copyright header ",
    )
    process_parser.add_argument(
        "-i",
        "--inputFolder",
        dest="inputFolder",
        required=True,
        help="path to folder containing source code to operate on",
    )
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    setup_logging(logging.DEBUG)
    if hasattr(args, "display"):
        if args.display == "all":
            Conf().info()
        else:
            Conf().short_info()
    else:
        _logger.debug("Starting calculations...")
        conf = Conf(
            args.report,
            args.update,
            args.forceOldHeader,
            args.nameCompany,
            args.addressCompany,
            args.countryCompany,
            args.yearCompany,
            args.inputFolder,
        )
        conf.short_info()
        dryRun = not args.update
        analyser = Analyser(args.inputFolder, dryRun, conf)
        analyser.process()
        _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m copyrightheader.skeleton 42
    #
    run()
