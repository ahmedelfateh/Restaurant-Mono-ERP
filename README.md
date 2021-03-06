<h1 align="center"> Restaurants 🛖 </h1>

<p align="center">
<a href="https://github.com/pydanny/cookiecutter-django/">
<img alt="Cookiecutter Django " src="https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg">
</a>

<a href="https://github.com/ambv/black">
<img alt="Black code style" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>

<a href="https://choosealicense.com/licenses/unlicense/">
<img alt="License: unlicense" src="https://img.shields.io/badge/License-Unlicense-brightgreen">
</a>
</p>

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### setup the development environment

1. [Install docker on you platform.](https://docs.docker.com/docker-for-windows/install/)
2. [Install docker-compose on your platform.](https://docs.docker.com/compose/install/)
3. Run the Development environment:

```bash
    git clone https://github.com/ahmedelfateh/Restaurant-Mono-ERP.git
    cd Restaurant-Mono-ERP
    docker-compose up --build
```

4. Open another terminal tab, to migrate DB:

```bash
    docker-compose run --rm django ./manage.py migrate
```

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, your login done.
- To create an **superuser account**, start in the root folder and use this command:

```bash
    docker-compose run --rm django ./manage.py createsuperuser
```

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

- To run any django command inside the docker environment, start in the root folder and use this command:

```bash
    docker-compose run --rm django ./manage.py **...django_command...**
    docker-compose run --rm django ./manage.py makemigrations
```

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report::

```bash
    docker-compose run --rm django coverage run -m pytest
    docker-compose run --rm django coverage html
    open htmlcov/index.html
```

### Testing

- Run tests, for all app:

```bash
    docker-compose run --rm django ./manage.py test --debug-mode
```

## Access App

- you can access the App Admin on [Admin](http://localhost:8000/admin/)
- you can access the App API on [API](http://localhost:8000/api/)
