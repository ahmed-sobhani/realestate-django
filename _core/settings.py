import os
from pathlib import Path
from environs import Env
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


def join(path):
    return os.path.join(BASE_DIR, path)


env = Env()
env.read_env(recurse=False, path=join('.env'))

SECRET_KEY = env("SECRET_KEY", "=)lpcfnj$#7$e1==+!9la_0yq8)w79!k_&t^-76i*_+83z2ymy")
DEBUG = env.bool("DEBUG", True)
ALLOWED_HOSTS = env("ALLOWED_HOSTS", ['*'])
DRF_ENABLED = env("DRF_ENABLED", True)
CURRENT_SITE_DOMAIN = env("CURRENT_SITE_DOMAIN", "http://127.0.0.1:8000")
ONFIDO_TOKEN = env("ONFIDO_TOKEN", "api_sandbox.-aSIZTux3Cx.95wKRuItkxmmrbHoiGDdtKPLiR9cPkXs")

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # third-party
    'drf_yasg',
    'rest_framework',
    'django_rest_passwordreset',
    'django_filters',
    'corsheaders',
    'six',

    # real-estate
    'account.apps.AccountConfig',
    'investment.apps.InvestmentConfig',
    'opportunity.apps.OpportunityConfig',
    'kyc.apps.KycConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '_core.wsgi.application'


# Database
with env.prefixed('DB_') as e:
    DATABASES = {
        'default': dict(
            ENGINE='django.contrib.gis.db.backends.postgis',
            NAME=e('NAME', 'realEstate'),
            USER=e('USER', 'postgres'),
            PASSWORD=e('PASS', '000'),
            HOST=e('HOST', 'localhost'),
            PORT=e('PORT', '5432')
        )
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = join('static')
MEDIA_URL = '/media/'
MEDIA_ROOT = join("media")

AUTH_USER_MODEL = 'account.CustomUser'

with env.prefixed('CORS_ORIGIN_') as e:
    CORS_ORIGIN_ALLOW_ALL = e.bool('ALLOW_CREDENTIALS', True)
    CORS_ORIGIN_WHITELIST = e.list('WHITELIST', ['localhost'])

ACCESS_TOKEN_LIFETIME = env.int('ACCESS_TOKEN_LIFETIME_DAYS', 1)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=ACCESS_TOKEN_LIFETIME),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=ACCESS_TOKEN_LIFETIME),
    'ROTATE_REFRESH_TOKENS': True,
}

_DEFAULT_TIME_RELATED_FORMAT = "%Y-%m-%d"

REST_FRAMEWORK = dict(
    # DEFAULT_PERMISSION_CLASSES=('rest_framework.permissions.IsAuthenticated',),
    DEFAULT_AUTHENTICATION_CLASSES=('rest_framework_simplejwt.authentication.JWTAuthentication',),
    UNAUTHENTICATED_USER=None,
    DEFAULT_RENDERER_CLASSES=('rest_framework.renderers.JSONRenderer',),
    DEFAULT_PAGINATION_CLASS='utils.paginations.DefaultPagination',
    DATE_FORMAT=_DEFAULT_TIME_RELATED_FORMAT,
    DATE_INPUT_FORMATS=[_DEFAULT_TIME_RELATED_FORMAT],
    DATETIME_FORMAT=_DEFAULT_TIME_RELATED_FORMAT,
    DATETIME_INPUT_FORMATS=[_DEFAULT_TIME_RELATED_FORMAT],
    # TIME_FORMAT=_DEFAULT_TIME_RELATED_FORMAT,
    # TIME_INPUT_FORMATS=[_DEFAULT_TIME_RELATED_FORMAT]
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # During development only
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# MAILER_EMAIL_BACKEND = EMAIL_BACKEND
# EMAIL_HOST = 'your_mail_server'
# EMAIL_HOST_PASSWORD = 'your_password'
# EMAIL_HOST_USER = 'your_email'
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'JSON_EDITOR': True,
    'VALIDATOR_URL': None,
    'SHOW_REQUEST_HEADERS': False,
    'APIS_SORTER': 'alpha',
    'DEEP_LINKING': True,
    'USE_SESSION_AUTH': False,
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'PERSIST_AUTH': False,
    'DEFAULT_MODEL_RENDERING': 'example',
    'DOC_EXPANSION': 'none',
    'DEFAULT_FIELD_INSPECTORS': (
        'drf_yasg.inspectors.CamelCaseJSONFilter',
        'drf_yasg.inspectors.RecursiveFieldInspector',
        'drf_yasg.inspectors.ReferencingSerializerInspector',
        'drf_yasg.inspectors.ChoiceFieldInspector',
        'drf_yasg.inspectors.FileFieldInspector',
        'drf_yasg.inspectors.DictFieldInspector',
        'drf_yasg.inspectors.HiddenFieldInspector',
        'drf_yasg.inspectors.RelatedFieldInspector',
        'drf_yasg.inspectors.SerializerMethodFieldInspector',
        'drf_yasg.inspectors.SimpleFieldInspector',
        'drf_yasg.inspectors.StringDefaultFieldInspector',
    )
}

DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomStringTokenGenerator",
    "OPTIONS": {
        "min_length": 20,
        "max_length": 30
    }
}
RESET_PASSWORD_URL = env("RESET_PASSWORD_URL", 'http://realEstate.co/reset-pass')

CONTACT_EMAIL = env("CONTACT_EMAIL", 'realEstate.capital@gmail.com')
CONTACT_PHONE = env("CONTACT_PHONE", '(000) 000-0000')

GOOGLE_API_KEY = env('GOOGLE_API_KEY')
GOOGLE_SEARCH_RADIUS = env('GOOGLE_SEARCH_RADIUS', 1000)

with env.prefixed('REDIS_') as e:
    REDIS = 'redis://{}:{}'.format(e('HOST'), e('PORT'))

CELERY_BROKER_URL = REDIS + '/1'
CELERY_RESULT_BACKEND = None
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERY_TASK_IGNORE_RESULT = True
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "max_retries": 3,
    "interval_start": 0.5,
    "interval_step": 0.1,
    "interval_max": 1.0
}
