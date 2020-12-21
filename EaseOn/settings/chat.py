# -*- coding: utf-8 -*-
import environ

root = environ.Path(__file__) - 1  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()  # reading .env file
CHAT_SERVICE_URL = env("CHAT_SERVICE_URL", default="")
CHAT_SERVICE_ADMIN = env("CHAT_SERVICE_ADMIN", default="")
CHAT_SERVICE_ADMIN_PASSWORD = env("CHAT_SERVICE_ADMIN_PASSWORD", default="")
ENABLE_CHAT = env("ENABLE_CHAT", default=0, cast=bool)
