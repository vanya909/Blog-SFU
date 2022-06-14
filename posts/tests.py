"""Posts views tests"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from users.models import StudyGroup, Follow
from .models import Post, Comment


def get_test_user(username, password, group_title):
    """Function which returns a new user for tests"""
    group = StudyGroup.objects.get_or_create(title=group_title, slug=group_title.lower())[0]
    return get_user_model().objects.create_user(username=username, password=password, group=group)


class PostDetailViewTest(TestCase):
    """Test post detail page"""
    def setUp(self):
        """Create two users. First will be logged in and second will not"""
        self.test_user = get_test_user('testuser', '12345678', 'ABC')
        self.first_user = get_test_user('firstuser', '12345678', 'ABC')
        self.second_user = get_test_user('seconduser', '12345678', 'BCA')

        self.client.login(username='testuser', password='12345678')

    def test_post_detail_status_code(self):
        """Test page status code is 200"""
        post = Post.objects.create(
            author=self.first_user,
            only_for_group=False,
            description='SimpleDescription',
        )

        response = self.client.get(f'/posts/{post.pk}/')
        self.assertEqual(response.status_code, 200, "Detail page status code isn't 200")

    def test_post_detail_status_code_reverse_lazy(self):
        """Test page status code using reverse_lazy() is 200"""
        post = Post.objects.create(
            author=self.first_user,
            only_for_group=False,
            description='SimpleDescription',
        )

        response = self.client.get(reverse_lazy('post_detail', kwargs={'post_pk': post.pk}))
        self.assertEqual(
            response.status_code, 200,
            msg="Detail page status code using reverse_lazy() isn't 200"
        )

    def test_own_group_post_detail_status_code(self):
        """Test own group post detail page status code is 200"""
        own_group_post = Post.objects.create(
            author=self.first_user,
            only_for_group=True,
            description='SimpleDescription',
        )

        response = self.client.get(
            reverse_lazy('post_detail', kwargs={'post_pk': own_group_post.pk})
        )
        self.assertEqual(
            response.status_code, 200,
            msg="Own group post's detail page status code isn't 200"
        )

    def test_another_group_post_detail_status_code(self):
        """Test another group post detail page status code is not 200"""
        another_group_post = Post.objects.create(
            author=self.second_user,
            only_for_group=True,
            description='SimpleDescription',
        )

        response = self.client.get(
            reverse_lazy('post_detail', kwargs={'post_pk': another_group_post.pk})
        )
        self.assertNotEqual(
            response.status_code, 200,
            msg="Another group post's detail page status code is 200"
        )


class StudyGroupPostsViewTest(TestCase):
    """Test study group posts page"""
    def setUp(self):
        """Create test user"""
        self.test_user = get_test_user(username='testuser', password='12345678', group_title='ABC')
        self.client.login(username='testuser', password='12345678')

    def test_study_group_posts_status_code(self):
        """Test page status code is 200"""
        response = self.client.get('/posts/group/')
        self.assertEqual(
            response.status_code, 200,
            msg="Study group posts page status code isn't 200"
        )

    def test_study_group_posts_status_code_reverse_lazy(self):
        """Test page status code using reverse_lazy() is 200"""
        response = self.client.get(reverse_lazy('study_group_posts'))
        self.assertEqual(
            response.status_code, 200,
            msg="Study group posts page status code using reverse_lazy() isn't 200"
        )

    def test_study_group_posts_status_code_with_and_without_login(self):
        """Test page status code is 200 when logged in and isn't 200 when not"""
        response = self.client.get(reverse_lazy('study_group_posts'))
        self.assertEqual(
            response.status_code, 200,
            msg="Study group posts page status code isn't 200 when logged in"
        )

        self.client.logout()

        response = self.client.get(reverse_lazy('study_group_posts'))
        self.assertNotEqual(
            response.status_code, 200,
            msg="Study group posts page status code is 200 when logged out"
        )

    def test_content_on_study_group_posts_page(self):
        """Test group post is on the page and public post is not"""
        group_post = Post.objects.create(
            author=self.test_user,
            only_for_group=True,
            description='Description'
        )
        public_post = Post.objects.create(
            author=self.test_user,
            only_for_group=False,
            description='Description'
        )

        response = self.client.get(reverse_lazy('study_group_posts'))
        self.assertIn(
            group_post, response.context['posts'],
            msg="Group post isn't in the study group page's context"
        )
        self.assertNotIn(
            public_post, response.context['posts'],
            msg="Public post is in the study group page's context"
        )


