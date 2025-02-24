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
