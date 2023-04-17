# FastAPI with MongoDB

Repository to practice using [FastAPI](https://fastapi.tiangolo.com/) with [MongoDB](https://www.mongodb.com/).

FastAPI is a micro-framework for development of Rest APIs, created and maintained by [Tiangolo](https://github.com/tiangolo) (real name: [Sebastián Ramírez](https://www.linkedin.com/in/tiangolo/)).

MondoDB is a [NoSQL](https://en.wikipedia.org/wiki/NoSQL), source-available, cross-platform, document-oriented database program. It uses [JSON](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON)-like documents with optional schemas.

## Features

1. Document database connection via both: synchronous (via [__PyMongo__](https://www.mongodb.com/docs/drivers/pymongo/)) and asynchronous (via [__Motor__](https://motor.readthedocs.io/en/stable/index.html)) drivers.
2. User authentication via [Json Web Token](https://jwt.io/) with separate `accessTokens` and `RefreshTokens`.

## Setup

We will now go through how o setup the project on your development machine.

### Pre-Requisites

1. __Python 3.9__
2. __BASh__
    - __GitBASh for Windows__

### Development Setup

__N.B:__ _We are assuming you know how to properly clone a repository from GitHub._

1. Create a new `virtual environment` using `python -m venv env`.
2. Activate the virtual environment via `source env/bin/activate`.
    - `source env/Scripts/activate` in Windows.
3. Install `setup-tools` via the command `python -m pip install pip-tools`
4. Install the dependencies via the command `sh scripts/install_dependencies.sh`
    - This auto-generates the platform-specific `requirements.txt` file via the `requirements.in` file.
    - All new dependencies are to only be added to the `requirements.in` file; the `requirements.txt` file is __not__ to be edited manually.
    - In fact, you can even add the `requirements.txt` file to the `.gitignore` file.
5. Setup [__MongoDB__](https://www.mongodb.com/try/download/community) either locally or in a personal cloud.
    - Also, install [__MongoDB Compass__](https://www.mongodb.com/products/compass) locally on your development machine.
6. Copy the `.env` file to the root folder.
7. You can use `sh scripts/run.sh` to run the application.

## Documentation

1. [Postman Generated](https://documenter.getpostman.com/view/17779018/2s93XzwN15)
2. [Swagger](localhost:8000/docs) ___(___ _Only works if the server is running._ ___)___
