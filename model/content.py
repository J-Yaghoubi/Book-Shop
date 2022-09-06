from dataclasses import dataclass
from typing import ClassVar
import re
from exceptions import *
from model.template import DBModel


@dataclass()
class Content(DBModel): 
    """
        This class act as a Content-Table for storing the information 
        of the stored file in store
    """

    STRUCTURE: ClassVar[str] = """
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        owner VARCHAR(50) NOT NULL,
        user_id int REFERENCES users (id),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    """
    TABLE: ClassVar[str] = 'contents'
    owner : str
    user_id : int
    name : str

    messages: ClassVar[list] = [
        'alphanumeric with 1~50 chars',
        'numeric max 10 digits',
        'numeric max 10 digits'
    ]

    patterns: ClassVar[dict] = {
        'owner': r'^[a-zA-Z]+[a-zA-Z\- ]{1,50}[a-zA-Z]{1}$',
        'user_id': r'^\d{1,10}$',
        'name': r'^[\w\-\.]{1,50}$'
    }

    def __post_init__(self):
        counter = 0
        for key, value in self.__dict__.items():
            if not re.match(self.__class__.patterns[key], str(value)):
                raise StructureError(key, self.__class__.messages[counter])
            counter += 1
