# UAV-Rental-Project-with-Django

***UAV Rental Project with Django*** 

## Table of Contents
- [About](#about)
- [Built With](#built-with)
- [Prerequisites](#prerequisites)
- [How to Build](#how-to-build)
- [Getting Started](#getting-started)
- [Pages](#pages)
- [Routes](#page-routes)

## About
**UAV Rental Project** is a project that allows users to manage aircraft production processes and part stock tracking

## Built With
* [![Django][Django.com]][Django-url]
* [![DjangoRestFramework][DjangoRestFramework.com]][DjangoRestFramework-url]
* [![PostgreSQL][PostgreSQL.com]][PostgreSQL-url]
* [![Docker][Docker.com]][Docker-url]
* [![Bootstrap 5][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]
* [![Swagger][Swagger.com]][Swagger-url]

## Prerequisites 
- **[Docker](https://www.docker.com/)**
- **[Python ](https://www.python.org/downloads/)**

## How to Build

To build the packages, follow these steps:

```bash
# Open a terminal (Command Prompt or PowerShell for Windows, Terminal for macOS/Linux)

# Clone the repository
git clone https://github.com/onur-dogan/UAV-Rental-Project-with-Django.git

# Navigate to the project's root directory
cd UAV-Rental-Project-with-Django

# Build docker 
docker-compose build

# Run docker 
docker-compose up
```

## Getting Started
- After successfull deployment, open the [Sign Up](http://localhost:8000/signup/) page. Register to the system by filling the informations.
- After registering successfully, [Login](http://localhost:8000/login/) page will display. Login to the system. One of the [Parts](#parts-parts), [Aircrafts](#aircrafts-aircrafts) pages opens according to the user's team.


## Pages
### PARTS ("/parts")
Part page lists the parts, stock informations and mobilities. Under the list tables, some forms exist. The user can add parts to the stock or remove parts from the stock via using these forms. 

**User Actions**
- When the user adds any part to the stock, the stock count increases and a new mobility log creates. Otherwise, when the user removes a part from the stock, the stock count decreases and a new mobility log creates.

**Permissions**
- In this part, the user can make any process on only the parts which it has permission. However, it can list all of the parts on the tables. 
- On the other hand, the users who have permission to see [Aircrafts](#aircrafts-aircrafts) can see the part lists but can't make any stock process.

### AIRCRAFTS ("/aircrafts")
Aircraft page lists the aircrafts, produced aircraft informations and aircraft production which is in progress. Under the aircraft list tables, there are some forms to assembly a new aircraft and list/manage the aircraft production processes. 

**User Actions** 
- While assemblying a new aircraft, the system checks the stocks whether the required parts are enough or missing in the stocks. According to the results, it shows warnings to the user or allow to assembly a new aircraft.
- In the manage table, the user can change the aircraft produces statuses as completed or canceled. According to the selection, the stock counts update and new log creates for each process. They are listed on the [Part](#parts-parts) page.

**Permissions**
- Only the teams that have the permission could see this page. Other users don't have permission to open it.


## Page Routes
- [`/`](http://localhost:8080/) ==> Django Rest Framework Api Root Documentation
- [`/login`](http://localhost:8000/login) ==> Login Page
- [`/signup`](http://localhost:8000/signup) ==> Sign up Page
- [`/parts`](http://localhost:8000/parts) ==> [Part](#parts-parts) Page
- [`/aircrafts`](http://localhost:8000/aircrafts) ==> [Aircraft](#aircrafts-aircrafts) Page
- [`swagger`](http://localhost:8000/swagger) ==> Swagger Documentation
- [`/admin`](http://localhost:8080/admin) ==> Django Administration Page


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Django.com]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green
[Django-url]: https://www.djangoproject.com/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[DjangoRestFramework.com]: https://img.shields.io/badge/django--rest--framework-3.12.2-blue?style=for-the-badge&labelColor=333333&logo=django&logoColor=white&color=blue
[DjangoRestFramework-url]: https://www.django-rest-framework.org/
[PostgreSQL.com]: https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Docker.com]: https://img.shields.io/badge/docker-257bd6?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/ 
[Bootstrap-url]: https://getbootstrap.com/docs/5.0/getting-started/introduction/
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[Swagger.com]: https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white
[Swagger-url]: https://swagger.io/ 