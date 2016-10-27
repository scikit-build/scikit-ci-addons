
import ci_addons
import os
import pytest
import subprocess

from . import captured_lines


def test_home():
    expected_home = os.path.abspath(os.path.dirname(__file__) + '/..')
    assert ci_addons.home() == expected_home


@pytest.mark.parametrize("addon", ['anyci/noop', 'anyci/noop.py'])
def test_path(addon):
    expected_path = ci_addons.home() + '/' + addon
    if not addon.endswith('.py'):
        expected_path += '.py'
    assert ci_addons.path(addon) == expected_path


def test_list(capsys):
    ci_addons.list_addons()
    output_lines, _ = captured_lines(capsys)
    assert 'anyci/noop.py' in output_lines


@pytest.mark.parametrize("addon", ['anyci/noop', 'anyci/noop.py'])
def test_execute(addon, capfd):
    ci_addons.execute(addon, ['foo', 'bar'])
    output_lines, _ = captured_lines(capfd)
    assert ci_addons.home() + '/anyci/noop.py foo bar' in output_lines


def test_cli():

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    environment = dict(os.environ)
    environment['PYTHONPATH'] = root

    subprocess.check_call(
        "python -m ci_addons",
        shell=True,
        env=environment,
        stderr=subprocess.STDOUT,
        cwd=str(root)
    )
