import pytest
from model.user import User
from model.comment import Comment
from model.content import Content
from exceptions import *


class TestUserModel:

    def test_user_success(self):
        self.p1 = User('jafar', 'Yaghoubi', '09123536842', '0386628221', 'jeff', 'qwer!1234')
        assert self.p1.first_name == 'jafar'
        assert self.p1.last_name == 'Yaghoubi'
        assert self.p1.phone == '09123536842'
        assert self.p1.national_id == '0386628221'
        assert self.p1.username == 'jeff'
        assert self.p1.password
        assert self.p1.code
        assert self.p1.permission

    @pytest.mark.parametrize('first_name, last_name, phone, national_id, username, password',
        [
            ('1', 'Yaghoubi', '09123536842', '0386628221', 'jeff', 'qwer!1234'), 
            ('jafar', 'Yaghoubi', '123536842', '0386628221', 'jeff', 'qwer!1234'), 
            ('jafar', '1', '09123536842', '0386628221', 'jeff', 'qwer!1234'), 
            ('jafar', 'Yaghoubi', '1', '0386628221', 'jeff', 'qwer!1234'), 
            ('jafar', 'Yaghoubi', '09123536842', '1', 'jeff', 'qwer!1234'), 
            ('jafar', 'Yaghoubi', '09123536842', '0386628221', '1', 'qwer!1234'), 
            ('jafar', 'Yaghoubi', '09123536842', '0386628221', 'jeff', '1'), 
            ('jafar', 'Yaghoubi', '09123536842', '0386628221', 'jeff', '123454567!')               
        ]
    )
    def test_user_raise_structure(self, first_name, last_name, phone, national_id, username, password):
        pytest.raises(StructureError, User, first_name, last_name, phone, national_id, username, password)

    @pytest.mark.parametrize('first_name, last_name, phone, national_id, username, password',
        [
            (1, 'Yaghoubi', '09123536842', '0386628221', 'jeff', 'qwer!1234'),
            ('jafar', 1, '09123536842', '0386628221', 'jeff', 'qwer!1234'),
            ('jafar', 'Yaghoubi', 1, '0386628221', 'jeff', 'qwer!1234'),    
            ('jafar', 'Yaghoubi', '09123536842', 1, 'jeff', 'qwer!1234'), 
            ('jafar', 'Yaghoubi', '09123536842', '0386628221', 1, 'qwer!1234'), 
            ('jafar', 'Yaghoubi', '09123536842', '0386628221', 'jeff', 1)           
        ]
    )
    def test_user_raise_type(self, first_name, last_name, phone, national_id, username, password):
        pytest.raises(InputTypeError, User, first_name, last_name, phone, national_id, username, password)


class TestCommentModel:

    def test_comment_success(self):
        self.p1 = Comment('this is my comment', '1', '2')
        assert self.p1.comment == 'this is my comment'
        assert self.p1.user_id == '1'
        assert self.p1.content_id == '2'

    @pytest.mark.parametrize('comment, user_id, content_id',
        [
            ('', '1', '1'),
            ('comment', '10000000000', '1'), 
            ('comment', '1', '10000000000'), 
            ('comment', 'abc', '1'), 
            ('comment', '1', 'abc')           
        ]
    )

    def test_comment_raise(self, comment, user_id, content_id):
        pytest.raises(StructureError, Comment, comment, user_id, content_id)  


class TestContentModel:

    def test_content_success(self):
        self.p1 = Content('Seyed Jafar Yaghoubi', '1', 'file')
        assert self.p1.owner == 'Seyed Jafar Yaghoubi'
        assert self.p1.user_id == '1'
        assert self.p1.name == 'file'

    @pytest.mark.parametrize('owner, user_id, name',
        [
            ('', '1', 'file'),
            ('foo', '', '1'), 
            ('foo', '1', ''),         
        ]
    )

    def test_content_raise(self, owner, user_id, name):
        pytest.raises(StructureError, Content, owner, user_id, name)  
