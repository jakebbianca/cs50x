from django.test import Client, TestCase
from .models import User, Post

#test cases
class PostTestCase(TestCase):

    def setUp(self):

        #create users
        #user who posts acceptable content
        u0 = User.objects.create(username="u0", password="u0")
        #user who posts unacceptable content
        u1 = User.objects.create(username="u1", password="u1")

        #create posts
        #short but within character range
        p0 = Post.objects.create(poster=u0, content="Hello!")
        #exactly 280 characters
        p1 = Post.objects.create(poster=u0, content="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat mas")
        #exactly 0 characters
        p2 = Post.objects.create(poster=u1, content="")
        #exactly 281 characters
        p3 = Post.objects.create(poster=u1, content="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat mas!")
        #exactly 560 characters characters
        p4 = p1 = Post.objects.create(poster=u1, content="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat masLorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat mas")

    
    # Post content tests
    def test_character_count(self):
        """Test that character count is correct"""
        p = Post.objects.get(content="Hello!")
        self.assertEqual(len(p.content), 6)

    def test_valid_post(self):
        """Test that a post with valid content length passes validation"""
        p = Post.objects.get(content="Hello!")
        self.assertTrue(p.is_valid_post())

    def test_valid_post_280(self):
        """Test that a post with exactly 280 characters (the maximum) passes validation"""
        p = Post.objects.get(content="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat mas")
        self.assertTrue(p.is_valid_post())

    def test_invalid_post_0(self):
        """Test that a post with exactly 0 characters fails validation (minimum is 1)"""
        p = Post.objects.get(content="")
        self.assertFalse(p.is_valid_post())

    def test_invalid_post_281(self):
        """Test that a post with exactly 281 characters, 1 above minimum, fails validation"""
        p = Post.objects.get(content="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat mas!")
        self.assertFalse(p.is_valid_post())

    def test_invalid_post(self):
        """Test that a post with far greater than 280 character maximum fails validation"""
        p = Post.objects.get(content="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat masLorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat mas")
        self.assertFalse(p.is_valid_post())

    # client tests
    def test_index(self):
        """Test that index page loads correctly"""
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)