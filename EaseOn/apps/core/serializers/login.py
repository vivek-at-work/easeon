# -*- coding: utf-8 -*-
# import logging

# from django.contrib.auth import authenticate, get_user_model
# from rest_framework import exceptions, serializers

# logger = logging.getLogger('easeOn')


# class LoginSerializer(serializers.Serializer):
#     'Serializer for login.'
#     email = serializers.EmailField(required=True, allow_blank=False)
#     password = serializers.CharField(style={'input_type': 'password'})

#     def _authenticate_via_email(self, email, password):
#         user = None
#         if email and password:
#             user = authenticate(
#                 self.context.get('request'),
#                 **{'email': email, 'password': password}
#             )
#             if not user:
#                 raise Exception()
#         else:
#             msg = 'Must include "email" and "password".'
#             raise exceptions.ValidationError(msg)

#         return user

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#         try:
#             unauthenticated_user = get_user_model().objects.get(
#                 email__iexact=email
#             )
#             if not unauthenticated_user.is_active:
#                 msg = 'User account has been disabled.'
#                 raise exceptions.ValidationError(msg)
#             user = self._authenticate_via_email(email, password)
#             attrs['user'] = user
#             return attrs
#         except Exception as exception:
#             msg = 'Unable to login with provided credentials.'
#             logger.error(exception)
#             raise exceptions.ValidationError(msg)
