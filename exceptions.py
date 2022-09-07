
class CustomException(Exception):
    """Main format exceptions"""

    def __init__(self, field: str, msg: str) -> None:
        self.alert = 'Field'
        self.field = field
        self.msg = msg
    
    def __str__(self) -> str:
        return f'{self.alert}: {self.field} => {self.msg}'


class StructureError(CustomException):
    pass


class InputTypeError(CustomException):
    pass


class BadQueryError(CustomException):
    pass
