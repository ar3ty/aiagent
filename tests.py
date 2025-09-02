import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

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
        self.assertTrue("""calculator = Calculator()
    if len(sys.argv) <= 1:""" in result)
    
    def test_inner2(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        self.assertTrue("""def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }""" in result)

    def test_outer(self):
        result = get_file_content("calculator", "/bin/cat")
        self.assertEqual(result, 'Error: Cannot read "/bin/cat" as it is outside the permitted working directory')
    
    def test_doesnt_exist(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        self.assertEqual(result, 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"')

class TestWriteContent(unittest.TestCase):
    def test_inner(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        self.assertEqual('Successfully wrote to "lorem.txt" (28 characters written)', result)
    
    def test_create(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        self.assertEqual('Successfully wrote to "pkg/morelorem.txt" (26 characters written)', result)

    def test_outer(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        self.assertEqual('Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory', result)
    
class TestExecuteCode(unittest.TestCase):
    def test_inner(self):
        result = run_python_file("calculator", "main.py")
        self.assertTrue("STDOUT:" in result)
    
    def test_arg(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        self.assertTrue("STDOUT:" in result)

    def test_tests(self):
        result = run_python_file("calculator", "tests.py")
        self.assertTrue("STDERR:" in result)
        self.assertTrue("Ran 9 tests in" in result)
    
    def test_outer(self):
        result = run_python_file("calculator", "../main.py")
        self.assertEqual(result, 'Error: Cannot execute "../main.py" as it is outside the permitted working directory')

    def test_doesnt_exist(self):
        result = run_python_file("calculator", "nonexistent.py")
        self.assertEqual(result, 'Error: File "nonexistent.py" not found.')

if __name__ == "__main__":
    unittest.main()