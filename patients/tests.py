from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

# -- See unit testing section in README before running --


# Create your tests here.
class CreatePatientTest(TestCase):
    def test_init(self):
        User.objects.create_user(userID="John1", email="john@smartcare.com", password="pw1", role="admin", name="John Doe")
        user = User.objects.get(userID="John1")
        # self.assertEqual(user.get_email_field_name, "john@smartcare.com")
        self.assertEqual(user.role, "admin")

    # def test_get_user_attributes(self):
        