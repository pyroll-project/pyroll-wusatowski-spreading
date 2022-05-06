import logging
from pathlib import Path

import pyroll


def test_solve(tmp_path: Path, caplog):
    caplog.set_level(logging.ERROR, "matplotlib")
    caplog.set_level(logging.DEBUG)

    import pyroll_wusatowski_spreading

    from pyroll.ui.cli.res import input_trio

    pyroll.solve(input_trio.sequence, input_trio.in_profile)

    report = pyroll.Reporter().render(input_trio.sequence)

    report_file = tmp_path / "report.html"
    report_file.write_text(report)
    print()
    print(report_file)

    print()
    print(caplog.text)
