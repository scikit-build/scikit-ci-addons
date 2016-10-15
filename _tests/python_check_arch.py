import os
import struct

current_arch = struct.calcsize("P") * 8
print("current_arch: %s-bit" % current_arch)

expected_arch = int(os.environ["EXPECTED_PYTHON_ARCH"])
print("expected_arch: %s-bit" % expected_arch)

assert current_arch == expected_arch
