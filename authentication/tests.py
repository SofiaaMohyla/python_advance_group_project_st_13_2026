from django.contrib.auth import get_user_model
from django.test import TestCase


class AuthenticationRedirectTests(TestCase):
	def test_registration_redirects_to_notebook_and_logs_user_in(self):
		response = self.client.post('/register/', {
			'username': 'new_student',
			'email': 'student@example.com',
			'password1': 'StrongPass123!',
			'password2': 'StrongPass123!',
			'role': 'user',
		})

		self.assertRedirects(response, '/notebook/')
		self.assertTrue(response.wsgi_request.user.is_authenticated)

	def test_login_redirects_to_notebook(self):
		get_user_model().objects.create_user(username='student', password='StrongPass123!')

		response = self.client.post('/login/', {
			'username': 'student',
			'password': 'StrongPass123!',
		})

		self.assertRedirects(response, '/notebook/')
