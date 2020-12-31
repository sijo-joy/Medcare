# Medcare
This system manages medical equipment’s donation, equipment booking using the payment gateway system (For the deposit amount), product returning, and refunding deposit amount to the user’s account.

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/sijo-joy/Medcare.git
$ cd Medcare
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

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd project
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/

