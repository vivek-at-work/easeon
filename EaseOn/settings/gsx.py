# -*- coding: utf-8 -*-
import environ

root = environ.Path(__file__) - 1  # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False))  # set default values and casting
environ.Env.read_env()  # reading .env file


GSX_SOLD_TO = env("GSX_SOLD_TO", default="GSX_SOLD_TO")
GSX_SHIP_TO = env("GSX_SHIP_TO", default="GSX_SHIP_TO")
GSX_ENV = env("GSX_ENV", default="PROD")
GSX_SETTINGS_PROD = (
    env("GSX_CERT_FILE_PATH_PROD", default="GSX_CERT_FILE_PATH_PROD"),
    env("GSX_KEY_FILE_PATH_PROD", default="GSX_KEY_FILE_PATH_PROD"),
    env("GSX_URL_PROD", default="GSX_URL_PROD"),
    GSX_SOLD_TO,
    GSX_SHIP_TO,
)
GSX_SETTINGS_UAT = (
    env("GSX_CERT_FILE_PATH_UAT", default="GSX_CERT_FILE_PATH_UAT"),
    env("GSX_KEY_FILE_PATH_UAT", default="GSX_KEY_FILE_PATH_UAT"),
    env("GSX_URL_UAT", default="GSX_URL_UAT"),
    GSX_SOLD_TO,
    GSX_SHIP_TO,
)

VALIDATE_GSX_AUTH_TOKEN_ON_SIGN_UP = env(
    "VALIDATE_GSX_AUTH_TOKEN_ON_SIGN_UP",default=1, cast=bool
)
