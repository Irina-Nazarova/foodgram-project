![Build Status](https://github.com/Irina-Nazarova/foodgram-project/workflows/foodgram-app%20workflow/badge.svg)

# foodgram-project

Foodgram — grocery assistant. Here you can create your own recipes, subscribe to other authors. There is a page for favorites, and you can also make a list of products based on selected recipes with subsequent unloading. Filtering recipes by tags has been implemented. The project can be deployed in three Docker containers using docker-compose.

## Site url:
--


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
docker exec web -t -i <WEB CONTAINER ID> bash
```
**Make migrations:**
```
python manage.py migrate
```
**To create a superuser:**
```
python manage.py createsuperuser
```


## Tech Stack
* [Python 3.8.5](https://www.python.org/)
* [Django 3.1.4](https://www.djangoproject.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
