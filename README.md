# Building Management

Tenant & Request Management.

## First Steps

```bash
brew install pipx
pipx install poetry

# This should automatically put you in the virtual environment.
# Make sure to add Django or any other depencendies to the pyproject.toml file.
poetry install

# Troubleshooting
poetry env list
poetry env info
poetry env remove <environment-name-as-listed>
```

## Poetry commands

```bash
poetry-runserver
poetry-makemigrations
poetry-migrate
poetry-shell
poetry-test
poetry-createsuperuser
poetry-startapp <app-name>
poetry-startproject <project-name> <location>
```

## Postgres

### Local (MacOS) nstall

```bash
brew install postgresql
brew services start postgresql
brew services stop postgresql
```

### Configuring

```bash
psql postgres

create role benadmin with login password '12345';

# Give elevated privileges, allow benadmin to create and manage databases.
alter role benadmin createdb;

\q

# Login as the new user: benadmin.
psql postgres -U benadmin
# Create the database for the project: estate.
CREATE DATABASE estate;
# Ensure that it exists.
\l
```