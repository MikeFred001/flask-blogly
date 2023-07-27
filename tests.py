import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import User, Post, DEFAULT_IMAGE_URL

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()
        Post.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        test_post = Post(
            title="test_title",
            content="test_content",
            user_id = test_user.id
        )

        db.session.add(test_user)
        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Tests that html and status code for user list is correct"""

        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)


    def test_add_user_redirect(self):
        """Tests that add_user() redirects properly to the right route, has the
        correct status code, and contains the expected html"""

        with self.client as c:
            resp = c.post("/users/new",
                        data={
                        "first_name": "Mike",
                        "last_name": "Fred",
                        "image_url": "test"
                        },
                        follow_redirects=True
                    )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Delete</button>", html)
            self.assertIn("Mike", html)
            self.assertIn("For testing user_info", html)


    def test_show_user(self):
        """Tests that html and status code for show_user is correct"""

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Edit</a>", html)
            self.assertIn("For testing user_info", html)
            self.assertIn("test1_first", html)


    def test_display_edit_form(self):
        """Tests that html and status code for display_edit_form is correct"""

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Save</button>", html)
            self.assertIn("Test for Edit Page", html)
            self.assertIn("test1_first", html)


    def test_add_post_form(self):
        """Tests that html and status code for test_add_post_form is correct.
        Also tests that out-of-range ids return 404"""

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/posts/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Test for add post form", html)
            self.assertIn("Post Content</label>", html)
            self.assertIn("test1_first", html)

            resp2 = c.get(f"/users/99999999/posts/new")
            self.assertEqual(resp2.status_code, 404)


    def test_handle_add_post_form(self):
        """Tests that redirect occurs properly and directs to the proper route"""

        with self.client as c:
            resp = c.post(f"/users/{self.user_id}/posts/new",
                        data={
                        "post_title": "test title",
                        "post_content": "test content"
                        },
                        follow_redirects=True
                    )
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Posts</h3>", html)
            self.assertIn("For testing user_info", html)
            self.assertIn("test title", html)

    # Test failure conditions to make sure 404 works
