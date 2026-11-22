class LoanError(Exception):
    pass


class ValidationError(LoanError):
    pass


class DuplicateRecordError(LoanError):
    pass


class NotFoundError(LoanError):
    pass


class EquipmentUnavailableError(LoanError):
    pass


class NoActiveLoanError(LoanError):
    pass
