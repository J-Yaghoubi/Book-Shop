from dataclasses import dataclass
from typing import ClassVar
import re
from model.exceptions import StructureError
from model.template import DBModel


@dataclass
class Comment(DBModel): 
    """
        This class act as a Comment-Table for storing the comments
    """

    STRUCTURE: ClassVar[str] = """
        id SERIAL PRIMARY KEY,
        comment TEXT NOT NULL,
        user_id int REFERENCES users (id),
        content_id int REFERENCES contents (id)
    """
    TABLE: ClassVar[str] = 'comments'
    comment : str
    user_id : int
    content_id : int   

    def __post_init__(self):
        p = re.match(r'^[\w\-\.]{1,250}$', self.comment)
        if not p:
            raise StructureError(self.comment, 'should be alphanumeric and 1~250 chars')

