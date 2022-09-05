from dataclasses import dataclass
from typing import ClassVar
import re
from exceptions import StructureError
from model.template import DBModel


@dataclass(slots=True)
class Content(DBModel): 
    """
        This class act as a Content-Table for storing the information 
        of the stored file in store
    """

    STRUCTURE: ClassVar[str] = """
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        owner VARCHAR(100) NOT NULL,
        user_id int REFERENCES users (id),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    """
    TABLE: ClassVar[str] = 'contents'
    owner : str
    user_id : int
    name : str

    def __post_init__(self):
        p = re.match(r'^[\w\-\.]{1,50}$', self.name)
        if not p:
            raise StructureError(self.name, 'should be alphanumeric and 1~50 chars')

