
import os


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
