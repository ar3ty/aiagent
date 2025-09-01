import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

class TestGetFilesInfo(unittest.TestCase):
    def test_current(self):
        result = get_files_info("calculator", ".")
        self.assertTrue(" - main.py: file_size=" in result)
        self.assertTrue(" - tests.py: file_size=" in result)
        self.assertTrue(" - pkg: file_size=" in result)
    
    def test_inner(self):
        result = get_files_info("calculator", "pkg")
        self.assertTrue(" - calculator.py: file_size=" in result)
        self.assertTrue(" - render.py: file_size=" in result)

    def test_outer(self):
        result = get_files_info("calculator", "/bin")
        self.assertEqual(result, """Error: Cannot list "/bin" as it is outside the permitted working directory""")
    
    def test_outer_2(self):
        result = get_files_info("calculator", "../")
        self.assertEqual(result, """Error: Cannot list "../" as it is outside the permitted working directory""")
    
class TestGetFileContent(unittest.TestCase):
    def test_inner(self):
        result = get_file_content("calculator", "main.py")
        print(result)
        self.assertTrue("""calculator = Calculator()
    if len(sys.argv) <= 1:""" in result)
    
    def test_inner2(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result)
        self.assertTrue("""def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }""" in result)

    def test_outer(self):
        result = get_file_content("calculator", "/bin/cat")
        print(result)
        self.assertEqual(result, 'Error: Cannot read "/bin/cat" as it is outside the permitted working directory')
    
    def test_doesnt_exist(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        print(result)
        self.assertEqual(result, 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"')

if __name__ == "__main__":
    unittest.main()