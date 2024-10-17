# naurr
[![License](https://img.shields.io/github/license/pawelad/fakester.svg)][license]
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]
[![py.typed](https://img.shields.io/badge/py-typed-FFD43B)][rickroll]

## Running locally
The easiest way run naurr locally is to install [Docker] and run:

```console
$ # Build Docker images
$ make docker-build
$ # Run Docker compose stack
$ make docker-run
```

If everything went well, naurr should be available at http://localhost:8000/.

Alternatively, you can also run it without [Docker], but you need to have [PostgreSQL]
installed and running locally:

```console
$ # Create a Python virtualenv
$ python3 -m venv venv
$ source venv/bin/activate
$ # Install dependencies
$ make install-dev
$ # Run the app
$ make run
```

### Migrations
If you're setting up the app for the first time (or some database model changes were
introduced since you last used it), you need to apply the database migrations:

```console
$ make docker-shell # Skip if not using Docker
$ make apply-migrations
```

It might also be useful to create a superuser for yourself with 
`python src/manage.py createsuperuser`.

### Sample data
There's a couple of helper utils to help load data from an external file. If you
have a text file with one word per line, you can load, group and export it to a
JSON file with:

```console
$ python src/manage.py group_values_by_prefix --input_file=names.csv --output_file=grouped_names.json
```

You can then load that JSON data directly to the database by performing an API call:

```console
$ # I'm using HTTPie (https://httpie.io/cli) as my API client
$ # First, get the API access token
$ http --body POST http://localhost:8000/api/auth/obtain_token username=foobar password=spam
$ export TOKEN={token_from_previous_command}
$ http --body POST http://localhost:8000/api/folder/bulk_add/ "Authorization:Token $TOKEN" < grouped_names.json
```

### Configuration
All configurable settings are loaded from environment variables and a local `.env`
file (in that order). Note that when running locally through Docker Compose, you
need to restart the app for it to pick up the changes.

Available settings:

```
# App environment. Should be set to one of: "local" or "production"
ENVIRONMENT='local'

# Django secret key; should be unique, long and private
# Docs: https://docs.djangoproject.com/en/5.1/ref/settings/#secret-key
SECRET_KEY=CHANGE_ME

# Controls Django's debug mode. Can't be enabled on a non-local enviroment.
# Docs: https://docs.djangoproject.com/en/5.1/ref/settings/#debug
DEBUG=True

# Comma separated list of allowed hosts
# Docs: https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# Database URL
# Docs: https://github.com/jazzband/dj-database-url#url-schema
DATABASE_URL=postgres://postgres@localhost/naurr
```

## Makefile
Available `make` commands:

```console
$ make help
install                                   Install app dependencies
install-dev                               Install app dependencies (including dev)
pip-compile                               Compile requirements files
upgrade-package                           Upgrade Python package (pass "package=<PACKAGE_NAME>")
upgrade-all                               Upgrade all Python packages
run                                       Run the app
create-migration                          Create Django migration (pass "name=<MIGRATION_NAME>")
apply-migrations                          Apply Django migrations
format                                    Format code
test                                      Run the test suite
docker-build                              Build Docker compose stack
docker-run                                Run Docker compose stack
docker-stop                               Stop Docker compose stack
docker-shell                              Run bash inside dev Docker image
clean                                     Clean dev artifacts
help                                      Show help message
```

## Authors
Developed and maintained by [Paweł Adamczak][pawelad].

Source code is available at [GitHub][github naurr].

Released under [Mozilla Public License 2.0][license].


[black]: https://black.readthedocs.io/
[docker]: https://www.docker.com/
[github naurr]: https://github.com/pawelad/naurr
[license]: ./LICENSE
[pawelad]: https://pawelad.me/
[postgresql]: https://www.postgresql.org/
[rickroll]: https://www.youtube.com/watch?v=I6OXjnBIW-4&t=15s
