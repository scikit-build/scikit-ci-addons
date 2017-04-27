
import anyci.docker
import ci_addons
import os
import py_compile
import pytest
import shutil
import subprocess
import sys

from lxml import etree

from . import captured_lines, format_args_for_display


def test_home():
    expected_home = os.path.abspath(os.path.dirname(__file__) + '/..')
    assert ci_addons.home() == expected_home


@pytest.mark.parametrize("addon, extension, exception, expected_prefix_path", [
    ('anyci/noop', '.py', None, ""),
    ('anyci/noop.py',  '.py', None, ""),
    ('noop', '.py', None, "anyci"),
    ('noop.py',  '.py', None, "anyci"),
    ('appveyor/patch_vs2008',  '.py', None, ""),
    (os.path.join(ci_addons.home(), 'appveyor/patch_vs2008'),  '.py', None, ""),
    ('travis/run-with-pyenv.sh',  '.sh', None, ""),
    ('install_cmake',  '.py', RuntimeError, ""),
    ('nonexistent',  '', RuntimeError, ""),
])
def test_path(addon, extension, exception, expected_prefix_path):
    expected_path = os.path.join(ci_addons.home(), expected_prefix_path, addon)
    if not addon.endswith(extension):
        expected_path += extension
    if exception is None:
        assert ci_addons.path(addon) == expected_path
    else:
        with pytest.raises(exception):
            ci_addons.path(addon)


def test_addons():
    noop_file_name = os.path.join("anyci", "noop") + ".py"
    noop_file_name_pyc = os.path.join("anyci", "noop") + ".pyc"
    noop_file_path = os.path.join(ci_addons.home(), noop_file_name)
    noop_file_path_pyc = os.path.join(ci_addons.home(), noop_file_name_pyc)

    py_compile.main([noop_file_path])

    if sys.version_info < (3,):
        assert os.path.exists(noop_file_path_pyc)

    assert noop_file_name in ci_addons.addons()
    assert noop_file_name_pyc not in ci_addons.addons()


@pytest.mark.parametrize("addon", ['anyci/noop', 'anyci/noop.py'])
def test_execute(addon, capfd):
    ci_addons.execute(addon, ['foo', 'bar'])
    output_lines, _ = captured_lines(capfd)
    noop_path = os.path.join(ci_addons.home(), 'anyci/noop.py')
    assert noop_path + ' foo bar' in output_lines


def test_install(tmpdir, capfd):
    noop = tmpdir.ensure('anyci/noop.py')

    ci_addons.install(str(tmpdir))
    output_lines, _ = captured_lines(capfd)

    for addon in ci_addons.addons():
        assert tmpdir.join(addon).exists()

    assert str(noop) + ' (skipped)' in output_lines
    assert str(tmpdir.join('appveyor', 'patch_vs2008.py')) in output_lines

    #
    # Check specifying --force overwrite add-ons already installed
    #
    ci_addons.install(str(tmpdir), force=True)
    output_lines, _ = captured_lines(capfd)

    assert str(noop) + ' (overwritten)' in output_lines

    #
    # Check that trying to overwrite original add-ons fails
    #
    with pytest.raises(RuntimeError):
        ci_addons.install(ci_addons.home())


def test_cli():

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    environment = dict(os.environ)
    environment['PYTHONPATH'] = root

    #
    # Running without argument should NOT fail
    #
    output = subprocess.check_output(
        "python -m ci_addons",
        shell=True,
        env=environment,
        stderr=subprocess.STDOUT,
        cwd=str(root)
    ).decode("utf-8")
    assert "usage:" in output

    #
    # Check that --list works
    #
    output = subprocess.check_output(
        "python -m ci_addons --list",
        shell=True,
        env=environment,
        stderr=subprocess.STDOUT,
        cwd=str(root)
    ).decode("utf-8")
    # Check that at least one add-on of each service is reported
    for addon in [
        "anyci/run.sh",
        "appveyor/rolling-build.ps1",
        "circle/install_cmake.py",
        "travis/run-with-pyenv.sh"
    ]:
        assert addon.replace('/', os.path.sep) in output


@pytest.mark.parametrize("filename, expected", [
    ("library/hello-world:latest", "library-hello-world-latest")
])
def test_addon_anyci_docker_get_valid_filename(filename, expected):
    assert anyci.docker.get_valid_filename(filename) == expected


