import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app import app  
from utils.data_utils import DataUtils
from unittest.mock import MagicMock, patch

class TestApp(unittest.TestCase):
    """
    Test suite for the FastAPI app endpoints.
    """
    def setUp(self):
        """
        Set up the test client and mock SQL instance for each test.
        """
        self.client = TestClient(app)
        self.mock_sql_instance = MagicMock()

    def test_read_main(self):
        """
        Test the root endpoint ("/") to ensure it returns a status code of 200
        and the correct JSON response.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"msg": "Hello World"})

    @patch.object(DataUtils, 'get_patient_by_insurance_no')
    @patch.object(DataUtils, 'insert_interactions')
    def test_create_interactions(self, mock_insert_interactions, mock_get_patient_by_insurance_no):
        """
        Test the endpoint for creating patient interactions. Mocks the
        DataUtils methods to test the creation process without a real database.
        
        Args:
            mock_insert_interactions: Mock for the insert_interactions method.
            mock_get_patient_by_insurance_no: Mock for the get_patient_by_insurance_no method.
        """
        # Mock interaction data
        interaction_data = {
            "id": 18,
            "insurance_no": "123",
            "ailment": "Cough",
            "symptoms": "Fever",
            "interaction_date": "2024-06-29",
            "metrics": {},
            "remarks": "",
            "health_status": 7,
            "qa": {'since': '4 days'},
            "next_steps": {
                "next_visit": "2024-06-29",
                "prescribed_meds": ["GRE"],
                "prescribed_tests": ["blood"],
                "prescribed_specialist": "cardiologist"
            },
            "label": "Cough"
        }

        mock_get_patient_by_insurance_no.return_value = [
            {
                "insurance_no": "123",
                "fname": "John",
                "lname": "Doe",
                "addr": "123 Main St",
                "age": 35,
                "sex": "M",
                "ph_no": "123-456-7890",
                "email": "john.doe@example.com",
                "related_docs": "",
                "habits": "None",
                "pre_existing_conditions": "None",
                "pre_existing_medications": "None",
                "blood_type": "O+",
                "insurance_provider": "XYZ Insurance"
            }
        ]

        response = self.client.post("/interactions/", json=interaction_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Patient Interaction created successfully"})

    @patch.object(DataUtils, 'get_patient_by_insurance_no')
    @patch.object(DataUtils, 'insert_interactions')
    def test_get_interactions(self, mock_insert_interactions, mock_get_patient_by_insurance_no):
        """
        Test the endpoint for retrieving interactions by insurance number.
        Mocks the DataUtils methods to simulate database operations.
        
        Args:
            mock_insert_interactions: Mock for the insert_interactions method.
            mock_get_patient_by_insurance_no: Mock for the get_patient_by_insurance_no method.
        """
        mock_get_patient_by_insurance_no.return_value = [
            {
                "insurance_no": "111",
                "fname": "Vernon",
                "lname": "Lopez",
                "addr": "Berliner Straße 123",
                "age": 30,
                "sex": "M",
                "ph_no": "0171 234567",
                "email": "vernon@yahoo.co.in",
                "related_docs": None,
                "habits": "smoking, drinking",
                "pre_existing_conditions": "Asthma",
                "pre_existing_medications": "GTH 30mg",
                "blood_type": "B+",
                "insurance_provider": "ABC"
            }
        ]
        mock_insert_interactions.return_value = [{
            "id": 18,
            "insurance_no": "123",
            "ailment": "Cough",
            "symptoms": "Fever",
            "interaction_date": "2024-06-29",
            "metrics": {},
            "remarks": "",
            "health_status": 7,
            "qa": {'since': '4 days'},
            "next_steps": {
                "next_visit": "2024-06-29",
                "prescribed_meds": ["GRE"],
                "prescribed_tests": ["blood"],
                "prescribed_specialist": "cardiologist"
            },
            "label": "Cough"
        }]

        response = self.client.get("/patient/111/")
        assert response.status_code == 200
        assert response.json()[0]["insurance_no"] == "111"

    @patch.object(DataUtils, 'get_patient_by_insurance_no')
    def test_get_patient_info_existent_insurance_no(self, mock_get_patient_by_insurance_no):
        """
        Test the endpoint for retrieving patient information by an existing
        insurance number. Mocks the DataUtils method to simulate a database call.
        
        Args:
            mock_get_patient_by_insurance_no: Mock for the get_patient_by_insurance_no method.
        """
        mock_get_patient_by_insurance_no.return_value = [
            {
                "insurance_no": "111",
                "fname": "Vernon",
                "lname": "Lopez",
                "addr": "Berliner Straße 123",
                "age": 30,
                "sex": "M",
                "ph_no": "0171 234567",
                "email": "vernon@yahoo.co.in",
                "related_docs": None,
                "habits": "smoking, drinking",
                "pre_existing_conditions": "Asthma",
                "pre_existing_medications": "GTH 30mg",
                "blood_type": "B+",
                "insurance_provider": "ABC"
            }
        ]

        response = self.client.get("/patient/111/")
        assert response.status_code == 200
        assert response.json()[0]["insurance_no"] == "111"

    @patch.object(DataUtils, 'get_patient_by_insurance_no')
    def test_get_patient_info_nonexistent_insurance_no(self, mock_get_patient_by_insurance_no):
        """
        Test the endpoint for retrieving patient information by a nonexistent
        insurance number. Mocks the DataUtils method to simulate a database call.
        
        Args:
            mock_get_patient_by_insurance_no: Mock for the get_patient_by_insurance_no method.
        """
        mock_get_patient_by_insurance_no.return_value = None

        response = self.client.get("/patient/456/")
        assert response.status_code == 404
        assert response.json()["detail"] == "Patient record does not exist"


if __name__ == "__main__":
    unittest.main()

