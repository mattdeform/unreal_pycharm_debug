from pathlib import Path
import sys

import pytest


@pytest.fixture(scope='session', autouse=True)
def add_root_to_sys_path():
    """ Currently hardcoded to UE5"""
    root_dir = Path(__file__).resolve().parents[1] / "plugin_src" / "5.x.0" / "pycharm_remote_debug" / "Content" / "Python"
    sys.path.insert(0, root_dir.as_posix())
