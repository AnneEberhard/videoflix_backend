from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Video

class VideoOverviewTestCase(APITestCase):
    def setUp(self):
        self.video_overview_url = reverse('videos')
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpassword', is_active=True)
        login = self.client.post(reverse('login'), {'email': 'test@example.com', 'password': 'testpassword'}, format='json')
        token = login.data['token']
        self.token_with_prefix = 'Bearer ' + token

    def test_authenticated_user_access(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_with_prefix)
        response = self.client.get(self.video_overview_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_access(self):
        response = self.client.get(self.video_overview_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cached_data_returned(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_with_prefix)
        # Make an initial request to cache the data
        initial_response = self.client.get(self.video_overview_url)
        self.assertEqual(initial_response.status_code, status.HTTP_200_OK)
        # Make a second request to ensure cached data is returned
        cached_response = self.client.get(self.video_overview_url)
        self.assertEqual(cached_response.status_code, status.HTTP_200_OK)


class VideoModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpassword', is_active=True)

    def test_video_creation(self):
        video = Video.objects.create(
            title='Test Video',
            description='This is a test video',
            genre='Fantasy',
            video_file=SimpleUploadedFile('test_video.mp4', b'content'),
            thumbnail_file=SimpleUploadedFile('test_thumbnail.jpg', b'content')
        )

        self.assertEqual(video.title, 'Test Video')
        self.assertEqual(video.description, 'This is a test video')
        self.assertEqual(video.genre, 'Fantasy')
        self.assertTrue(video.video_file)
        self.assertTrue(video.thumbnail_file)
        print(video.thumbnail_file.name)
        self.assertTrue('test_video_thumbnail.jpg' in video.thumbnail_file.name)

    def tearDown(self):
        videos = Video.objects.all()
        for video in videos:
            if video.video_file:
                video.video_file.delete()
            if video.thumbnail_file:
                video.thumbnail_file.delete()

        