class SubscriptionsPostsViewTest(TestCase):
    """Test subscriptions page"""
    def setUp(self):
        """Create test users and subscription"""
        self.main_user = get_test_user(
            username='mainuser',
            password='12345678',
            group_title='ABC'
        )
        self.first_user = get_test_user(
            username='firstuser',
            password='12345678',
            group_title='ABC'
        )
        self.second_user = get_test_user(
            username='seconduser',
            password='12345678',
            group_title='ABC'
        )

        Follow.objects.create(user=self.main_user, author=self.first_user)

        self.client.login(username='mainuser', password='12345678')

    def test_subscriptions_status_code(self):
        """Test page status code is 200"""
        response = self.client.get('/posts/subscriptions/')
        self.assertEqual(
            response.status_code, 200,
            msg="Subscriptions page status code isn't 200"
        )

    def test_subscriptions_status_code_reverse_lazy(self):
        """Test page status code using reverse_lazy() is 200"""
        response = self.client.get(reverse_lazy('subscriptions_posts'))
        self.assertEqual(
            response.status_code, 200,
            msg="Subscriptions page status code using reverse_lazy() isn't 200"
        )

    def test_subscriptions_status_code_with_and_without_login(self):
        """Test page status code is 200 when logged in and isn't 200 when not"""
        response = self.client.get(reverse_lazy('subscriptions_posts'))
        self.assertEqual(
            response.status_code, 200,
            msg="Subscriptions page status code isn't 200 when logged in"
        )

        self.client.logout()

        response = self.client.get(reverse_lazy('subscriptions_posts'))
        self.assertNotEqual(
            response.status_code, 200,
            msg="Subscriptions page status code is 200 when logged out"
        )

    def test_content_on_subscriptions_page(self):
        """Test author's post is on the page but not author's and group posts are not"""
        sub_post = Post.objects.create(
            author=self.first_user,
            only_for_group=False,
            description='Description'
        )
        not_sub_post = Post.objects.create(
            author=self.second_user,
            only_for_group=False,
            description='Description2'
        )
        group_post = Post.objects.create(
            author=self.first_user,
            only_for_group=True,
            description='Description3'
        )

        response = self.client.get(reverse_lazy('subscriptions_posts'))

        self.assertIn(
            sub_post, response.context['posts'],
            msg="Author's post isn't in the subscriptions page's context"
        )
        self.assertNotIn(
            group_post, response.context['posts'],
            msg="Group post is in the subscriptions page's context"
        )
        self.assertNotIn(
            not_sub_post,
            response.context['posts'],
            "Not author's post is in the subscriptions page's context"
        )


class PostCreateViewTest(TestCase):
    """Test post creation page"""
    def setUp(self):
        """Create test user"""
        self.user = get_test_user('testuser', '12345678', 'ABC')
        self.client.login(username='testuser', password='12345678')

    def test_post_create_status_code(self):
        """Test page status code is 200"""
        response = self.client.get('/posts/create/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_status_code_reverse_lazy(self):
        """Test page status code using reverse_lazy() is 200"""
        response = self.client.get(reverse_lazy('create_post'))
        self.assertEqual(response.status_code, 200)

    def test_post_create_status_code_with_and_without_login(self):
        """Test page status code is 200 when logged in and isn't 200 when not"""
        response = self.client.get(reverse_lazy('create_post'))
        self.assertEqual(
            response.status_code, 200,
            msg="Post creation page status code isn't 200 when logged in"
        )

        self.client.logout()

        response = self.client.get(reverse_lazy('create_post'))
        self.assertNotEqual(
            response.status_code, 200,
            msg="Post creation page status code is 200 when logged out"
        )

    def test_post_creation(self):
        """Test post creation"""
        data = {'description': 'Post1', 'only_for_group': False}
        response = self.client.post(reverse_lazy('create_post'), data)

        self.assertEqual(
            response.status_code, 302,
            msg="Don't redirect after post creation"
        )
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                only_for_group=data['only_for_group'],
                description=data['description'],
                pk=1
            ).exists(),
            msg="Created post doesn't exists"
        )


