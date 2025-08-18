import pytest
from interface import LoggingInterface

def test_interface_is_abstract_and_not_instantiable():
    with pytest.raises(TypeError):
        LoggingInterface()

def test_interface_exposes_abstractmethods():
    assert hasattr(LoggingInterface, "__abstractmethods__")
    assert "log" in LoggingInterface.__abstractmethods__

def test_subclass_without_implementation_still_abstract():
    class Incomplete(LoggingInterface):
        pass
    with pytest.raises(TypeError):
        Incomplete()

def test_concrete_subclass_and_cover_base_body():
    class Concrete(LoggingInterface):
        def __init__(self):
            self.called = False
        def log(self, level: str, message: str):
            # ABC-Methodenrumpf ausführen (deckt die 'pass'-Zeile)
            LoggingInterface.log(self, level, message)
            self.called = True

    c = Concrete()
    c.log("info", "hello")
    assert c.called is True
