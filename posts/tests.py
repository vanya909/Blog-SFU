from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from users.models import StudyGroup
from .models import Post


class PostDetailTest(TestCase):
    """Test post detail page"""

    def setUp(self):
        """Create two users. First will be logged in and second will not"""
        self.first_study_group = StudyGroup.objects.create(title='ABC', slug='abc')
        self.second_study_group = StudyGroup.objects.create(title='BCA', slug='bca')

        self.first_user = get_user_model().objects.create_user(
            username='firstuser',
            password='12345678',
            group=self.first_study_group
        )
        self.second_user = get_user_model().objects.create_user(
            username='seconduser',
            password='12345678',
            group=self.second_study_group
        )

        self.client.login(username='firstuser', password='12345678')

    def test_post_detail_status_code(self):
        """Test post detail page status code is 200"""
        post = Post.objects.create(
            author=self.first_user,
            only_for_group=False,
            title='SimpleTitle',
            description='SimpleDescription',
        )

        response = self.client.get(f'/posts/{post.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_status_code_reverse_lazy(self):
        """Test post detail page status code using reverse_lazy() is 200"""
        post = Post.objects.create(
            author=self.first_user,
            only_for_group=False,
            title='SimpleTitle',
            description='SimpleDescription',
        )

        response = self.client.get(reverse_lazy('post_detail', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_own_group_post_detail_status_code(self):
        """Test own group post detail page status code is 200"""
        own_group_post = Post.objects.create(
            author=self.first_user,
            only_for_group=True,
            title='SimpleTitle',
            description='SimpleDescription',
        )

        response = self.client.get(reverse_lazy('post_detail', kwargs={'pk': own_group_post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_another_group_post_detail_status_code(self):
        """Test another group post detail page status code is not 200"""
        another_group_post = Post.objects.create(
            author=self.second_user,
            only_for_group=True,
            title='SimpleTitle',
            description='SimpleDescription',
        )

        response = self.client.get(reverse_lazy('post_detail', kwargs={'pk': another_group_post.pk}))
        self.assertNotEqual(response.status_code, 200)
