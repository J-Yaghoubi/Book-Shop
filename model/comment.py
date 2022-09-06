from dataclasses import dataclass
from typing import ClassVar
import re
from exceptions import *
from model.template import DBModel


@dataclass()
class Comment(DBModel): 
    """
        This class act as a Comment-Table for storing the comments
    """
    STRUCTURE: ClassVar[str] = """
        id SERIAL PRIMARY KEY,
        comment TEXT NOT NULL,
        user_id int REFERENCES users (id),
        content_id int REFERENCES contents (id),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    """
    TABLE: ClassVar[str] = 'comments'
    comment : str
    user_id : int
    content_id : int   

    messages: ClassVar[list] = [
        'max 250 char',
        'numeric max 10 digits',
        'numeric max 10 digits'
    ]

    patterns: ClassVar[dict] = {
        'comment': r'^.{1,250}$',
        'user_id': r'^\d{1,10}$',
        'content_id': r'^\d{1,10}$'
    }

    def __post_init__(self):
        counter = 0
        for key, value in self.__dict__.items():
            if not re.match(self.__class__.patterns[key], str(value)):
                raise StructureError(key, self.__class__.messages[counter])
            counter += 1
