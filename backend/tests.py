import unittest
from flask import Flask
from flask.testing import FlaskClient
import os
from io import BytesIO
from app import app

class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def upload_file(self, filename, tag=None):
        with open(filename, 'rb') as file:
            data = {'file': (BytesIO(file.read()), filename)}
        if tag:
            query_params = {}
            query_params['tag'] = tag
            response = self.app.post('/save_file', query_string=query_params, data=data, content_type='multipart/form-data')
        else:
            response = self.app.post('/save_file', data=data, content_type='multipart/form-data')
        return response
        
    def test_health_check(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Health check ok!')

    def test_no_file(self):
        response = self.app.post('/save_file')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'No file')

    def test_wrong_file_format(self):
        response = self.upload_file('test.txt')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Unable read file')

    def test_missing_tag(self):
        response = self.upload_file('IM000001.dcm')
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'No DICOM Tag provided')

    def test_valid_input(self):
        filenames = ['IM000001.dcm', 'IM000002.dcm', 'IM000003.dcm', 'IM000004.dcm', 'IM000005.dcm', 'IM000006.dcm']
        for filename in filenames:    
            response = self.upload_file(filename, tag='PatientName')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIn('attribute_value', data)
            self.assertIn('dicom_image', data)
            self.assertTrue(os.path.isfile(filename))

if __name__ == '__main__':
    unittest.main()
