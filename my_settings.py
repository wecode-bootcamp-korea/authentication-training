SECRET_KEY = 'YOUR_SECRET_KEY'

ALGORITHM = 'HS256' 

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'DB_HOST',
        'PORT': 'DB_PORT'
    }
}
