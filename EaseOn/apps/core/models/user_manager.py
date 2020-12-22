# -*- coding: utf-8 -*-
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    "User Manager Class used to create user from command line."

    def create_user(
        self,
        email,
        username,
        first_name,
        last_name,
        contact_number,
        is_admin,
        address,
        pin_code,
        city,
        gsx_technician_id,
        gsx_user_name,
        gsx_auth_token,
        password=None,
    ):
        """
        Creates and saves a User with the given arguments.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            address=address,
            pin_code=pin_code,
            is_admin=False,
            city=city,
            is_system_user=False,
            last_login=None,
            is_active=False,
            gsx_technician_id=gsx_technician_id,
            gsx_user_name=gsx_user_name,
            gsx_auth_token=gsx_auth_token,
            can_login_to_admin_site=False,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        username,
        first_name,
        last_name,
        contact_number,
        address,
        pin_code,
        city,
        gsx_technician_id,
        gsx_user_name,
        gsx_auth_token,
        password,
    ):
        """
        Creates and saves a superuser with the given arguments.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            address=address,
            pin_code=pin_code,
            is_admin=True,
            is_active=False,
            last_login=None,
            city=city,
            is_system_user=False,
            gsx_technician_id=gsx_technician_id,
            gsx_user_name=gsx_user_name,
            gsx_auth_token=gsx_auth_token,
            can_login_to_admin_site=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def all_superusers(self):
        return self.get_queryset().filter(user_type__in=[1, 5])

    def all_non_superusers(self):
        return self.get_queryset().exclude(user_type__in=[1, 5])

    def all_superusers_email(self):
        return self.all_superusers().values_list("email", flat=True)
