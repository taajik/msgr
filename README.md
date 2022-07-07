# msgr

This is a messenger web app written in Python/Django. It's My first Django project!

> A live demo is available at [msgr.pythonanywhere.com](https://msgr.pythonanywhere.com/).

**Some Screenshots:**
![Screenshots of the app](https://msgr.pythonanywhere.com/media/other/MSGR_Screenshots_2.png)


## Features

It has the basic features expected from a minimum messenger app:
- One-to-one messaging
- Chat groups (coming soon!)
- Real-time chat
- Personal profile with biography and unique ID
- Profile pictures and thumbnails
- Search for users based on their full names and IDs
- Message delete
- Message seen status check marks
- Unread messages counter
- Saved messages chat


## Installation

First, as usual, you need to clone the project and install the requirements (psycopg2 is only required for Postgres).

Then you have to set up the settings.
Settings are located at [project/settings](/project/settings). There are different setting files there.

You have to choose one of the [development](/project/settings/development.py) or [production](/project/settings/production.py) settings, depending on the situation.
You can do that by setting the [DJANGO_SETTINGS_MODULE](https://docs.djangoproject.com/en/4.0/topics/settings/#envvar-DJANGO_SETTINGS_MODULE) environment variable.

In addition to these setting files, you need to create another one named private.py in the settings folder.
This file is for sensitive settings of your particular Django installation.
In the private.py you need to put:

1. [SECRET_KEY](https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/#secret-key): A long, unique, and unpredictable value. You can learn how to generate one [here](https://humberto.io/blog/tldr-generate-django-secret-key/).
2. [DATABASES](https://docs.djangoproject.com/en/4.0/ref/settings/#databases): You should create your database and add its settings here.
3. [ALLOWED_HOSTS](https://docs.djangoproject.com/en/4.0/ref/settings/#std-setting-ALLOWED_HOSTS): This isn't necessary for development, but in production, you have to list your domain names.
3. [TIME_ZONE](https://docs.djangoproject.com/en/4.0/ref/settings/#std-setting-TIME_ZONE): Additionally, you can set your time zone here.

