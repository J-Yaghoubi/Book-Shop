import pytest
from core.managers import DBManager
from model.user import User
from exceptions import BadQueryError

"""
Note: to execute this test successfully from the root, should comment 
__init__ in model package to prevent circular input error
"""

class TestDBManager:

    @pytest.fixture
    def setup(self) -> None:
        self.db_manager = DBManager()
        self.db_manager.create(User)
        self.u1 = User('jafar', 'yaghoubi', '09123536842', '0381111111', 'jefferson', "ThisIsPassword!12")

        yield 'setup'

        try:
            self.db_manager.delete(self.u1)
        except:
            pass
        del self.db_manager

    def test_insert_success(self, setup):
        self.db_manager.insert(self.u1)

    def test_read_success(self, setup):
        find = DBManager().read('*', User, f"code = '{self.u1.code}'")[0]
        assert find != None
        assert find[1] == 'jafar'
        assert find[2] == 'yaghoubi'
        assert find[3] == '09123536842'
        assert find[4] == '0381111111'
        assert find[5] == 'jefferson'
        assert find[6] != 'ThisIsPassword!12'
        assert find[8] !=  None

    def test_update_success(self, setup):
        DBManager().update(User, 'first_name', "'ali'", f"code = '{self.u1.code}'") 
        find = DBManager().read('*', User, f"code = '{self.u1.code}'")[0]
        assert find[1] == 'ali'

    def test_delete_success(self, setup):
        DBManager().delete(User, f"code = '{self.u1.code}'") 
        find = DBManager().read('*', User, f"code = '{self.u1.code}'")
        assert find == [] 

    def test_bad_query_raise(self, setup):
        pytest.raises(BadQueryError, DBManager().read, '*', User, f"code = {self.u1.code}")
