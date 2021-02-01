# -*- coding: utf-8 -*-
import environ

root = environ.Path(__file__) - 1  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()  # reading .env file

ENABLE_DISTANCE_CHECK_FOR_TOKEN = int(env("ENABLE_DISTANCE_CHECK_FOR_TOKEN", default=0))
MAX_TOKEN_RADIUS = int(env("MAX_TOKEN_RADIUS", default=500))