import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_current(self):
        result = get_files_info("calculator", ".")
       
        print(result)
    
    def test_inner(self):
        result = get_files_info("calculator", "pkg")
        self.assertEqual(result, """Result for 'pkg' directory:
 - calculator.py: file_size=1739 bytes, is_dir=False
 - render.py: file_size=768 bytes, is_dir=False""")

    def test_outer(self):
        result = get_files_info("calculator", "/bin")
        self.assertEqual(result, """Result for '/bin' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory""")
    
    def test_outer_2(self):
        result = get_files_info("calculator", "../")
        self.assertEqual(result, """Result for '../' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory""")

if __name__ == "__main__":
    unittest.main()