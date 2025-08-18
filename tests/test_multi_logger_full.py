import pytest
from interface import LoggingInterface
from multi_logger import MultiLogger, VALID_LEVELS

class Dummy(LoggingInterface):
    def __init__(self, name="d"):
        self.name = name
        self.calls = []
    def log(self, level, message):
        self.calls.append((level, message))

class MutatingDummy(LoggingInterface):
    """Entfernt sich selbst beim ersten Log-Aufruf aus dem MultiLogger (per Closure-Ref)."""
    def __init__(self, ml_ref, name="m"):
        self.ml_ref = ml_ref
        self.name = name
        self.calls = []
        self._removed = False
    def log(self, level, message):
        self.calls.append((level, message))
        if not self._removed:
            self.ml_ref.remove_target(self)
            self._removed = True

def test_init_and_basic_dispatch():
    # init ohne targets
    ml = MultiLogger()
    # kein Fehler, keine Targets
    ml.info("noop")

    # mit target
    a = Dummy("a")
    ml = MultiLogger([a])
    ml.info("hello")
    assert ("info", "hello") in a.calls

def test_add_target_and_filtering():
    a, b = Dummy("a"), Dummy("b")
    ml = MultiLogger([a])
    # b akzeptiert nur error/critical
    ml.add_target(b, levels=["ERROR", "critical", "invalid", "DeBuG"])  # Normalisierung + Filter
    # info -> nur a
    ml.info("i")
    assert ("info", "i") in a.calls
    assert ("info", "i") not in b.calls
    # error -> beide
    ml.error("e")
    assert ("error", "e") in a.calls
    assert ("error", "e") in b.calls

def test_set_levels_and_reset():
    a, b = Dummy("a"), Dummy("b")
    ml = MultiLogger([a, b])
    # zunächst beide ohne Filter
    ml.warning("w0")
    assert ("warning", "w0") in a.calls and ("warning", "w0") in b.calls

    # b nur debug zulassen
    ml.set_levels(b, levels=["debug"])
    ml.debug("d1")
    ml.info("i1")
    assert ("debug", "d1") in a.calls and ("debug", "d1") in b.calls
    assert ("info", "i1") in a.calls and ("info", "i1") not in b.calls

    # Filter von b entfernen (None)
    ml.set_levels(b, None)
    ml.info("i2")
    assert ("info", "i2") in b.calls

def test_remove_target_also_removes_filter():
    a, b = Dummy("a"), Dummy("b")
    ml = MultiLogger([a])
    ml.add_target(b, levels=["error"])
    ml.remove_target(b)
    ml.info("after-remove")
    assert ("info", "after-remove") in a.calls
    assert ("info", "after-remove") not in b.calls  # b ist weg

def test_unknown_level_falls_back_to_info():
    a = Dummy()
    ml = MultiLogger([a])
    ml.log("not-a-level", "x")
    assert ("info", "x") in a.calls

def test_none_or_empty_level_falls_back_to_info():
    a = Dummy()
    ml = MultiLogger([a])
    ml.log(None, "n")
    ml.log("", "e")
    assert ("info", "n") in a.calls
    assert ("info", "e") in a.calls

def test_convenience_methods():
    a = Dummy()
    ml = MultiLogger([a])
    ml.debug("d"); ml.info("i"); ml.warning("w"); ml.error("e"); ml.critical("c")
    assert ("debug", "d") in a.calls
    assert ("info", "i") in a.calls
    assert ("warning", "w") in a.calls
    assert ("error", "e") in a.calls
    assert ("critical", "c") in a.calls
    # VALID_LEVELS wird zumindest einmal benutzt
    assert {"debug","info","warning","error","critical"}.issubset(VALID_LEVELS)

def test_mutation_during_dispatch_is_safe():
    a = Dummy("a")
    # ml-Ref erst nach Konstruktion einsetzen
    ml = MultiLogger([a])
    m = MutatingDummy(ml, "m")
    ml.add_target(m)  # wird sich beim ersten Log selbst entfernen
    ml.info("once")
    # beide haben den ersten Call bekommen
    assert ("info", "once") in a.calls
    assert ("info", "once") in m.calls
    # zweiter Call: m ist schon entfernt, bekommt nichts mehr
    ml.info("twice")
    assert ("info", "twice") in a.calls
    assert ("info", "twice") not in m.calls
