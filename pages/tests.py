from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from posts.models import Post
from users.models import StudyGroup


def get_test_user(username, password, group_title):
    """Function which returns a new user for tests"""
    group = StudyGroup.objects.get_or_create(title=group_title, slug=group_title.lower())[0]
    return get_user_model().objects.create_user(username=username, password=password, group=group)


class IndexPageTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='A', email='a@a.com', password='123')

    def test_status_code(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_reverse_lazy_status_code(self):
        response = self.client.get(reverse_lazy('index'))
        self.assertEqual(response.status_code, 200)

    def test_page_title(self):
        response = self.client.get(reverse_lazy('index'))
        self.assertEqual(response.context['page_title'], 'Домашняя страница', "Index page has wrong title")

    def test_template_use(self):
        response = self.client.get(reverse_lazy('index'))
        self.assertTemplateUsed(response, 'pages/index.html')


class IndexPageSearchTestCase(TestCase):
    """Test search on index page"""
    def setUp(self):
        """Creating test user and posts"""
        self.test_user = get_test_user('testuser', '12345678', 'ABC')

        self.first_post = Post.objects.create(
            author=self.test_user,
            only_for_group=False,
            description='First Post',
        )

        self.second_post = Post.objects.create(
            author=self.test_user,
            only_for_group=False,
            description='Second Post',
        )

        self.first_post_only_for_group = Post.objects.create(
            author=self.test_user,
            only_for_group=True,
            description='First Post',
        )

    def test_page_title(self):
        """Test search page title"""
        response = self.client.get(f"{reverse_lazy('index')}?search=search")
        self.assertEqual(response.context['page_title'], 'Поиск', "Search page has wrong title")

    def test_search(self):
        """Test search returns only public posts that match the request"""
        response = self.client.get(f"{reverse_lazy('index')}?search=first")

        self.assertIn(self.first_post, response.context['posts'],
                      msg="Proper post isn't in the context")

        self.assertNotIn(self.second_post, response.context['posts'],
                         msg="Post that doesn't match the request is in the context")

        self.assertNotIn(self.first_post_only_for_group, response.context['posts'],
                         msg="Not public post is in the context")
