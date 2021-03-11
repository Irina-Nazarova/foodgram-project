![Build Status](https://github.com/Irina-Nazarova/foodgram-project/workflows/foodgram-app%20workflow/badge.svg)

# foodgram-project

Foodgram — grocery assistant. 
The project can be deployed in three Docker containers using docker-compose.

## Site url:

[www.foodgram.pytools.ru](http://foodgram.pytools.ru/)

## Test User

You can use test user to Login:

Username: test_user

Password: kNzfTb34


## Starting docker-compose:
```
docker-compose up --build
```
## First Start
**For the first launch**, for project functionality, go inside to the container:
```
docker exec -t -i <WEB CONTAINER ID> bash
```
**Make migrations:**
```
python manage.py migrate
```
**To create a superuser:**
```
python manage.py createsuperuser
```

## Functionality

* Full user authentication
* Create/edit/delete new recipe
* Filter by breakfast/lunch/dinner
* Choose from a bunch of ingredients
* Add to favourites
* Favourites page
* Follow another authors
* Add to shopping list
* Download shopping list

## Tech Stack
* [Python 3.8.5](https://www.python.org/)
* [Django 3.1.4](https://www.djangoproject.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
