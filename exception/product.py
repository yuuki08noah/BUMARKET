from starlette import status


class ProductException(Exception):
    def __init__(self, message, status_code: int = status.HTTP_404_NOT_FOUND):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ImageInvalidException(ProductException):
    def __init__(self):
        super().__init__(
            message=f"Image Invalid"
        )