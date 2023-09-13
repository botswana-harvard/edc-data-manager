import datetime
import uuid
from unittest.mock import MagicMock, patch

import xlwt
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core import mail
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import TestCase
from model_mommy import mommy

from .modeladmin_mixin import ExportActionMixin
from .models import DataActionItem


class TestDataActionItem(TestCase):

    def setUp(self):
        self.assigned_user = User.objects.create_user(
            username='testuser', password='12345')
        self.user_created = User.objects.create_user(
            username='testuser2', password='12345')
        self.options = {
            'subject_identifier': '123124',
            'comment': 'This participant need to take PBMC for storage',
            'assigned': self.assigned_user.username,
            'user_created': self.user_created.username}

        self.normal_user = User.objects.create(username="harry")
        self.firstname_user = User.objects.create(username="rill", first_name="bill")
        self.fullname_user = User.objects.create(username="ell", first_name="dass",
                                                 last_name="oienjd")

    def create_user_in_assignable_group(self, username):
        user = User.objects.create_user(username=username)
        group_name = 'assignable users'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

    def test_assign_users_requires_first_and_last_name(self):
        self.create_user_in_assignable_group("user_blank")
        instance = DataActionItem()
        with self.assertRaises(ValidationError) as error:
            instance.assign_users
        self.assertEqual(
            error.exception.message,
            'The user user_blank needs to set their first name.'
        )

    def test_assign_users_includes_valid_users(self):
        user = User.objects.create(
            username="adsaww",
            first_name="djsd",
            last_name="dsuhd",
        )
        group_name = 'assignable users'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        instance = DataActionItem()
        self.assertIn(("adsaww", "djsd dsuhd"), instance.assign_users)

    def test_data_action_item(self):
        """Test creation of a data action item.
        """
        DataActionItem.objects.create(
            **self.options)
        data_action_item = DataActionItem.objects.all()
        self.assertEqual(data_action_item.count(), 1)

    def test_action_item_sequnce_numbering(self):
        """Test creation of a data action item issue number increments sequentially.
        """
        count = 1
        while count < 4:
            data_action_item = DataActionItem.objects.create(
                **self.options)
            self.assertEqual(data_action_item.issue_number, count)
            count += 1

    def test_user_assigning(self):
        """Test that an issue can not be created if the user
        assigning does not exists as a django user.
        """
        options = {
            'subject_identifier': '123124',
            'comment': 'This participant need to take PBMC for storage',
            'assigned': 'testuser3',
            'issue_number': 1}
        with self.assertRaises(ValidationError) as error:
            DataActionItem.objects.create(**options)
        self.assertEqual(
            error.exception.message,
            f"The user {options.get('assigned')} that you have assigned the "
            f"data issue {options.get('issue_number')} does not exist.")


class EmailUsersTest(TestCase):

    def setUp(self):
        self.normal_user = User.objects.create(username="user_normal",
                                               email='normal@example.com')
        self.another_user = User.objects.create(username="user_another",
                                                email='another@example.com')
        self.instance = DataActionItem()  # You'll have to adapt this instantiation to
        # your own model
        self.instance.assigned = self.normal_user.username
        self.instance.user_created = self.another_user.username

    def test_no_such_users(self):
        self.instance.assigned = "nonexistent"
        with self.assertRaises(ValidationError) as error:
            self.instance.email_users(instance=self.instance, subject="Test",
                                      message="Test message")
        self.assertEqual(str(error.exception),
                         "['The user nonexistent that you have assigned the data issue "
                         "0 does not exist.']")

    def test_send_email(self):
        self.instance.email_users(instance=self.instance, subject="Test",
                                  message="Test message")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test')
        self.assertEqual(mail.outbox[0].body, 'Test message')
        self.assertEqual(mail.outbox[0].from_email,
                         settings.EMAIL_HOST_USER)  # Replace with your default sender
        self.assertEqual(mail.outbox[0].to,
                         [self.normal_user.email, self.another_user.email])


class TestExportActionMixin(TestCase):
    @patch('django.http.HttpResponse', spec=HttpResponse)
    @patch('xlwt.Workbook', spec=xlwt.Workbook)
    def test_export_as_csv(self, mock_workbook, mock_response):
        # Create instance of mixin and add dummy request
        mixin = ExportActionMixin()
        mixin.model = DataActionItem
        request = MagicMock()

        User.objects.create(username='testuser', email='testuser@test.com')
        User.objects.create(username='testuser1', email='testuser1@test.com')

        # Create and setup queryset
        item1 = mommy.prepare('DataActionItem', id=uuid.uuid4(),
                              subject='Test subject', assigned='testuser',
                              comment='Test comment')
        item2 = mommy.prepare('DataActionItem', id=uuid.uuid4(),
                              subject='Test subject 1', assigned='testuser1',
                              comment='Test comment')
        queryset = [item1, item2]

        # Call the method
        mixin.export_as_csv(request, queryset)

        # Assertions
        self.assertTrue(mock_workbook.called)
