# -*- coding: utf-8 -*-
import environ

root = environ.Path(__file__) - 1  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()  # reading .env file

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB", default="DB"),
        "USER": env("DB_USER", default="DB_USER"),
        "PASSWORD": env("DB_USER_PASSWORD", default="DB_USER_PASSWORD"),
        "HOST": env("DB_HOST", default="DB_HOST"),
        "PORT": "",
    }
}
