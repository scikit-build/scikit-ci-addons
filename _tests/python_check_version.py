
import os
import sys

current_version = list(sys.version_info[:3])
print("current: %s" % str(current_version))

expected_version = list(
    map(int, os.environ["EXPECTED_PYTHON_VERSION"].split(".")))
print("expected: %s" % str(expected_version))

assert current_version == expected_version
