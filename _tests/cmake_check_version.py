
import os
from subprocess import check_output
import sys


def _log(*args):
    script_name = os.path.basename(__file__)
    print("[%s] " % script_name + " ".join(args))
    sys.stdout.flush()


expected = sys.argv[1]
_log("expected:", expected)

output = check_output(
    "cmake --version", shell=True).decode("utf-8")
current = output.splitlines()[0].split()[2]
_log("current:", current)

assert current == expected
