<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h2 align="center">Flask training (skill-up) application</h2>

</div>


<!-- ABOUT THE PROJECT -->
## About The Project

This repository contains the code for the application defined in the technical specification, which you can find in the documetation.


Project documentation:
* [Technical requirements](docs/flask_training_task.pdf)
* [Api Endpoints (Postman collection)](docs/autopark_flask_postman_collection.json)
* [Api Endpoints Examples](docs/api_requests_examples.MD)

### Built With

List any major frameworks/libraries used to bootstrap project.

* [Docker](https://docs.docker.com/engine/install/)
* [Docker-compose](https://docs.docker.com/compose/install/)
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/)
* [marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)
* [pytest](https://docs.pytest.org/en/6.2.x/index.html)
* [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

You should install following software first:
* Git
* Docker
* Docker-compose

### Installation

1.Clone the repo
   ```sh
   git clone https://github.com/sheleh/autopark_flask
   ```
2.Activate virtual environment
   ```sh
   source /venv/bin/activate
   ```
3.Make first application build via docker-compose
   ```sh
   docker-compose up
   ```

3.Move .env configuration file to the project root



### Project resources
_Run project on local machine_

   ```sh
   docker-compose up
   ```


_Finally local uri is..._

   ```sh
   http://localhost:5000/api/
   ```

### Tests running

_Connect to application container_

   ```sh
   docker exec -it {application container} /bin/bash
   ```

_Running tests on local machine_

   ```sh
   {application container} pytest --setup-show tests
   ```



<!-- CONTRIBUTING -->
## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- CONTACT -->
## Contact

Dmytro Shelekhov  - shelex87@gmail.com

Project Link: [https://github.com/sheleh/autopark_flask](https://github.com/sheleh/autopark_flask)


