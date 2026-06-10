from constants.messages import MSG_DIAGNOSTIC_OFFLINE, MSG_REBOOT_SUCCESS
from models.service_results import DiagnosticResult, RebootResult
from services.base_diagnostic_service import DiagnosticServiceABC


class DiagnosticService(DiagnosticServiceABC):
    _DEVICE_STATUS: str = "OFFLINE"

    def run_diagnostic(self) -> DiagnosticResult:
        return DiagnosticResult(
            device_status=self._DEVICE_STATUS,
            message=MSG_DIAGNOSTIC_OFFLINE,
        )

    def reboot(self) -> RebootResult:
        return RebootResult(
            success=True,
            message=MSG_REBOOT_SUCCESS,
        )
