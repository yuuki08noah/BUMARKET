from starlette import status


class AuthException(Exception):
    def __init__(self, message, status_code: int = status.HTTP_401_UNAUTHORIZED):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class JwtRequiredException(AuthException):
    def __init__(self):
        super().__init__(
            message=f"jwt required",
        )
class AdminRequiredException(AuthException):
    def __init__(self):
        super().__init__(
            message=f"어드민 required"
        )