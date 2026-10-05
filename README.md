# Project 1

Due: Oct 23rd, 11:59PM

| Grading Criteria | Description                                                                                                                                                                                                                                                                                                                                               | Weight |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| Ambition         | Graded relative to other projects. It is hard to get marks for this category. These marks are awarded for projects<br>that go significantly beyond my expectations with respect to technical ambition and scope.                                                                                                                                          | 20     |
| Polish           | Usability, mobile responsiveness, visual consistency and style.<br>Strongly recommend that you [test your project thoroughly with real users](https://dn790002.ca.archive.org/0/items/SteveKrugDontMakeMeThink/Steve_Krug_Don%E2%80%99t_Make_Me_Think%2C.pdf) (Chapter 9, p141) and get feedback.<br>Hint: You can test with other students in the class. | 35     |
| Functionality    | Application works without crashing/bugs                                                                                                                                                                                                                                                                                                                   | 10     |
| Use of HTMX      | HTMX used where it improves user experience to complement server side rendering                                                                                                                                                                                                                                                                           | 10     |
| Use of Django    | Models, url routing, views, and templates are reasonable                                                                                                                                                                                                                                                                                                  | 10     |
| README.md        | Explains application purpose, contains useful screenshots of application and instructions to run the application<br>locally (including setting up API keys if needed)                                                                                                                                                                                     | 10     |
| Security         | Django's protections not disabled, API keys not committed to repo or exposed, personal data not exposed, etc                                                                                                                                                                                                                                              | 5      |

## AI Use

You may use AI to write code.

Human-facing text in your application as well as human-facing documentation (e.g. README) **must** be written by you.

I encourage you not to generate image assets used in your application with AI.

## Submitting the Project

This repository contains a minimal Django project with no apps or models. Build off of this for your first project.

The project is submitted by committing and pushing to the main branch of this repository. Please verify that your
web application successfully deployed to the production server, as we will be grading what is deployed on your server!

For deployment to work, you must complete [Lab 3 - Automated Deployment](https://portal.carleton.university/c/itec4012/docs/lab-3-automated-deployment/). It's a prerequisite for submitting your project.

## Setup to run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

The values in `.env.example` work as they are for local development, so no editing is needed to get started.

```bash
python manage.py migrate
python manage.py runserver
```

Then access the server at http://localhost:8000

## Configuration Notes

We want to use different settings in our development server versus our production server. When we've completed a feature
for our application, we want to push the changes to our source code to the production server, but we don't want our
local development settings to be pushed to the production server. 

These settings include things like:
* Is the server running in debug mode?
* What is the URL of the server (e.g. 127.0.0.1:8000 or james.projects.carleton.university)?
* What secret keys does the server use?

We don't want to hardcode the values for these settings in the application source code that we send to github, because
we actually want these settings to be different when developing locally versus remotely. 

To solve this problem, we store values for these settings in *environment variables*. Locally, we [read these variables 
from a file](https://django-environ.readthedocs.io/) called `.env` that is excluded from version control with the
`.gitignore` file. The file `.env.example` has a working local value for each one.

Then when we deploy our application to the production server the Django application reads from the server environment 
and picks up different values. The values that will run on the server are defined in `deploy/project_1.service`.

Here are some variables that we can set in Django:

| Variable               | Description                                 | Local values                                  | Production values                                       |
|------------------------|---------------------------------------------|-----------------------------------------------|---------------------------------------------------------|
| `SECRET_KEY`           | used by some security features              | `django-insecure-local-development-only`      | generated by `deploy.sh` in `/etc/project_1/env`        |
| `DEBUG`                | detailed error pages in HTTP responses      | `True`                                        | unset                                                   |
| `ALLOWED_HOSTS`        | domains the server can run on               | `localhost,127.0.0.1`                         | `<your-subdomain>.projects.carleton.university`         |
| `CSRF_TRUSTED_ORIGINS` | urls that forms can be submitted from       | `http://localhost:8000,http://127.0.0.1:8000` | `https://<your-subdomain>.projects.carleton.university` |
| `DATABASE_URL`         | location of application database            | `sqlite:///db.sqlite3`                        | `sqlite:////var/lib/project_1/db.sqlite3`               |
| `STATIC_ROOT`          | location of static files (e.g. css, images) | `staticfiles`                                 | `/var/lib/project_1/static`                             |
| `MEDIA_ROOT`           | location of user-uploaded files             | `media`                                       | `/var/lib/project_1/media`                              |


## Deployment

On the production server we run the application as a systemd service. Systemd services are pretty neat. They let you
set up a unit file that defines a *service*. Then the service can be run/restarted with a single command.

Systemd services are a boring and standard way to deploy a web application on linux. You can define the following
with your systemd service:

* a description of the service
* what user account the service runs as (you can limit the permissions of this account!)
* the directory that the process runs in
* what folders the service is allowed to write in
* what environment variables are given to the service
* what commands to run before starting up the service
* what command to run which runs the service
* what to do if the service crashes (restart it!)
* whether to run the service automatically when the computer turns on
* what things to wait for before starting up the service

Because I'm such a nice prof, I've set up a service file for you in `deploy/project_1.service`. I've documented
it thoroughly, so feel free to take a look. Once you've set up GitHub Actions, whatever changes you make to it 
will automatically deploy to the production server. Here's how that will work:

1) Your AI agent opens a pull request
2) You approve the pull request, which merges to the main branch
3) This triggers a GitHub Action which runs in the cloud:
   - The GitHub action connects to your production server
   - The GitHub action copies over all the changes from the main branch to the production server
   - The GitHub action triggers the `deploy.sh` script on the production server
