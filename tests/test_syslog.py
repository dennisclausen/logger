import logging
import pytest
from syslog_target import SyslogTarget
from interface import LoggingInterface

def test_syslogtarget_is_interface():
    target = SyslogTarget(name="testlogger")
    assert isinstance(target, LoggingInterface)

def test_syslogtarget_logging(caplog):
    target = SyslogTarget(name="testlogger")
    with caplog.at_level(logging.INFO):
        target.log("info", "Test message")
    assert "Test message" in caplog.text
