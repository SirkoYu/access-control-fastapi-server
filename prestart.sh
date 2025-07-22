#!/usr/bin/env bash
set -e

echo "Run applying migrations"
alembic upgrade head
echo "Migrations are applied"

exec "$@"