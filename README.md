# Starnavi API Task

Simple Rest Api with Users, Posts, Likes/Dislikes

###Stack:
* API: Flask
* PostgreSQL

Deployment:

`make docker-up`

<small>docker-compose up with all required initializing/migration commands such as</small>

`flask db init`

`flask db migrate`

`flask db upgrade`

`flask run`


Tests:

User Register, User Login (+JWT access key), Create Post, Like & Dislike Post

`make test`

<a>http://localhost:5000/api/analytics?date_from=2018-12-30&date_to=2021-05-01

Like count URL

### api_user table:

| Field  | Type  | Null | KEY | DEFAULT | EXTRA |
| ------------- | ------------- | ------ | ----- | ----- | ------- |
| id  | int  | NO | PRIMARY | NULL | auto_increment |
| email  | varchar(60) | NO |  | NULL |  |
| password | varchar | NO |  | NULL |  |
| first_name | varchar(50) | NO |  | NULL |  |
| last_name | varchar(50) | NO |  | NULL |  |
| birth_date | date | NO |  | NULL |  |

