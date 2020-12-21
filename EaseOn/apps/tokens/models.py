# -*- coding: utf-8 -*-
from core.models import BaseModel
from core.utils import send_token_to_customer
from core.cache_mixin import ModelCacheMixin
from django.contrib.auth import get_user_model
from django.db import connection, models
from organizations.models import Organization
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache




class Token(BaseModel):
    """A Service Token"""
    CACHE_KEY = "token"
    CACHED_RELATED_OBJECT = ["organization"]

    organization = models.ForeignKey(
        Organization,
        related_name="tokens",
        editable=False,
        null=True,
        on_delete=models.DO_NOTHING,
    )
    location_code = models.CharField(max_length=100)
    token_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    invited_by = models.ForeignKey(
        get_user_model(),
        null=True,
        related_name="received_tokens",
        on_delete=models.DO_NOTHING,
    )
    counter_number = models.IntegerField(null=True)
    contact_number = models.CharField(blank=True, null=True, max_length=50)
    invite_sent_on = models.DateTimeField(null=True)
    is_present = models.BooleanField(default=False)

    def send_token_number_by_sms(self):
        send_token_to_customer(
            self.contact_number, str(self.token_number).rjust(4, "0")
        )

    def can_invite(self, user):
        return (self.invited_by is None) or (self.invited_by == user)

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))

# def clear_model_cache(sender, *args, **kwargs):
#     """
#     Clears cached data of models on update or delete.
#     :param sender: Model Class triggering this signal.
#     :param args: extra arguments
#     :param kwargs: extra keyword arguments
#     :return: None
#     """
#     if Token.CACHE_KEY in cache:
#         cache.delete(Token.CACHE_KEY)



# post_save.connect(clear_student_cache, sender=Student)
# post_delete.connect(clear_student_cache, sender=Student)