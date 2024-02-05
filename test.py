import unittest
import json

class TestJsonStructure(unittest.TestCase):
    def test_json_structure(self):
        json_obj = {
            "Title": "Data Scientist",
            "Agency": "National Nuclear Security Administration",
            # ... rest of your JSON object
        }

        expected_keys = {
            "Title": str,
            "Agency": str,
            "Department": str,
            "SalaryDisplay": str,
            "DocumentID": str,
            "PositionID": str,
            "Location": str,
            "DateDisplay": str,
            "WorkSchedule": str,
            "WorkType": str,
            "ClockDisplay": str,
            "ShowMapIcon": bool,
            "LocationLatitude": float,
            "LocationLongitude": float,
            "HiringPath": list,
            "LowGrade": str,
            "HighGrade": str,
            "JobGrade": str,
            "LocationName": str,
            "PositionLocationCount": str,
            "PositionURI": str,
            "Relocation": str,
            "MinimumRange": str,
            "PositionEndDate": str,
            "Description": str,
            "Qualifications": str,
            "Requirements": str
        }

        for key, value_type in expected_keys.items():
            self.assertIn(key, json_obj)
            self.assertIsInstance(json_obj[key], value_type)

if __name__ == '__main__':
    unittest.main()