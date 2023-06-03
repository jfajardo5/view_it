# View It

## View-It is a video hosting platform. It is a fun hobby project.

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Getting up and running with docker

### Pre-requisites

- Git
- Python 3.11
- python-venv
- Docker Compose (https://docs.docker.com/compose/install/)
- Pre-commit (https://pre-commit.com/)

### Setup

- Create a venv environment for python to run in (Only needed if you wish to contribute via git):

      $ python -m venv view_it_venv
      $ cd view_it_venv && source bin/activate

- Install pre-commit (Only needed if you wish to contribute via git):

      $ pip install pre-commit

- Clone this repository:

      $ git clone https://github.com/jfajardo5/view_it

- Build a local docker image (The first docker build will take a while):

      $ cd view_it
      $ docker compose -f local.yml build

- Start up the newly created docker container:

      $ docker compose -f local.yml up

- ### That's it! The site should be accessible at http://localhost:3000/ after the container has been fully initialized!

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ docker compose -f local.yml run --rm django python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ docker compose -f local.yml run --rm django mypy view_it

### Test coverage with pytest

To run the tests and check your test coverage:

    $ docker compose -f local.yml run --rm django pytest

## Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [MailHog](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

Container mailhog will start automatically when you run all docker containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`
