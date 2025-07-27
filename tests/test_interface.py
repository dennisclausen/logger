from interface import LoggingInterface
import pytest

def test_interface_cannot_be_instantiated():
    with pytest.raises(TypeError):
        LoggingInterface()
