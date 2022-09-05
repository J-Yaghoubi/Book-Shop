from enum import Enum

class LoggedUser: 
    ID = None
    FIRSTNAME = None
    LASTNAME = None
    PHONE = None
    NATIONAL = None
    USERNAME = None
    PASSWORD = None
    BALANCE = None
    CODE = None
    FULLNAME = None

class DbConfig(Enum):
    DATABASE = "bookshop"
    HOST = "localhost"
    USER = "postgres"
    PORT = 5432
    PASSWORD = ""

class Info(Enum):
    PROJECT = "Book Shop"
    VERSION = "1.0.0"
    AUTHOR = "Seyed Jafar Yaghoubi"
    DESCRIPTION = "This is a micro project that simulate a\n book-store with python and postgresql"

