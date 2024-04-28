from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


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
        self.uidb64 = urlsafe_base64_encode(self.user.pk.to_bytes(4, 'big'))
        self.token = default_token_generator.make_token(self.user)

    def test_activation_success(self):
        print(f'udib= ',self.uidb64)
        print(f'token = ',self.token)
        response = self.client.get(reverse('activate', args=[self.uidb64, self.token]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.activation_success_url)

        # Refresh user instance
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activation_failure_invalid_uid(self):
        response = self.client.get(reverse('activate', args=['invalid_uidb64', self.token]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.activation_failure_url)

        # Refresh user instance
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activation_failure_invalid_token(self):
        response = self.client.get(reverse('activate', args=[self.uidb64, 'invalid_token']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.activation_failure_url)

        # Refresh user instance
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activation_failure_invalid_user(self):
        User = get_user_model()
        uid = urlsafe_base64_encode((self.user.pk + 1).to_bytes(4, 'big'))  # Use an invalid user ID
        response = self.client.get(reverse('activate', args=[uid, self.token]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.activation_failure_url)

        # Refresh user instance
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
