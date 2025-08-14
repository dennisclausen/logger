# tests/test_syslog_target_levels.py
import logging
import pytest
from unittest.mock import patch
from syslog_target import SyslogTarget

class FakeSysLogHandler(logging.StreamHandler):
    def __init__(self, *args, **kwargs):
        # ignoriert address/facility u.ä.
        super().__init__()

@pytest.fixture
def patched_syslog_handler():
    # Patche auf eine KLASSE, nicht auf eine Instanz oder Lambda
    with patch("logging.handlers.SysLogHandler", FakeSysLogHandler):
        yield
       
@pytest.mark.parametrize("level,expected_levelname", [
    ("debug",    "DEBUG"),
    ("info",     "INFO"),
    ("warning",  "WARNING"),
    ("error",    "ERROR"),
    ("critical", "CRITICAL"),
])
def test_syslogtarget_emits_each_level(patched_syslog_handler, caplog, level, expected_levelname):
    logger_name = "testlogger"
    target = SyslogTarget(name=logger_name)
    with caplog.at_level(logging.DEBUG, logger=logger_name):
        target.log(level, f"msg-{level}")
    # Prüfe, dass die Nachricht und das Level im Log auftauchen
    assert any(rec.levelname == expected_levelname and f"msg-{level}" in rec.message
               for rec in caplog.records)

def test_syslogtarget_unknown_level_falls_back_to_info(patched_syslog_handler, caplog):
    logger_name = "testlogger2"
    target = SyslogTarget(name=logger_name)
    with caplog.at_level(logging.INFO, logger=logger_name):
        target.log("unknown", "fallback-msg")
    assert any(rec.levelname == "INFO" and "fallback-msg" in rec.message for rec in caplog.records)

def test_syslogtarget_no_duplicate_handlers(patched_syslog_handler):
    logger_name = "dupcheck"
    t1 = SyslogTarget(name=logger_name)
    t2 = SyslogTarget(name=logger_name)
    # Es sollte nur ein SysLog/Stream-Handler am Logger hängen
    handlers = [h for h in logging.getLogger(logger_name).handlers]
    # genau 1 Handler
    assert len(handlers) == 1
