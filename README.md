
# auth_service

## Overview
"auth_service" is a lightweight authentication service for microservice architecture, focusing on efficient user authentication and data management.

## Features
- **User Registration**: Enabling unique username-password based registration.
- **Login**: Providing JWT tokens for authenticated users.
- **User Data Storage**: Storing personal user data in JSON format.
- **user/me Handler**: Managing and retrieving user-specific information.
- **Rate Limiting**: Implementing access control.

## Technology Stack
- **Language**: Python
- **Framework**: FastAPI
- **Design**: Modular for extendability

## Installation and Setup
Includes `pyproject.toml` for Poetry dependencies and a Dockerfile for containerization.

## Configuration
Service configuration requires these environment variables:
- `USER_DATA_STORE`: Path for user data.
- `USERS_STORE`: Path for user credentials.
- `SECRET_KEY`: Application's secret key.
- `APP_KEYS`: Client-side secrets.

## Usage Instructions
Endpoints for user authentication and data management:

| URL                             | Method   | Description                              | Data Types & Examples |
|---------------------------------|----------|------------------------------------------|-----------------------|
| `/api/v0.1/auth/login`          | `POST`   | Authenticate users, returning a JWT token. | **form**: `username` (string), `password` (string)<br> **Example**: `username=user`, `password=PaSSword!` |
| `/api/v0.1/auth/register`       | `POST`   | Register new users. | **form**: `username` (string), `password` (string), `client_secret` (string)<br> **Example**: `username=newuser`, `password=NewPass!`, `client_secret=secret1` |
| `/api/v0.1/user/me`             | `GET`    | Retrieve profile information of the authenticated user. | **Headers**: `Authorization: Bearer [JWT_TOKEN]` |
| `/api/v0.1/user/me`             | `PATCH`  | Update profile information of the authenticated user. | **Headers**: `Authorization: Bearer [JWT_TOKEN]`<br>**Body**: JSON object<br>**Example**: `{ "email": "example@mail.com", "full_name": "John Doe" }` |
| `/api/v0.1/user/data`           | `GET`    | Get stored personal data of the authenticated user. | **Headers**: `Authorization: Bearer [JWT_TOKEN]` |
| `/api/v0.1/user/data`           | `POST`   | Update or add new personal data for the authenticated user. | **Headers**: `Authorization: Bearer [JWT_TOKEN]`<br>**Body**: JSON object<br>**Example**: `{ "android_key": "abcd1234", "app_ver": 1010, "force_update": false }` |

**Note**: Replace `[JWT_TOKEN]` with the actual JWT token obtained after login.