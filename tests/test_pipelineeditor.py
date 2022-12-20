import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipelineeditor.node_scene import Scene # noqa


def test_imports():
    assert hasattr(Scene, 'has_been_modified')