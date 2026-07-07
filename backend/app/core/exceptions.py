class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

class ValidationException(AppException):
    pass

class SetuException(AppException):
    pass
