# Access Control System

A web-based application for managing user access and permissions.

## Table of Contents

* [About](#about)
* [Features](#features)
* [Technical Details](#technical-details)
* [Getting Started](#getting-started)
* [API Documentation](#api-documentation)
* [Database Schema](#database-schema)
* [Contributing](#contributing)
* [License](#license)

## About

The Access Control System is a web-based application designed to manage user access and permissions. It provides a robust and scalable solution for organizations to control and monitor user access to sensitive resources.

## Features

* User Management: Create, read, update, and delete users
* Role Management: Create, read, update, and delete roles
* Access Rule Management: Create, read, update, and delete access rules
* Access Log Management: Create, read, and delete access logs
* Authentication and Authorization: Securely authenticate and authorize users using JWT tokens

## Technical Details

* Built with FastAPI (version 0.116.1)
* Database Operations: Powered by SQLAlchemy (version 2.0.41)
* Alembic Migrations: Manage database schema changes (version 1.16.4)
* Pydantic Validation: Ensure data consistency and validation (version 2.11.7)
* Database Schema: Defined using SQLAlchemy and Alembic

## Getting Started

1. Clone the repository: `git clone https://github.com/[your-username]/access-control-system.git`
2. Install dependencies: `poetry install`
3. Configure database: Create a database and configure the database connection in [src/core/config.py](cci:7://file:///c:/Users/ITryHard/Desktop/Projects/Project/src/core/config.py:0:0-0:0)
4. Run the application: `poetry run uvicorn src.main:main_app --host 0.0.0.0 --port 8000`

## API Documentation

The API documentation is available at the `/docs` endpoint.

## Database Schema

The database schema is defined in the [src/models](cci:7://file:///c:/Users/ITryHard/Desktop/Projects/Project/src/models:0:0-0:0) directory and includes the following tables:

* users: Stores user information
* roles: Stores role information
* access_rules: Stores access rule information
* access_logs: Stores access log information

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.

## License

Access Control System is licensed under the MIT License.

## Badges

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/release/python-313/)
[![FastAPI 0.116.1](https://img.shields.io/badge/FastAPI-0.116.1-green.svg)](https://fastapi.tiangolo.com/)