
"""
Usage::

    import install_pyenv
    install_pyenv.install("3.4.5")

"""

import os
import sys
import tempfile
import textwrap

from subprocess import check_output


def _log_prefix():
    script_name = os.path.basename(__file__)
    return "[travis:%s] " % script_name


def _log(*args):
    print(_log_prefix() + " ".join(args))
    sys.stdout.flush()


def indent(text, prefix, predicate=None):
    """Adds 'prefix' to the beginning of selected lines in 'text'.
    If 'predicate' is provided, 'prefix' will only be added to the lines
    where 'predicate(line)' is True. If 'predicate' is not provided,
    it will default to adding 'prefix' to all non-empty lines that do not
    consist solely of whitespace characters.

    Copied from textwrap.py available in python 3 (cpython/cpython@a2d2bef)
    """
    if predicate is None:
        def predicate(line):
            return line.strip()

    def prefixed_lines():
        for line in text.splitlines(True):
            yield (prefix + line if predicate(line) else line)
    return ''.join(prefixed_lines())


def _execute_script(script):
    def _write(output_stream, txt):
        output_stream.write(bytearray("%s\n" % txt, "utf-8"))
    with tempfile.NamedTemporaryFile(delete=True) as script_file:
        _write(script_file, script)
        script_file.file.flush()
        # _log("Executing:", "bash", script_file.name)
        return check_output(
            ["bash", script_file.name]).decode("utf-8").strip()


def is_pyenv_installed(py_version):
    """Return True if ``py_version`` pyenv is installed.
    """
    script = textwrap.dedent(
        r"""
        #eval "$( pyenv init - )"
        (pyenv versions             \
          | sed -Ee "s/\(.+\)//"    \
          | tr -d "* "              \
          | grep "^{py_version}$")  \
        || echo ""
        """.format(py_version=py_version)
    )
    return _execute_script(script) == py_version


def pyenv_executable_path(py_version, executable="python"):
    return os.path.expanduser(
        "~/.pyenv/versions/%s/bin/%s" % (py_version, executable))


def pyenv_executable_exists(py_version, executable="python"):
    return os.path.exists(pyenv_executable_path(py_version, executable))


def install(py_version):
    """Update and install ``pyenv``."""

    _log("Looking for", pyenv_executable_path(py_version))
    python_found = pyenv_executable_exists(py_version)
    if python_found:
        _log("  ->", "found")
        return
    else:
        _log("  ->", "not found")

    cmd = "brew update"
    _log("Executing:", cmd)
    check_output(cmd, shell=True)
    _log("  -> done")

    cmd = "brew outdated pyenv || brew upgrade pyenv"
    _log("Executing:", cmd)
    check_output(cmd, shell=True)
    _log("  -> done")

    _log("Looking for pyenv", py_version)
    if is_pyenv_installed(py_version) and pyenv_executable_exists(py_version):
        _log("  ->", "found")
        return
    else:
        _log("  ->", "not found")

    _log("Installing pyenv", py_version)
    cmd = textwrap.dedent(
        """
        eval "$( pyenv init - )"
        pyenv install {py_version}
        """.format(py_version=py_version)
    ).strip()
    _log("Executing:")
    for line in indent(cmd, " " * 11).splitlines():
        _log(line)
    check_output(cmd, shell=True)
    _log("  -> done")

    _log("Looking for pyenv", py_version)
    if not is_pyenv_installed(py_version):
        exit(_log_prefix() +
             "  -> ERROR: Failed to install pyenv %s" % py_version)
    _log("  ->", "found")


if __name__ == '__main__':
    install(os.environ['PYTHON_VERSION'])
