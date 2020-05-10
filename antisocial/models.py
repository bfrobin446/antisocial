import uuid

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from human_uuid import human_uuid


class User(AbstractBaseUser):
    """A model for users that aren't identified by usernames and don't log in
    with passwords."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    human_id = models.TextField(unique=True)
    USERNAME_FIELD = 'human_id'

    display_name = models.CharField(max_length=128)
    """
    Use this instead of Django's first_name and last_name, because not every
    name can be sensibly divided into first and last. Length is limited because
    this is untrusted text: third parties shouldn't be able to use unreasonable
    amounts of disk space or make the UI look stupid.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.human_id == '':
            self.human_id = human_uuid.encode(
                self.id, settings.HUMAN_ID_LENGTH
            )

    def __str__(self):
        return f'{self.human_id} ({self.display_name})'


class LinkedAccount(models.Model):
    """
    A user logs in by proving control of an outside account. Because we plan to
    support several different types of accounts that have different
    authentication flows, we have an abstract class to handle any members that
    should be common to all supported types.
    """
    class Meta:
        abstract = True

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # We allow the user link to be nullable because during account creation, we
    # may need to save the LinkedAccount before we populate the user.


class LinkedEmailAccount(LinkedAccount):
    """
    An email address that can be authenticated by mailing a link that contains
    a unique token.
    """
    email = models.EmailField(unique=True)


class EmailToken(models.Model):
    """
    A token that was sent to an email address to authenticate it.
    """
    account = models.ForeignKey(LinkedEmailAccount, on_delete=models.CASCADE)
    token = models.CharField(max_length=40)
