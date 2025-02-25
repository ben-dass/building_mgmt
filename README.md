# Building Management

Tenant & Request Management.

## First Steps

1. Install dependencies.

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

2. Enter `.env.dev` variables.
3. Build database.

```bash
make build
make up

# Ensure docker <-> db is set up correctly by being able to login.
make psql
\q
```

4. Run migrations & create a superuser.

```bash
# Migrations.
poetry-makemigrations
poetry-migrate

# Create superuser.
poetry-createsuperuser
```

5. Success! You should be able to runserver.

```bash
poetry-runserver
```

## VENV management

```bash
python3.13 -m venv .venv
python3 -m venv .venv
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

## Other Config

### Generating secret key

```bash
python -c "import secrets; print(secrets.token_urlsafe(38))"
```
