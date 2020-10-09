from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from .views import HomePageView


# Create your tests here.
class HomepageTests(TestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass',
        )

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html_while_logged_out(self):
        self.assertContains(self.response, 'Create a new split. Log in or sign up to save your splits.')
        self.assertContains(self.response, 'Sign up')

    def test_homepage_contains_correct_html_while_logged_in(self):
        self.client.login(email='testuser@email.com', password='testpass')
        self.assertContains(self.response, 'Create a new split.')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Should not contain this')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__, HomePageView.as_view().__name__
        )
