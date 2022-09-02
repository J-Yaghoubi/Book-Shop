from core.managers import DBManager
from model.user import User
from model.content import Content
from model.comment import Comment


"""
    Create database if not exists:
"""
try:
    DBManager().make()
except:
    pass    


"""
    Check for tables(models) and make them if is not exists
"""

DBManager().create(User)
DBManager().create(Content)
DBManager().create(Comment)

