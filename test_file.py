"""File for testing functionality"""

from unittest import TestCase
from server import app
from model import connect_to_db, db
from flask import session


class FlaskTestCreateUser(TestCase):
    """Create account with a new caregiver & user"""

    def setUp(self):
        """Prepare the test field"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage"""

        result = self.client.get('/')
        self.assertIn(b"Create a New Shower", result.data)

    def test_login(self):
        """Create test user"""

        result = self.client.post("/create_user", data={"user_name": "Lola", 
                                "cg_email": "jo@aol.com", "cg_pass": 
                                "qwertyuiop", "cg_phone": "123-456-7890"}, 
                                follow_redirects=True)

        self.assertIn(b"Welcome!", result.data)

if __name__ == "__main__":
    import unittest

    unittest.main()