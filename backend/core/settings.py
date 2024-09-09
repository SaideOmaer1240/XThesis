from pathlib import Path
from datetime import timedelta
from decouple import config  
# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent 

# Segurança
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
GROQ_API_KEY = config('GROQ_API_KEY', default='') 
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')
GROQ_MODEL_NAME = config('GROQ_MODEL_NAME', default='')
ALLOWED_HOST = config('ALLOWED_HOSTS', default='')
# Hosts permitidos
ALLOWED_HOSTS = [
    ALLOWED_HOST ]

# Aplicativos instalados
INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    "django.contrib.sites",
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts', 
    'rest_framework',
    'corsheaders',
    'app',
    'chat',
    'tools',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django_grip.GripMiddleware',
]

# Configuração de CORS
CORS_ALLOWED_ORIGINS = [
   ALLOWED_HOST ]

CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=True, cast=bool)

# Configuração de CSRF
CSRF_TRUSTED_ORIGINS = [
   ALLOWED_HOST ]

# Configuração de URL raiz
ROOT_URLCONF = 'core.urls'

# Configuração de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Aplicação WSGI e ASGI
WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application' 

# Configuração de camadas de canal
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("xthesis-redis-1", 6379)],  # nome do contêiner Redis no Docker
        },
    },
}

# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DATABASE_NAME', default='postgres'),
        'USER': config('DATABASE_USER', default='postgres'),
        'PASSWORD': config('DATABASE_PASSWORD', default='password'),
        'HOST': config('DATABASE_HOST', default='inaudibly-flashy-flatfish.data-1.use1.tembo.io'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
} 

# Configuração do Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Configuração do JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('JWT_ACCESS_TOKEN_LIFETIME', default=30, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('JWT_REFRESH_TOKEN_LIFETIME', default=1, cast=int)),
}

# Validadores de senha
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

# Internacionalização
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos e de mídia 
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/' 
STATIC_ROOT = '/app/staticfiles'

# Campo de chave primária padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração adicional
AUTHENTICATION_BACKENDS = ['accounts.backends.AuthBackend']
