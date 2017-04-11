
import errno
import os

from contextlib import contextmanager


def captured_lines(cap):
    """Given a ``capsys`` or ``capfd`` pytest fixture, return
     a tuple of the form ``(out_lines, error_lines)``.

    See http://doc.pytest.org/en/latest/capture.html
    """
    out, err = cap.readouterr()
    return (out.replace(os.linesep, "\n").split("\n"),
            err.replace(os.linesep, "\n").split("\n"))


def format_args_for_display(args):
    """Format a list of arguments appropriately for display. When formatting
    a command and its arguments, the user should be able to execute the
    command by copying and pasting the output directly into a shell.

    Currently, the only formatting is naively surrounding each argument with
    quotation marks.
    """
    return ' '.join("\"{}\"".format(arg) for arg in args)


def mkdir_p(path):
    """Ensure directory ``path`` exists. If needed, parent directories
    are created.

    Adapted from http://stackoverflow.com/a/600612/1539918
    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:  # pragma: no cover
            raise


@contextmanager
def push_dir(directory=None, make_directory=False):
    """Context manager to change current directory.

    :param directory:
      Path to set as current working directory. If ``None``
      is passed, ``os.getcwd()`` is used instead.

    :param make_directory:
      If True, ``directory`` is created.
    """
    old_cwd = os.getcwd()
    if directory:
        if make_directory:
            mkdir_p(directory)
        os.chdir(str(directory))
    yield
    os.chdir(old_cwd)
