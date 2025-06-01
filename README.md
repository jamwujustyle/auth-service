# auth-service

Authentication microservice for **Eldorado**, a marketplace platform built using FastAPI.

This service handles user registration, login, JWT token issuance, and basic user management. It’s built with an async-first approach using FastAPI and Tortoise ORM.

---

## 🔧 Stack

- **FastAPI** — async Python web framework
- **Tortoise ORM** — async ORM with Aerich for migrations
- **PostgreSQL** — relational database
- **Docker** — containerized development
- **python-jose** — for JWT token handling
- **dotenv** — environment variable management

---

## 🚀 Features

- User registration and login with JWT tokens
- Password hashing with bcrypt
- Token verification middleware
- Environment-based config management
- Async DB access and migrations

---

## 🛠️ Local Development

### 1. Set up `.env`

```bash
./scripts/setup-env.sh