class PostEditViewTest(TestCase):
    """Test post edit page"""
    def setUp(self):
        """Create two test users and test post"""
        self.first_user = get_test_user('firstuser', '12345678', 'ABC')
        self.second_user = get_test_user('seconduser', '12345678', 'ABC')

        self.client.login(username='firstuser', password='12345678')
        self.client.post(
            reverse_lazy('create_post'),
            {'description': 'abc', 'only_for_group': False}
        )

    def test_post_edit_status_code(self):
        """Test page status code is 200"""
        response = self.client.get('/posts/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit_status_code_reverse_lazy(self):
        """Test page status code using reverse_lazy() is 200"""
        response = self.client.get(reverse_lazy('post_edit', kwargs={'post_pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_post_edit_access(self):
        """Test access to the page of the not author of the post"""
        self.client.logout()
        response = self.client.get(reverse_lazy('post_edit', kwargs={'post_pk': 1}))
        self.assertNotEqual(
            response.status_code, 200,
            msg="Anonymous user have access to edit posts"
        )

        self.client.login(username='seconduser', password='12345678')
        response = self.client.get(reverse_lazy('post_edit', kwargs={'post_pk': 1}))
        self.assertNotEqual(
            response.status_code, 200,
            msg="User have access to edit someone else's post"
        )

    def test_post_edit(self):
        """Test post edit"""
        self.assertTrue(
            Post.objects.filter(description='abc', author=self.first_user, pk=1).exists()
        )
        self.assertFalse(
            Post.objects.filter(description='def', author=self.first_user, pk=1).exists()
        )

        data = {'description': 'def', 'only_for_group': False}
        self.client.post(reverse_lazy('post_edit', kwargs={'post_pk': 1}), data)

        self.assertFalse(
            Post.objects.filter(description='abc', author=self.first_user, pk=1).exists()
        )
        self.assertTrue(
            Post.objects.filter(description='def', author=self.first_user, pk=1).exists()
        )


class PostDeleteViewTest(TestCase):
    """Test post delete page"""
    def setUp(self):
        """Create two test users and test post"""
        self.first_user = get_test_user('firstuser', '12345678', 'ABC')
        self.second_user = get_test_user('seconduser', '12345678', 'ABC')

        self.client.login(username='firstuser', password='12345678')
        self.client.post(
            reverse_lazy('create_post'),
            {'description': 'abc', 'only_for_group': False}
        )

    def test_post_delete_status_code(self):
        """Test page status code is 200"""
        response = self.client.get('/posts/1/delete/')
        self.assertEqual(response.status_code, 200)

    def test_post_delete_status_code_reverse_lazy(self):
        """Test page status code using reverse_lazy() is 200"""
        response = self.client.get(reverse_lazy('post_delete', kwargs={'post_pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_post_delete_access(self):
        """Test access to the page of the not author of the post"""
        self.client.logout()
        response = self.client.get(reverse_lazy('post_delete', kwargs={'post_pk': 1}))
        self.assertNotEqual(
            response.status_code, 200,
            msg="Anonymous user have access to delete posts"
        )

        self.client.login(username='seconduser', password='12345678')
        response = self.client.get(reverse_lazy('post_delete', kwargs={'post_pk': 1}))
        self.assertNotEqual(
            response.status_code, 200,
            msg="User have access to delete someone else's post"
        )

    def test_post_delete(self):
        """Test post deletion"""
        self.assertTrue(
            Post.objects.filter(description='abc', author=self.first_user, pk=1).exists()
        )

        self.client.post(reverse_lazy('post_delete', kwargs={'post_pk': 1}))

        self.assertFalse(
            Post.objects.filter(description='abc', author=self.first_user, pk=1).exists()
        )


class CommentCreateViewTest(TestCase):
    """Test comment creation page"""
    def setUp(self):
        """Create test user"""
        self.user = get_test_user('testuser', '12345678', 'ABC')
        self.client.login(username='testuser', password='12345678')

        data = {'description': 'abc', 'only_for_group': False}
        self.client.post(reverse_lazy('create_post'), data)

    def test_comment_create_status_code(self):
        """Test page status code is 200"""
        response = self.client.get('/posts/1/comment/')
        self.assertEqual(response.status_code, 200)

    def test_comment_create_status_code_reverse_lazy(self):
        """Test page status code using reverse_lazy() is 200"""
        response = self.client.get(reverse_lazy('comment_create', kwargs={'post_pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_comment_create_status_code_with_and_without_login(self):
        """Test page status code is 200 when logged in and isn't 200 when not"""
        response = self.client.get(reverse_lazy('comment_create', kwargs={'post_pk': 1}))
        self.assertEqual(
            response.status_code, 200,
            msg="Comment creation page status code isn't 200 when logged in"
        )

        self.client.logout()

        response = self.client.get(reverse_lazy('comment_create', kwargs={'post_pk': 1}))
        self.assertNotEqual(
            response.status_code, 200,
            msg="Comment creation page status code is 200 when logged out"
        )

    def test_comment_creation(self):
        """Test comment creation"""
        data = {'text': 'Comment'}
        response = self.client.post(reverse_lazy('comment_create', kwargs={'post_pk': 1}), data)

        self.assertEqual(
            response.status_code, 302,
            msg="Don't redirect after comment creation"
        )
        self.assertTrue(
            Comment.objects.filter(
                author=self.user,
                post__pk=1,
                text='Comment'
            ).exists(),
            msg="Created comment doesn't exists"
        )


class CommentEditViewTest(TestCase):
    """Test comment editing page"""
    def setUp(self):
        """Create test user, post and comment"""
        self.comment_author = get_test_user('testuser', '12345678', 'ABC')
        self.second_user = get_test_user('seconduser', '12345678', 'ABC')
        self.client.login(username='testuser', password='12345678')

        self.post = Post.objects.create(
            author=self.second_user,
            description='Test post',
            only_for_group=False
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.comment_author,
            text='Before Editing'
        )

    def test_comment_edit_status_code(self):
        """Test page status code is 200"""
        response = self.client.get('/posts/1/comment/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_comment_edit_status_code_reverse_lazy(self):
        """Test page status code using reverse_lazy() is 200"""
        response = self.client.get(
            reverse_lazy('comment_edit', kwargs={'post_pk': 1, 'comment_pk': 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_comment_edit_status_code_with_and_without_login(self):
        """Test page status code isn't 200 when user is anonymous or not the author"""
        self.client.logout()

        response = self.client.get(
            reverse_lazy('comment_edit', kwargs={'post_pk': 1, 'comment_pk': 1})
        )
        self.assertNotEqual(
            response.status_code, 200,
            msg="Comment editing page status code is 200 when logged out"
        )

        self.client.login(username='seconduser', password='12345678')

        response = self.client.get(
            reverse_lazy('comment_edit', kwargs={'post_pk': 1, 'comment_pk': 1})
        )
        self.assertNotEqual(
            response.status_code, 200,
            msg="Comment editing page status code is 200 when another user is logged in"
        )

    def test_comment_editing(self):
        """Test comment editing"""
        self.assertTrue(
            Comment.objects.filter(
                author=self.comment_author,
                pk=1,
                post__pk=1,
                text='Before Editing'
            ).exists(),
            msg="Comment doesn't exists"
        )

        response = self.client.post(
            reverse_lazy('comment_edit', kwargs={'post_pk': 1, 'comment_pk': 1}),
            {'text': 'After Editing'}
        )

        self.assertEqual(
            response.status_code, 302,
            msg="Don't redirect after comment editing"
        )
        self.assertTrue(
            Comment.objects.filter(
                author=self.comment_author,
                pk=1,
                post__pk=1,
                text='After Editing'
            ).exists(),
            msg="Comment wasn't edited"
        )
        self.assertFalse(
            Comment.objects.filter(
                author=self.comment_author,
                pk=1,
                post__pk=1,
                text='Before Editing'
            ).exists(),
            msg="Comment wasn't edited"
        )
