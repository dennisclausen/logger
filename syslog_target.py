import logging
import logging.handlers
from interface import LoggingInterface

class SyslogTarget(LoggingInterface):
    def __init__(self, name: str = "homelab", facility=logging.handlers.SysLogHandler.LOG_USER):
        """
        Syslog Logger.
        :param name: Name des Loggers (wird im Syslog angezeigt)
        :param facility: Syslog Facility (default: LOG_USER)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # alles loggen, Level wird in .log() gefiltert

        # Syslog-Handler konfigurieren
        syslog_handler = logging.handlers.SysLogHandler(address='/dev/log', facility=facility)
        formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
        syslog_handler.setFormatter(formatter)

        # Doppelte Handler vermeiden
        if not any(isinstance(h, logging.handlers.SysLogHandler) for h in self.logger.handlers):
            self.logger.addHandler(syslog_handler)

    def log(self, level: str, message: str):
        """
        Loggt eine Nachricht mit dem gegebenen Level ins Syslog.
        :param level: 'debug', 'info', 'warning', 'error', 'critical'
        :param message: Nachrichtentext
        """
        level = level.lower()
        if hasattr(self.logger, level):
            getattr(self.logger, level)(message)
        else:
            self.logger.info(message)
