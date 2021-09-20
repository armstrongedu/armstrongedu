from .common import *

ALLOWED_HOSTS = ['dedolms.com', 'www.dedolms.com', 'dev.dedolms.com',]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS=ENV.str('EMAIL_USE_TLS')
EMAIL_PORT=ENV.str('EMAIL_PORT')
EMAIL_HOST=ENV.str('EMAIL_HOST')
EMAIL_HOST_PASSWORD=ENV.str('EMAIL_HOST_PASSWORD')
