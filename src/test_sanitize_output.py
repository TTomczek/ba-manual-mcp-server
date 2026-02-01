import unittest

from src.sanitize_output import sanitize_output


class TestSanitizeOutput(unittest.IsolatedAsyncioTestCase):
    async def test_sanitize_string(self):

        @sanitize_output()
        async def dummy_function():
            return "password: 12345, path: ../secrets/../'nuclear_codes.txt'"

        result = await dummy_function()
        self.assertEqual(result, "password: ****, path: secrets/\\'nuclear_codes.txt\\'")


    async def test_sanitize_dict(self):
        @sanitize_output()
        async def dummy_function():
            return {
                "username": "user123",
                "password": "mysecretpassword",
                "file_path": "/home/user/../secret/file.txt",
                "api_key": "ABC123XYZ",
                "notes": 'He said, "Hello!" and left.'
            }

        result = await dummy_function()
        self.assertEqual(result, {
            "username": "user123",
            "password": "****",
            "file_path": "/home/user/secret/file.txt",
            "api_key": "****",
            "notes": 'He said, \\"Hello!\\" and left.'
        })

    async def test_sanitize_list(self):
        @sanitize_output()
        async def dummy_function():
            return [
                "user123",
                "mysecretpassword",
                "/home/user/../secret/file.txt",
                "ABC123XYZ",
                'He said, "Hello!" and left.'
            ]



if __name__ == '__main__':
    unittest.main()
