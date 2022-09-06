import pytest
from core.cryptic import *
import os


class TestCryptic:

    @pytest.fixture
    def setup(self) -> None:

        print('------------------SetUP---------------')
        with open('test.txt', 'w') as f:
            f.write('test')

        with open('key.key', 'w') as f:
            f.write('test')            

        yield 'setup'
        print('-----------------TearDown-------------')

        os.remove(f"test.txt")
        os.remove(f"key.key")

    def test_cryptic(self, setup):
        write_key('key.key')
        key = load_key('key.key')

        encrypt('test.txt', key)

        with open('test.txt', 'r') as f:
            data = f.read()
        assert data != 'test'

        decrypt('test.txt', key)

        with open('test.txt', 'r') as f:
            data = f.read()
        assert data == 'test'