def has_docker():
    """Return True if docker executable is found."""
    try:
        subprocess.check_output(["docker", "--version"])
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def test_addon_anyci_docker(tmpdir):

    test_image = "hello-world"
    test_image_filename = test_image + ".tar"
    test_image_id_filename = test_image + ".image_id"

    is_circleci = "CIRCLECI" in os.environ
    if is_circleci:
        assert has_docker(), "docker is expected when running tests on CircleCI"

    if not has_docker():
        pytest.skip("docker executable not found")

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    environment = dict(os.environ)
    environment['PYTHONPATH'] = root
    environment['HOME'] = str(tmpdir)

    def _display_cmd(cmd):
        print("\nExecuting: {}".format(format_args_for_display(cmd)))

    #
    # Delete image if any (useful when testing locally)
    #
    if not is_circleci:
        try:
            cmd = ["docker", "rmi", "-f", test_image]
            _display_cmd(cmd)
            subprocess.check_output(cmd)
        except subprocess.CalledProcessError:
            pass

    #
    # Check load-pull-save works with default cache directory
    #
    cmd = ["python", "-m",
           "ci_addons", "anyci/docker", "--",
           "load-pull-save", test_image, "--verbose"]
    _display_cmd(cmd)
    output = subprocess.check_output(
        cmd,
        env=environment,
        stderr=subprocess.STDOUT,
        cwd=str(root)
    ).decode("utf-8")
    assert "Status: Downloaded newer image for %s:latest" % test_image in output
    assert "cached image ID:" not in output
    assert tmpdir.join("docker", test_image_filename).exists()
    assert tmpdir.join("docker", test_image_id_filename).exists()

    #
    # Check load-pull-save works with custom cache directory
    #
    cache_dir = tmpdir.ensure("cache", dir=True)
    cmd_with_cache = cmd + ["--cache-dir", str(cache_dir)]
    _display_cmd(cmd_with_cache)
    output = subprocess.check_output(
        cmd_with_cache,
        env=environment,
        stderr=subprocess.STDOUT,
        cwd=str(root)
    ).decode("utf-8")
    assert "Status: Image is up to date for %s:latest" % test_image in output
    assert "cached image ID:" not in output
    assert tmpdir.join("cache", test_image_filename).exists()
    assert tmpdir.join("cache", test_image_id_filename).exists()

    #
    # Delete the image
    #

    cmd = ["docker", "rmi", "-f", test_image]
    _display_cmd(cmd)
    if not is_circleci:
        output = subprocess.check_output(cmd).decode("utf-8")
        assert "Untagged: %s@sha256" % test_image in output
        assert "Deleted: sha256:" in output
    else:
        print("  -> Skipping: "
              "Not supported on CircleCI because containers can NOT be "
              "removed in unprivileged LXC container")

    #
    # Check load-pull-save restores cached image
    #
    _display_cmd(cmd_with_cache)
    output = subprocess.check_output(
        cmd_with_cache,
        env=environment,
        stderr=subprocess.STDOUT,
        cwd=str(root)
    ).decode("utf-8")
    assert "cached image ID:" in output
    assert "Status: Image is up to date for %s:latest" % test_image in output
    assert "Skipped because pulled image did not change" in output
    assert tmpdir.join("cache", test_image_filename).exists()


def test_addon_anyci_ctest_junit_formatter(tmpdir):
    testing_dir = tmpdir.mkdir("Testing")
    tag = "20170426-0546"
    testing_dir.ensure("TAG").write(tag)

    # Input data and associated expected values were obtained by running Girder
    # tests using "ctest -D ExperimentalTest" and by copying the "Test.xml"
    # found in the Testing subdirectory.
    #
    # Note: If new data are generated, the expected values will have to be
    #       tweaked. Additionally, the "base64" section should be replaced by
    #       a shorter text.

    test_data_dir = os.path.join(os.path.dirname(__file__), "data")
    test_xml = os.path.join(test_data_dir, "ctest_junit_formatter_input.xml")
    assert os.path.exists(test_xml)

    shutil.copyfile(test_xml, str(testing_dir.mkdir(tag).join("Test.xml")))

    cmd = ["python", "-m",
           "ci_addons", "anyci/ctest_junit_formatter", str(tmpdir)]

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    environment = dict(os.environ)
    environment['PYTHONPATH'] = root
    environment['HOME'] = str(tmpdir)

    output = subprocess.check_output(
        cmd,
        env=environment,
        stderr=subprocess.STDOUT,
        cwd=root
    ).decode("utf-8", "ignore")

    expected_properties = {
        "BuildName": "Linux-",
        "BuildStamp": "20170426-0546-Experimental",
        "Name": "CerroTorre",
        "Generator": "ctest-3.4.2",
        "CompilerName": "",
        "OSName": "Linux",
        "Hostname": "CerroTorre",
        "OSRelease": "4.2.0-42-generic",
        "OSVersion": "#49-Ubuntu SMP Tue Jun 28 21:26:26 UTC 2016",
        "OSPlatform": "x86_64",
        "Is64Bits": "1",
        "VendorString": "GenuineIntel",
        "VendorID": "Intel Corporation",
        "FamilyID": "6",
        "ModelID": "94",
        "ProcessorCacheSize": "8192",
        "NumberOfLogicalCPU": "8",
        "NumberOfPhysicalCPU": "1",
        "TotalVirtualMemory": "63336",
        "TotalPhysicalMemory": "62267",
        "LogicalProcessorsPerPhysical": "8",
        "ProcessorClockFrequency": "3489.74"
    }

    output_doc = etree.XML(output)

    assert output_doc.tag == "testsuite"

    system_out = output_doc.findall("system-out")
    assert len(system_out) == 1

    properties = output_doc.findall("./properties/property")
    assert len(properties) == len(expected_properties)
    assert {elem.attrib["name"]: elem.attrib["value"]
            for elem in properties} == expected_properties

    testcases = output_doc.findall(
        "./testcase[@name][@classname='TestSuite'][@time]")
    assert len(testcases) == 193

    errors = output_doc.findall("./testcase/error[@message]")
    assert len(errors) == 37

    assert "testGroupAccess (tests.cases.group_test.GroupTestCase) ... FAIL" \
           in errors[0].text
