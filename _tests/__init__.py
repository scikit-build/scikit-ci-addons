
import os


def captured_lines(cap):
    """Given a ``capsys`` or ``capfd`` pytest fixture, return
     a tuple of the form ``(out_lines, error_lines)``.

    See http://doc.pytest.org/en/latest/capture.html
    """
    out, err = cap.readouterr()
    return (out.replace(os.linesep, "\n").split("\n"),
            err.replace(os.linesep, "\n").split("\n"))
