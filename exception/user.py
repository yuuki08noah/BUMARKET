from starlette import status


class UserException(Exception):
    def __init__(self, message, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class UserNotExistException(UserException):
    def __init__(self, user_id: int):
        super().__init__(
            message=f"유저 아이디 {user_id} 를 찾을 수 없다.",
            status_code=status.HTTP_404_NOT_FOUND
        )