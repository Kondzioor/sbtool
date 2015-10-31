#!/usr/bin/env python

r"""
Responsible for sbtool run mode
"""

import argparse
from sbtool import server

try:
    import config
except ImportError:
    import config_default as config


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Runs sbtool.")
    PARSER.add_argument("--server", action="store_true",
                        help="Runs in server mode")

    ARGS = PARSER.parse_args()

    if ARGS.server:
        server.run(config)
    else:
        PARSER.print_help()
