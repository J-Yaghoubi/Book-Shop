from dataclasses import dataclass
from configs import DbConfig
from typing import ClassVar
import re
from exceptions import StructureError
from model.template import DBModel
from uuid import uuid4
from hashlib import sha1


@dataclass()
class User(DBModel):
    """
        This class act as a User-Table for storing the 
        information of the registered users
    """

    STRUCTURE: ClassVar[str] = """
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(30) NOT NULL,
        last_name VARCHAR(30) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        national_id VARCHAR(10) NOT NULL,
        username VARCHAR(20) UNIQUE NOT NULL,
        password VARCHAR(50) NOT NULL,
        balance INT DEFAULT 0,
        code VARCHAR(50) NOT NULL,
        permission VARCHAR(20) NOT NULL
    """
    TABLE: ClassVar[str] = 'users'
    first_name: str
    last_name: str
    phone: str
    national_id: str
    username: str
    password: str
    balance: str = '0'
    code: str = str(uuid4())
    permission: str = 'basic'

    columns:  ClassVar[list] = [
        'First name', 'Last Name', 'Phone', 'National ID', 'Username', 'Password'
    ]

    messages: ClassVar[list] = [
        'alphabetic 2~14 char',
        'alphabetic 2~14 char',
        'numeric, prefix and 9 digits',
        'numeric with 10 digits',
        'alphanumeric 4~20 char',
        'complex with 8~40 char',
        'numeric max 10 digits',
        'max 40 chars',
        'max 20 chars'
    ]

    patterns: ClassVar[dict] = {
        'first_name': r'^([a-zA-Z]+[a-zA-Z\-]*[a-zA-Z]+){,20}$',
        'last_name': r'^([a-zA-Z]+[a-zA-Z\-]*[a-zA-Z]+){,20}$',
        'phone': r'^(09|\+98)[\d]{9}$',
        'national_id': r'^0\d{9}$',
        'username': r'^\w{4,20}$',
        'password': r'^(?=.*\d)(?=.*[a-z])(?=.*[a-zA-Z]).{8,40}$',
        'balance': r'^\d{1,10}$',
        'code': r'^.{1,40}$',
        'permission': r'^.{1,20}$'
    }

    # Validate the input with special regex patterns
    def __post_init__(self):
        counter = 0
        for key, value in self.__dict__.items():
            if not re.match(self.__class__.patterns[key], value):
                raise StructureError(key, self.__class__.messages[counter])
            counter += 1

        passphrase = DbConfig.PASSWORD.value + self.password
        self.password = sha1(passphrase.encode()).hexdigest()


