import unittest
from unittest.mock import MagicMock, patch
from src.database.auth import AuthService

class TestAuthService(unittest.TestCase):

    @patch('src.database.auth.supabase')
    def test_sign_up_success(self, mock_supabase):
        # Setup mock
        mock_response = MagicMock()
        mock_response.user = {'id': '123', 'email': 'test@example.com'}
        mock_supabase.auth.sign_up.return_value = mock_response

        # Execute
        result = AuthService.sign_up('test@example.com', 'password', 'Test User')

        # Assert
        self.assertEqual(result['user'], {'id': '123', 'email': 'test@example.com'})
        self.assertIsNone(result['error'])
        mock_supabase.auth.sign_up.assert_called_once()

    @patch('src.database.auth.supabase')
    def test_sign_in_success(self, mock_supabase):
        # Setup mock
        mock_response = MagicMock()
        mock_response.user = {'id': '123'}
        mock_response.session = {'access_token': 'token'}
        mock_supabase.auth.sign_in_with_password.return_value = mock_response

        # Execute
        result = AuthService.sign_in('test@example.com', 'password')

        # Assert
        self.assertEqual(result['user'], {'id': '123'})
        self.assertIsNone(result['error'])

    @patch('src.database.auth.supabase')
    def test_sign_up_failure(self, mock_supabase):
        # Setup mock to raise exception
        mock_supabase.auth.sign_up.side_effect = Exception("Auth error")

        # Execute
        result = AuthService.sign_up('test@example.com', 'password', 'Test User')

        # Assert
        self.assertIsNone(result['user'])
        self.assertEqual(result['error'], "Auth error")

if __name__ == '__main__':
    unittest.main()
