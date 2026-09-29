from flask import Flask

from .exceptions import ConflictError, ForbiddenError, NotFoundError, UnauthorizedError


# Satu-satunya tempat yang menerjemahkan error bisnis menjadi status HTTP.
# Ganti framework = cukup tulis ulang file ini, service tidak ikut berubah.
def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(NotFoundError)
    def handle_not_found(error: NotFoundError):
        return {"detail": error.message}, 404

    @app.errorhandler(ConflictError)
    def handle_conflict(error: ConflictError):
        return {"detail": error.message}, 409

    @app.errorhandler(ForbiddenError)
    def handle_forbidden(error: ForbiddenError):
        return {"detail": error.message}, 403

    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized(error: UnauthorizedError):
        return {"detail": error.message}, 401
