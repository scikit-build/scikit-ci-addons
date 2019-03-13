
import os
import sys

from pprint import pprint as pp
pp(os.environ['PATH'].split(os.path.pathsep))

current_version = list(sys.version_info[:3])
print("current: %s" % str(current_version))

expected_version = list(
    map(int, os.environ["EXPECTED_PYTHON_VERSION"].split(".")))
print("expected: %s" % str(expected_version))

assert current_version == expected_version
