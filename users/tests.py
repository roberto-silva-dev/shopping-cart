from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        """Tests the creation of a common user"""
        user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
            user_type="common"
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.user_type, "common")
        self.assertTrue(user.check_password("testpassword123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_vip_user(self):
        """Tests the creation of a VIP user"""
        user = get_user_model().objects.create_user(
            username="vipuser",
            password="vip123password",
            user_type="vip"
        )

        self.assertEqual(user.username, "vipuser")
        self.assertEqual(user.user_type, "vip")
        self.assertTrue(user.check_password("vip123password"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Tests the creation of a superuser"""
        user = get_user_model().objects.create_superuser(
            username="superuser",
            password="superpassword123"
        )

        self.assertEqual(user.username, "superuser")
        self.assertTrue(user.check_password("superpassword123"))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_type_default(self):
        """Tests the default value of user_type"""
        user = get_user_model().objects.create_user(
            username="defaultuser",
            password="defaultpassword123"
        )

        self.assertEqual(user.user_type, "common")

    def test_user_type_choices(self):
        """Tests if the user_type field is limited to the defined options"""
        user_common = get_user_model().objects.create_user(
            username="usercommon",
            password="commonpassword123",
            user_type="common"
        )
        user_vip = get_user_model().objects.create_user(
            username="uservip",
            password="vippassword123",
            user_type="vip"
        )

        self.assertEqual(user_common.user_type, "common")
        self.assertEqual(user_vip.user_type, "vip")

        invalid_user = get_user_model()(
            username="invaliduser",
            password="invalidpassword123",
            user_type="invalid"  # Invalid option
        )
        with self.assertRaises(ValidationError):
            invalid_user.full_clean()
