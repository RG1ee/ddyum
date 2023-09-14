# DDYUM API - Book Photo Shoots

# Description
The API provides a convenient way to
interact between the photographer and customers,
allowing the photographer to manage bookings.

# Technologies
- Programming Language: Python
- Framework: FastAPI
- Database: PostgreSQL, Redis
- API Documentation: Swagger

# Installation
```bash
git clone git@github.com:RG1ee/ddyum.git
cd ddyum

cat env.sample > .env
# change the value in `.env`
```

# Locally for development
```bash
python3.11 -m venv .venv
. .venv/bin/activate

# install all dependencies
poetry install

# install pre-commit
pre-commit install

# raise a docker container with a database
docker compose up -d --build db

# roll up the migration
alembic upgrade head
```

# Deployment
```bash
docker compose up -d --build
```
