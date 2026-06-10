from commands.base_command import BaseCommand
from models.service_results import DiagnosticResult
from services.base_diagnostic_service import DiagnosticServiceABC


class RunDiagnosticCommand(BaseCommand):
    def __init__(self, diagnostic_svc: DiagnosticServiceABC) -> None:
        self._diagnostic_svc = diagnostic_svc

    def execute(self) -> DiagnosticResult:
        return self._diagnostic_svc.run_diagnostic()
