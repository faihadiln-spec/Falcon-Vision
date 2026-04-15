class AppError(Exception):
    status_code = 400
    detail = "Application error"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail


class NotFoundError(AppError):
    status_code = 404
    detail = "Resource not found"


class ConflictError(AppError):
    status_code = 409
    detail = "Resource already exists"


class InvalidCredentialsError(AppError):
    status_code = 401
    detail = "Invalid email or password"


class PermissionDeniedError(AppError):
    status_code = 403
    detail = "Permission denied"


class InactiveUserError(AppError):
    status_code = 403
    detail = "User account is inactive"
