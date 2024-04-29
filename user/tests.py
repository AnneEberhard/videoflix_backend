from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.valid_payload = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword'
        }

    def test_registration_success(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('success', response.data)
        self.assertEqual(len(mail.outbox), 1)  # Check if an email is sent

    def test_registration_existing_email(self):
        # Create a user with the email used in valid payload
        User = get_user_model()
        existing_user = User.objects.create_user(email=self.valid_payload['email'], username='existinguser', password='existingpassword')
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Email already exists')

    def test_registration_missing_fields(self):
        # Payload without email field
        invalid_payload = {'username': 'testuser', 'password': 'testpassword'}
        with self.assertRaises(ValueError):
            self.client.post(self.register_url, invalid_payload, format='json')


class ActivationTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', username='testuser', password='testpassword')
        self.activation_success_url = reverse('activation_success')
        self.activation_failure_url = reverse('activation_failure')
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_activation_success(self):
        response = self.client.get(reverse('activate', args=[self.uidb64, self.token]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.activation_success_url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activation_failure_invalid_uid(self):
        response = self.client.get(reverse('activate', args=['invalid_uidb64', self.token]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.activation_failure_url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activation_failure_invalid_token(self):
        response = self.client.get(reverse('activate', args=[self.uidb64, 'invalid_token']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.activation_failure_url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activation_failure_invalid_user(self):
        User = get_user_model()
        uid = urlsafe_base64_encode((self.user.pk + 1).to_bytes(4, 'big'))  # Use an invalid user ID
        response = self.client.get(reverse('activate', args=[uid, self.token]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.activation_failure_url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpassword', is_active=True)

    def test_login_success(self):
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Account not activated')
 
    def test_login_invalid_credentials(self):
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Unable to log in with provided credentials.')


class ForgotViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.forgot_url = reverse('forgot')
        self.invalid_payload = {'email': 'invalid@example.com'}

    def test_forgot_password_success(self):
        email = 'test@example.com'
        get_user_model().objects.create(email=email)
        valid_payload = {'email': email}
        response = self.client.post(self.forgot_url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.json())
 
    def test_forgot_password_invalid_email(self):
        response = self.client.post(self.forgot_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())

    def test_forgot_password_invalid_payload(self):
        response = self.client.post(self.forgot_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ResetViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.reset_url = reverse('password_reset_confirm', kwargs={'uidb64': 'MQ', 'token': 'c67fc6-de05441d5fd5fc3abf49779eb39cf470'})
        self.user = get_user_model().objects.create_user(email='test@example.com', password='oldpassword')
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = PasswordResetTokenGenerator().make_token(self.user)
        self.new_password = 'newpassword'
        self.data = {'password': self.new_password}
        
    def test_reset_password_success(self):
        reset_url = reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token})
        response = self.client.post(reset_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.json())
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_password))

    def test_reset_password_invalid_token(self):
        invalid_token = 'invalid-token'
        reset_url = reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': invalid_token})
        response = self.client.post(reset_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid token', response.json()['error'])

    def test_reset_password_invalid_user(self):
        invalid_uidb64 = 'invalid-uidb64'
        reset_url = reverse('password_reset_confirm', kwargs={'uidb64': invalid_uidb64, 'token': self.token})
        response = self.client.post(reset_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid user or token', response.json()['error'])

