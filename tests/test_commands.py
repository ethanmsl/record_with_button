"""
Unit Tests for `commands.py`
"""

import pytest
import typer

from record_with_button import commands


def test_version_callback():
    """
    Test error and non-error exit
    """
    assert commands.version_callback(False) is None
    with pytest.raises(typer.Exit):
        commands.version_callback(True)
