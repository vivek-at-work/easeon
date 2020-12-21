# -*- coding: utf-8 -*-
import environ

root = environ.Path(__file__) - 1  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()  # reading .env file

# GSX_URL = env('GSX_URL')
GSX_SOLD_TO = env("GSX_SOLD_TO")
GSX_SHIP_TO = env("GSX_SHIP_TO")
GSX_ENV = env("GSX_ENV")
GSX_SETTINGS_PROD = (
    env("GSX_CERT_FILE_PATH_PROD"),
    env("GSX_KEY_FILE_PATH_PROD"),
    env("GSX_URL_PROD"),
    GSX_SOLD_TO,
    GSX_SHIP_TO,
)
GSX_SETTINGS_UAT = (
    env("GSX_CERT_FILE_PATH_UAT"),
    env("GSX_KEY_FILE_PATH_UAT"),
    env("GSX_URL_UAT"),
    GSX_SOLD_TO,
    GSX_SHIP_TO,
)
GSX_URL = env("GSX_URL_" + GSX_ENV)


GSX_DUMMY_RESPONSE = env("GSX_DUMMY_RESPONSE", cast=bool)
VALIDATE_GSX_AUTH_TOKEN_ON_SIGN_UP = env(
    "VALIDATE_GSX_AUTH_TOKEN_ON_SIGN_UP", cast=bool
)
