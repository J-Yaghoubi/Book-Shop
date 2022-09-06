import pytest
from model.user import User
from model.comment import Comment
from model.content import Content
from exceptions import *


class TestUserModel:

    def test_user_happy(self):
        self.p1 = User('jafar', 'Yaghoubi', '09123536842', '0386628221', 'jeff', 'qwer!1234')
        assert self.p1.first_name == 'jafar'
        assert self.p1.last_name == 'Yaghoubi'
        assert self.p1.phone == '09123536842'
        assert self.p1.national_id == '0386628221'
        assert self.p1.username == 'jeff'
        assert self.p1.password
        assert self.p1.code
        assert self.p1.permission

    def test_user_sad(self):
        pytest.raises(TypeError, User)
        pytest.raises(InputTypeError, User, 1, 'Yaghoubi', '09123536842', '0386628221', 'jeff', 'qwer!1234')
        pytest.raises(InputTypeError, User, 'jafar', 1, '09123536842', '0386628221', 'jeff', 'qwer!1234')
        pytest.raises(InputTypeError, User, 'jafar', 'Yaghoubi', 1, '0386628221', 'jeff', 'qwer!1234')
        pytest.raises(InputTypeError, User, 'jafar', 'Yaghoubi', '09123536842', 1, 'jeff', 'qwer!1234')
        pytest.raises(InputTypeError, User, 'jafar', 'Yaghoubi', '09123536842', '0386628221', 1, 'qwer!1234')
        pytest.raises(InputTypeError, User, 'jafar', 'Yaghoubi', '09123536842', '0386628221', 'jeff', 1)                                   
        pytest.raises(StructureError, User, '1', 'Yaghoubi', '09123536842', '0386628221', 'jeff', 'qwer!1234')   
        pytest.raises(StructureError, User, 'jafar', 'Yaghoubi', '123536842', '0386628221', 'jeff', 'qwer!1234')  
        pytest.raises(StructureError, User, 'jafar', '1', '09123536842', '0386628221', 'jeff', 'qwer!1234')   
        pytest.raises(StructureError, User, 'jafar', 'Yaghoubi', '1', '0386628221', 'jeff', 'qwer!1234')   
        pytest.raises(StructureError, User, 'jafar', 'Yaghoubi', '09123536842', '1', 'jeff', 'qwer!1234')          
        pytest.raises(StructureError, User, 'jafar', 'Yaghoubi', '09123536842', '0386628221', '1', 'qwer!1234')   
        pytest.raises(StructureError, User, 'jafar', 'Yaghoubi', '09123536842', '0386628221', 'jeff', '1')         
        pytest.raises(StructureError, User, 'jafar', 'Yaghoubi', '09123536842', '0386628221', 'jeff', '123454567!')         


class TestCommentModel:

    def test_comment_happy(self):
        self.p1 = Comment('this is my comment', '1', '2')
        assert self.p1.comment == 'this is my comment'
        assert self.p1.user_id == '1'
        assert self.p1.content_id == '2'

    def test_comment_sad(self):
        pytest.raises(StructureError, Comment, '', '1', '1')  
        pytest.raises(StructureError, Comment, 'comment', '10000000000', '1')         
        pytest.raises(StructureError, Comment, 'comment', '1', '10000000000')   
        pytest.raises(StructureError, Comment, 'comment', 'abc', '1')         
        pytest.raises(StructureError, Comment, 'comment', '1', 'abc') 


class TestContentModel:

    def test_comment_happy(self):
        self.p1 = Content('Seyed Jafar Yaghoubi', '1', 'file')
        assert self.p1.owner == 'Seyed Jafar Yaghoubi'
        assert self.p1.user_id == '1'
        assert self.p1.name == 'file'

    def test_comment_sad(self):
        pytest.raises(StructureError, Content, '', '1', 'file')  
        pytest.raises(StructureError, Content, 'owner', '', 'file')         
        pytest.raises(StructureError, Content, 'owner', '1', '') 