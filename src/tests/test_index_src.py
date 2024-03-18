import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import index_src



TEST_SRC = "c_example/test.c"

EXPECT_RESULT = [

]


def test_index_src():
    index_src.init_db()
    index_src.index_src_file(TEST_SRC)
    

if __name__ == "__main__":
    test_index_src()