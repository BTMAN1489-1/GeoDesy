import environs

env = environs.Env()
env.read_env()
SECRET_KEY = env.str('SECRET_KEY').encode('UTF-8')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')

EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env.str('EMAIL_PORT')
EMAIL_HOST_USER = env.str('EMAIL_USER')

EMAIL_HOST_PASSWORD = env.str('EMAIL_PASSWORD')

OFFSET_TIMEZONE = 3
LENGTH_CONFIRM_CODE = 6
INTERVAL_CONFIRM_CODE_IN_SECONDS = 200
INTERVAL_API_TOKEN_IN_SECONDS = 18000
MIN_DISTANCE_BETWEEN_POINTS = 30
