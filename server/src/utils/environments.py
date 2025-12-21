from src.utils.paths import ENVIRONMENT_FILE_PATH


from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path=ENVIRONMENT_FILE_PATH)


ENVIRONMENT_MODE = getenv('ENVIRONMENT_MODE', None)

DATABASE_URL =\
    getenv('DEVELOPMENT_DATABASE_URL', None)\
    if ENVIRONMENT_MODE == 'DEVELOPMENT'\
    else getenv('PRODUCTION_DATABASE_URL', None)

API_HOST =\
    getenv('DEVELOPMENT_API_HOST', None)\
    if ENVIRONMENT_MODE == 'DEVELOPMENT'\
    else getenv('PRODUCTION_API_HOST', None)

API_PORT =\
    int(getenv('DEVELOPMENT_API_PORT', None))\
    if ENVIRONMENT_MODE == 'DEVELOPMENT'\
    else int(getenv('PRODUCTION_API_PORT', None))


SECRET_KEY = getenv('SECRET_KEY', None)
TIME_ALLOWED_MODIFICATION = getenv('TIME_ALLOWED_MODIFICATION', None)
TIME_ZONE = getenv('TIME_ZONE', None)

SMTP_SERVER = getenv("SMTP_SERVER", "smtp.office365.com")
SMTP_PORT = int(getenv("SMTP_PORT", "587"))
SMTP_SENDER = getenv("SMTP_SENDER", "soporteti@consejodeauditoria.gob.cl")
SMTP_PASSWORD = getenv("SMTP_PASSWORD")

