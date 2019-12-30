# Insurance Risk API

Hi, this is a simple API system to calculating a risk-profile for insurance packages.

It determines your profile based in some information gathered through some questions about you, your houses and vehicles.

This API has an unique endpoint that accepts a POST request, check out request format, parameters and responses on [swagger documentation](https://github.com/tyronedamasceno).

If you want to run it on your machine, please be sure you have python 3.8 (or later) installed. **I strongly recommend to use a [virtual enviroment](https://docs.python.org/3/library/venv.html).**

When you have *venv* activated, follow the steps below:
```
$ python manage.py migrate
$ python manage.py runserver
```
Now, you have the server running on your `localhost:8000`. Try make some requests and enjoy =D.

If you want to run the tests, try:
`$ python manage.py test`

