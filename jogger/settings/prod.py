import * from base

STATICFILES_DIRS = []
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'dist/static')

ALLOWED_HOSTS = ['toptal-jogger.herokuapp.com']
