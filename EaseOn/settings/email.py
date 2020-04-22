# -*- coding: utf-8 -*-
import environ

root = environ.Path(__file__) - 1  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()  # reading .env file

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#  env('DEBUG'):
#if not env('DEBUG', cast=bool):
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = not True
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env('EMAIL_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')
EMAIL_PORT = 465
EMAIL_TEMPLATES = {
    'alert': 'email_templates/alert.html',
    'action': 'email_templates/action.html',
}
