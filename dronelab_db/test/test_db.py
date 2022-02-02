import unittest
from dronelab_db.test.base import scenario, dal

class TestDAL(unittest.TestCase):

    def test_get_session_data_blank(self):
        expected_result = list()
        result = dal.get_session_data('').values.tolist()
        self.assertEqual(result, expected_result)
    
    def test_get_all_cfs_in_session_blank(self):
        expected_result = list()
        result = dal.get_all_cfs_in_session('')
        self.assertListEqual(result, expected_result)

    def test_get_all_cfs_in_session_blank_all(self):
        expected_result = list()
        result = dal.get_all_cfs_in_session('')
        self.assertListEqual(result, expected_result)
    
    def test_get_cfs_data_from_session_blank_session_id(self):
        expected_result = list()
        result = dal.get_cfs_data_from_session('', 'cf1').values.tolist()
        self.assertListEqual(result, expected_result)
    
    def test_get_cfs_data_from_session_blank_cf_id(self):
        expected_result = list()
        result = dal.get_cfs_data_from_session(scenario['session_ids'][1], '').values.tolist()
        self.assertListEqual(result, expected_result)

    def test_get_unique_session_ids(self):
        expected_result = scenario['session_ids']
        result = dal.get_unique_session_ids()
        self.assertListEqual(result, expected_result)