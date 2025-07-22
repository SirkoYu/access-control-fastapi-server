#!/usr/bin/env bash
echo "Run applying migrations"
alembic upgrade head
echo "Migrations are applied"

exec "$@"