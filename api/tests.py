"""API tests"""
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from users.models import StudyGroup
from posts.models import Post
from .serializers import PostSerializer


def get_test_user(username, password, group_title):
    """Function which returns a new user for tests"""
    group = StudyGroup.objects.get_or_create(title=group_title)[0]
    return get_user_model().objects.create_user(username=username, password=password, group=group)


class GetPostsApiTest(APITestCase):
    """Class which tests receiving posts using API"""
    def setUp(self):
        """Creating test user and two test posts, one of which is public"""
        self.test_user = get_test_user('testuser', '12345678', 'ABC')
        self.client.login(username='testuser', password='12345678')

        self.public_post = Post.objects.create(
            author=self.test_user,
            only_for_group=False,
            description='Post1'
        )

        self.group_post = Post.objects.create(
            author=self.test_user,
            only_for_group=True,
            description='Post2'
        )

    def test_post_api_get_status_code(self):
        """Test page status code is 200"""
        response = self.client.get('/api/posts/')
        self.assertEqual(
            response.status_code, 200,
            msg="Detail page status code isn't 200"
        )

    def test_post_api_get_status_code_reverse_lazy(self):
        """Test page status code using reverse_lazy() is 200"""
        response = self.client.get(reverse_lazy('get_public_posts'))
        self.assertEqual(
            response.status_code, 200,
            msg="Detail page status code using reverse_lazy() isn't 200"
        )

    def test_post_api_get(self):
        """Test receiving posts using API"""
        response = self.client.get(reverse_lazy('get_public_posts'), format='json')

        self.assertEqual(
            len(response.data), 1,
            msg="Number of posts is differs from one"
        )
        self.assertIn(
            PostSerializer(self.public_post).data, response.data,
            msg="Public post isn't in the data"
        )
        self.assertNotIn(
            PostSerializer(self.group_post).data, response.data,
            msg="Group post is in the data"
        )
