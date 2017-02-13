
"""
Usage::

    import noop
    noop.execute()

"""

import os
import sys


def _log(*args):
    script_name = os.path.basename(__file__)
    print("[anyci:%s] " % script_name + " ".join(args))
    sys.stdout.flush()


def execute():
    """Display value of ``sys.argv`` and exit.
    """
    _log("Display value of 'sys.argv'")
    print(" ".join(sys.argv))


if __name__ == '__main__':
    execute()
