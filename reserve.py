#!/usr/bin/env python
r"""
Sbtool console client
"""

from sbtool.ui.console import run

try:
    import config
except ImportError:
    import config_default as config


if __name__ == "__main__":
    run(config)
