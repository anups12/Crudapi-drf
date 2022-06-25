# Crudapi-drf

To set up  run these commands 
pip install djangorestframework
pip install django-rest-knox


Add the following lines to the settings. py 
for authentication perpose 

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
    ]
}

to configure static and media files 
MEDIA_ROOT = BASE_DIR / 'media'         # 'data' is my media folder
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

In installed apps add 
    'crudapi',
    'rest_framework',
    'knox',
