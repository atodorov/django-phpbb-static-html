django-phpbb-static-html
========================

Quick and dirty Django app which helps dump a phpBB into static HTML for archiving purposes

Installation
------------

    $ cd myproject/
    $ pip install Django==1.6.8 MySQL-python boto django-storages
    $ git clone https://github.com/atodorov/django-phpbb-static-html phpbb_to_static

Then edit `settings.py` to look like this

```
INSTALLED_APPS = (
    'phpbb_to_static',
)

DATABASES = {
    'default': {
# this is either a dump of your phpBB database or the production instance (not recommended)
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db-name',
        'USER': 'db-user',
        'PASSWORD': 'db-pass',
        'HOST': 'localhost',
    },
}


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# in case you're dumping to Amazon S3
AWS_S3_ACCESS_KEY_ID='XXXXXXX'
AWS_S3_SECRET_ACCESS_KEY='YYY'
AWS_STORAGE_BUCKET_NAME='s3-bucket'
```



How to use
----------

    $ ./manage.py static_sync


This will generate static HTML for your index, forum and topic pages.
Avatars are linked to Gravatar.
