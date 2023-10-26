# Bongo BD 

## Setup

To run this project, locally using docker:
```
$ docker-compose build
$ docker-compose up
```
Create migrations and apply them to the database.
```
$ docker-compose exec web python manage.py makemigrations
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py createsuperuser
```
Test it out at http://localhost:8000
## API Endpoints
 - GET
   ```
   "Restaurants": api/restaurants/
   "Votes": api/votes/
   "Restaurant winner": api/restaurant-winner/
   "Current day menu": api/current_day_menu/
   ```
  - POST
    ```
    "Register a user" : api/register
    "User login" : api/login
    "Logout user" : api/logout
    "All registerd user" : api/user
    ```
    Post URLs will perform successfully authorized login.