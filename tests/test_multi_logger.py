# tests/test_multi_logger_basic.py
from interface import LoggingInterface
from multi_logger import MultiLogger

class Dummy(LoggingInterface):
    def __init__(self): self.calls = []
    def log(self, level, message): self.calls.append((level, message))

def test_multilogger_dispatch_and_filter():
    a, b = Dummy(), Dummy()
    ml = MultiLogger([a])
    ml.add_target(b, levels=["error"])
    ml.info("ok")
    ml.error("boom")
    assert ("info", "ok") in a.calls and ("info", "ok") not in b.calls
    assert ("error", "boom") in a.calls and ("error", "boom") in b.calls
