from commands.base_command import BaseCommand
from models.service_results import RebootResult
from services.base_diagnostic_service import DiagnosticServiceABC


class RebootRouterCommand(BaseCommand):
    def __init__(self, diagnostic_svc: DiagnosticServiceABC) -> None:
        self._diagnostic_svc = diagnostic_svc

    def execute(self) -> RebootResult:
        return self._diagnostic_svc.reboot()