4) The `deploy.sh` script copied to the production server runs and:
   - Copies application code to `/opt/project_1/app`
   - Installs python dependencies named in `requirements.txt`
   - Installs `deploy/project_1.service` and restarts it
5) Restarting the `project_1` service on the production server will:
   - Run `python manage.py migrate` on the server and collect static files
   - Start `gunicorn` and run the server

What this looks like to you is that merging a pull request magically makes that change appear on the production server!

It also means you shouldn't edit application files manually on the production server, because future pushes to the main
branch  will automatically wipe out those changes.

## Where files are located in production

Note that the file layout is also different on the production server compared to the development server. Locally in 
development, all project files are in one folder. On the production server, the files will be located in these locations:

| Location               | Contents                         | Owner                  |
|------------------------|----------------------------------|------------------------|
| `/opt/project_1/app`   | code                             | root                   |
| `/opt/project_1/venv`  | virtualenv                       | root                   |
| `/var/lib/project_1`   | SQLite database and static files | `project_1`            |
| `/etc/project_1/env`   | secret key                       | root, not readable by others |


### Before your first deploy

You need to set up the address of your website in your service file. Find it on
<https://portal.carleton.university>, then find the below lines in `deploy/project_1.service`
replace `CHANGE-ME` on both of these lines with your hostname (e.g. itec-4012-integral-basilisk.projects.carleton.university):

```ini
Environment=ALLOWED_HOSTS=CHANGE-ME
Environment=CSRF_TRUSTED_ORIGINS=https://CHANGE-ME
```

The deploy won't work until you do this.

### Useful commands to run on your production server

```bash
systemctl status project_1            # check the service status
sudo journalctl -u project_1 -f       # view logs
sudo systemctl restart project_1      # restart the app
```

To run a `manage.py` command on the production server, do the following:

```bash
/opt/project_1/app/deploy/manage.sh createsuperuser
```

## htmx

[django-htmx](https://django-htmx.readthedocs.io/) is installed. `request.htmx` is available in your views to check
whether a request came from htmx. To load htmx on a page, add this to your base django template:

```django
{% load django_htmx %}
<head>
    {% htmx_script %}
</head>
```

Django rejects `POST`, `PUT` and `DELETE` requests without a CSRF token. This includes htmx requests made with
`hx-post`, `hx-put` and `hx-delete`. To send a CSRF token with with every htmx request,
add this attribute to the `<body>` tag of your base Django template:

```django
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
```
