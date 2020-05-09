import requests


from django.test import TestCase, Client

# Create your tests here.
class DownloadFileCase(TestCase):
    def setUp(self):
        c = Client()
        with open('.gitignore', 'rb') as f:
            response = c.generic('POST', '/push', data=f.read())
            print(response)


    def test_get_with_unsupported_method(self):
        c = Client()
        response = c.head('/get/test_file')
        self.assertEqual(response.status_code, 405)

    def test_get_not_exist_file(self):
        c = Client()
        response = c.post('/get/test_file')
        self.assertEqual(response.status_code, 404)
