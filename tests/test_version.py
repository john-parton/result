from __future__ import annotations

from importlib import metadata

import result


def test_version_comes_from_package_metadata() -> None:
    """``__version__`` has a single source: the pyproject version."""
    assert result.__version__ == metadata.version("result")
    assert result.__version__
