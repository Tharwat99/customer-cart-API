# customer-cart-API
Simple API for an eCommerce site for customer cart manipulation. The API should allow users to view their cart details, add and remove products, and update the quantity of products in the cart.

## Normal Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Tharwat99/customer-cart-API.git
$ cd customer-cart-API
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Then makemigrations and migrate models to sqlite db:

```sh
(env)$ python manage.py makemigrations 
(env)$ python manage.py migrate
```

Once `pip` has finished downloading the dependencies:

```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

## Tests

To run the tests:
```sh
(env)$ python manage.py test
```
## Docker Setup

build docker-compose file
```sh
$ docker-compose up --build
```
## Tests

To run the tests:
```sh
(env)$ docker-compose run api sh -c "python manage.py test"
```
```
