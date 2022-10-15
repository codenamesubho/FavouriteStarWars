# FavouriteStarWars

## Setup:
1. Create virtualenv
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py populate_data

#### Run Test:
5. python manage.py test

#### Run DevServer:
6. python manage.py runserver

## API Documentation:

###### API: Planet List
```
**GET** 127.0.0.1:8000/components/planets/?user_id=10&name=earth
```
**user_id** and **name** are optional param

###### Output

```json
{
    "results": [
        {
            "id": 1,
            "name": "toto",
            "created": "2014-12-09T13:50:49.641000Z",
            "updated": "2014-12-20T20:58:18.411000Z",
            "url": "https://swapi.dev/api/planets/1/",
            "is_favourite": true
        },
        {
            "id": 2,
            "name": "Alderaan",
            "created": "2014-12-10T11:35:48.479000Z",
            "updated": "2014-12-20T20:58:18.420000Z",
            "url": "https://swapi.dev/api/planets/2/",
            "is_favourite": false
        }
    ]
}
```
***

###### API: Movie List
```
**GET** 127.0.0.1:8000/components/movies/?user_id=10&title=Earth
```
**user_id** and **title** are optional param

###### Output

```json
{
    "results": [
        {
            "id": 1,
            "title": "A New Hope",
            "release_date": "1977-05-25T00:00:00Z",
            "created": "2014-12-10T14:23:31.880000Z",
            "updated": "2014-12-20T19:49:45.256000Z",
            "url": "https://swapi.dev/api/films/1/",
            "is_favourite": false
        },
        {
            "id": 2,
            "title": "The Empire Strikes Back",
            "release_date": "1980-05-17T00:00:00Z",
            "created": "2014-12-12T11:26:24.656000Z",
            "updated": "2014-12-15T13:07:53.386000Z",
            "url": "https://swapi.dev/api/films/2/",
            "is_favourite": false
        },
    ]
}
```
***
###### API: Add Favourite Movie 
```
**POST** 127.0.0.1:8000/components/favourite/movie/
```
###### Body:
```json
{
	"user_id":10,
	"movie": 1,
	"custom_title": "toto"
}
```

###### Output

```json
{
    "data": {
        "id": 1,
        "user_id": 10,
        "planet": 1,
        "custom_title": "toto" // optional
    }
}
```
***
###### API: Add Favourite Planet 
```
**POST** 127.0.0.1:8000/components/favourite/planet/
```
###### Body:
```json
{
	"user_id":10,
	"planet": 1,
	"custom_name": "toto" // optional
}
```

###### Output

```json
{
    "data": {
        "id": 1,
        "user_id": 10,
        "planet": 1,
        "custom_name": "toto"
    }
}
```




