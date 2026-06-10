from abc import ABC, abstractmethod

from models.service_results import DiagnosticResult, RebootResult


class DiagnosticServiceABC(ABC):
    @abstractmethod
    def run_diagnostic(self) -> DiagnosticResult: ...

    @abstractmethod
    def reboot(self) -> RebootResult: ...
