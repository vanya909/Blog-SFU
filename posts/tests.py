from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from users.models import StudyGroup
from .models import Post


def get_test_user(username, password, group_title):
    """Function which returns a new user for tests"""
    group = StudyGroup.objects.get_or_create(title=group_title, slug=group_title.lower())[0]
    return get_user_model().objects.create_user(username=username, password=password, group=group)


class PostDetailViewTest(TestCase):
    """Test post detail page"""

    def setUp(self):
        """Create two users. First will be logged in and second will not"""

        self.first_user = get_test_user('firstuser', '12345678', 'ABC')
        self.second_user = get_test_user('seconduser', '12345678', 'BCA')

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


class StudyGroupPostsViewTest(TestCase):
    """Test study group posts page"""

    def setUp(self):
        """Create test user"""
        self.test_user = get_test_user(username='testuser', password='12345678', group_title='ABC')

    def test_study_group_posts_status_code(self):
        """Test study group posts status code is 200"""
        post = Post.objects.create(
            author=self.test_user,
            only_for_group=True,
            title='SimpleTitle',
            description='SimpleDescription',
        )
        self.client.login(username='testuser', password='12345678')

        response = self.client.get('/posts/group/')
        self.assertEqual(response.status_code, 200)

    def test_study_group_posts_status_code_reverse_lazy(self):
        """Test post detail page status code using reverse_lazy() is 200"""
        post = Post.objects.create(
            author=self.test_user,
            only_for_group=False,
            title='SimpleTitle',
            description='SimpleDescription',
        )
        self.client.login(username='testuser', password='12345678')

        response = self.client.get(reverse_lazy('study_group_posts'))
        self.assertEqual(response.status_code, 200)

    def test_study_group_posts_status_code_with_and_without_login(self):
        """Test study group posts status code is 200 when logged in and isn't 200 when not"""
        post = Post.objects.create(
            author=self.test_user,
            only_for_group=True,
            title='SimpleTitle',
            description='SimpleDescription',
        )

        response = self.client.get(reverse_lazy('study_group_posts'))
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='testuser', password='12345678')

        response = self.client.get(reverse_lazy('study_group_posts'))
        self.assertEqual(response.status_code, 200)
