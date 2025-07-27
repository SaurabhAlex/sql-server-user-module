# FastAPI User Management API

A simple RESTful API for user management using FastAPI and SQLAlchemy.

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── database.py     # Database connection and session management
│   ├── models.py       # SQLAlchemy ORM models
│   ├── schemas.py      # Pydantic models for request/response validation
│   └── routers/
│       ├── __init__.py
│       └── users.py    # User-related endpoints
├── .env                # Environment variables (database connection string)
├── main.py            # FastAPI application setup
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd first_project
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database connection

Edit the `.env` file and update the `DATABASE_URL` with your actual database connection string from Azure Data Studio.

For PostgreSQL:
```
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

For SQL Server:
```
DATABASE_URL=mssql+pyodbc://username:password@server_name/dbname?driver=ODBC+Driver+17+for+SQL+Server
```

### 5. Run the application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the auto-generated Swagger UI documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Available Endpoints

### Users

- `GET /users/`: Get all users
- `GET /users/{user_id}`: Get a specific user by ID
- `POST /users/`: Create a new user
- `PUT /users/{user_id}`: Update a user
- `DELETE /users/{user_id}`: Delete a user

## Database Schema

The `users` table has the following structure:

| Column          | Type      | Description                   |
|-----------------|-----------|-------------------------------|
| id              | Integer   | Primary key                   |
| username        | String    | Unique username               |
| email           | String    | Unique email address          |
| hashed_password | String    | Password (hashed)             |
| is_active       | Boolean   | User status                   |
| created_at      | DateTime  | Timestamp of creation         |
| updated_at      | DateTime  | Timestamp of last update      |