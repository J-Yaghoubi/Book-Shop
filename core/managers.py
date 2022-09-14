import psycopg2
import psycopg2.extras
from psycopg2._psycopg import connection

from model.template import DBModel
from configs import DbConfig
from exceptions import BadQueryError

class DBManager:

    def __init__(self) -> None:

        self.conn: connection = \
            psycopg2.connect(dbname=DbConfig.DATABASE.value, user=DbConfig.USER.value,
                             host=DbConfig.HOST.value, port=DbConfig.PORT.value, password=DbConfig.PASSWORD.value)
        self.conn.autocommit = True

    def _remove_quotes(self, coted_tpl: tuple) -> str:
        """
            Remove quotes from tuple and return as string
        """
        temp = ''
        for i in list(coted_tpl):
            temp += str(i).replace("'", "") + ', '
        return ('(' + temp + ')').replace(', )', ')')

    def _add_quotes(self, coted_tpl: tuple) -> str:
        """
            Add quotes to the tuple members and return as string
        """
        temp = ''
        for i in list(coted_tpl):
            if isinstance(i, str):
                temp += "'" + str(i) + "'" + ', '
            else:
                temp += str(i) + ', '
                    
        return ('(' + temp + ')').replace(', )', ')')

    def __del__(self):
        """
            Close the connection on delete
        """
        self.conn.close()  

    def _execute(self, query: str, data: bool = False) -> list | None:
        """
            Execute the query
        """
        try:
            with self.conn.cursor() as curs:
                curs.execute(query)
                return curs.fetchall() if data else None         
        except:
            raise BadQueryError('Query', query)


    def make(self) -> None:
        """
            make the database
        """
        query = f"CREATE DATABASE {DbConfig.DATABASE.value};"
        self._execute(query)       

    def create(self, model_instance: DBModel) -> None:
        """
            Create tables from information of models
        """
        query = f"CREATE TABLE IF NOT EXISTS {model_instance.TABLE} ({model_instance.STRUCTURE});"
        self._execute(query)

    def insert(self, model_instance: DBModel) -> None:
        """
            insert data to the table
        """
        query = f"INSERT INTO {model_instance.TABLE} {self._remove_quotes(model_instance.__dict__.keys())} VALUES \
            {self._add_quotes(model_instance.__dict__.values())};"
        self._execute(query)

    def read(self, fields: str, model_class: DBModel, condition: str) -> list:
        """
            returns a list of the values
        """
        query = f"SELECT {fields} FROM {model_class.TABLE} where {condition};" if  condition else f"SELECT {fields} FROM {model_class.TABLE};" 
        return self._execute(query, True)

    def update(self, model_class: DBModel, field: str, value: str, condition: str) -> None:
        """
            update selected fields based on the custom condition
        """
        query = f"UPDATE {model_class.TABLE} SET {field} = {value} WHERE {condition};"
        self._execute(query)

    def delete(self, model_class: DBModel, condition: int) -> None:
        """
            delete information from the selected table
        """
        query = f"DELETE FROM {model_class.TABLE} WHERE {condition};"   
        self._execute(query)
        