class AppError(Exception):
    """Induk semua error bisnis. Tidak tahu apa-apa soal HTTP atau framework."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(AppError):
    """Data yang dicari tidak ada."""


class ConflictError(AppError):
    """Bentrok dengan data/aturan yang sudah ada (misal: email sudah terdaftar)."""


class ForbiddenError(AppError):
    """Sudah login, tapi tidak punya hak untuk aksi ini."""


class UnauthorizedError(AppError):
    """Belum login atau kredensial salah."""
