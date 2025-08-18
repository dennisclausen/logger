from typing import Iterable, List, Dict, Set
from interface import LoggingInterface

VALID_LEVELS: Set[str] = {"debug", "info", "warning", "error", "critical"}

class MultiLogger:
    """
    Verteilt Log-Messages an mehrere Logging-Targets.
    Optional: pro Target Level-Filter (Whitelist).
    """
    def __init__(self, targets: Iterable[LoggingInterface] | None = None):
        self._targets: List[LoggingInterface] = list(targets or [])
        # optionaler Filter: target -> erlaubte Level (whitelist). Fehlt ein Eintrag, sind alle Level erlaubt.
        self._filters: Dict[LoggingInterface, Set[str]] = {}

    def add_target(self, target: LoggingInterface, levels: Iterable[str] | None = None) -> None:
        self._targets.append(target)
        if levels:
            level_set = {l.lower() for l in levels if l.lower() in VALID_LEVELS}
            self._filters[target] = level_set

    def remove_target(self, target: LoggingInterface) -> None:
        if target in self._targets:
            self._targets.remove(target)
            self._filters.pop(target, None)

    def set_levels(self, target: LoggingInterface, levels: Iterable[str] | None) -> None:
        if levels is None:
            self._filters.pop(target, None)
        else:
            self._filters[target] = {l.lower() for l in levels if l.lower() in VALID_LEVELS}

    def log(self, level: str, message: str) -> None:
        lvl = (level or "").lower()
        if lvl not in VALID_LEVELS:
            lvl = "info"
        for t in list(self._targets):  # Kopie, falls Targets während des Loggens geändert werden
            allowed = self._filters.get(t)
            if allowed is None or lvl in allowed:
                t.log(lvl, message)

    # Convenience
    def debug(self, msg: str) -> None:    self.log("debug", msg)
    def info(self, msg: str) -> None:     self.log("info", msg)
    def warning(self, msg: str) -> None:  self.log("warning", msg)
    def error(self, msg: str) -> None:    self.log("error", msg)
    def critical(self, msg: str) -> None: self.log("critical", msg)
