from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import pyodbc
import os

router = APIRouter(
    prefix="/azure_sql_api",
    tags=["Azure SQL API"],
)

# Pydantic models
class Country(BaseModel):
    id: int
    name: str

class State(BaseModel):
    id: int
    name: str
    country_id: int

# Database connection setup
def get_connection():
    # Connection parameters from environment variables or hardcoded for now
    server = os.getenv("AZURE_SQL_SERVER", "localhost")
    database = os.getenv("AZURE_SQL_DATABASE", "SMS")
    username = os.getenv("AZURE_SQL_USERNAME", "sa")
    password = os.getenv("AZURE_SQL_PASSWORD", "Alex@123#")
    driver = '{ODBC Driver 18 for SQL Server}'

    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;'
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

@router.get("/dbcheck")
def db_check():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return {"status": "Database connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

@router.get("/countries", response_model=List[Country])
def get_countries():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC sp_GetCountries")
        rows = cursor.fetchall()
        countries = [Country(id=row[0], name=row[1]) for row in rows]
        return countries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching countries: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/states/{country_id}", response_model=List[State])
def get_states(country_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Call stored procedure with parameter country_id
        cursor.execute("EXEC sp_GetStatesByCountryId ?", country_id)
        rows = cursor.fetchall()
        states = [State(id=row[0], name=row[1], country_id=row[2]) for row in rows]
        return states
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching states: {str(e)}")
    finally:
        cursor.close()
        conn.close()

class User(BaseModel):
    user_id: int
    u_name: str
    email: str
    gender: str | None = None

@router.get("/login/{email}/{password}", response_model=List[User])
def login(email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Call stored procedure with parameters email and password
        cursor.execute("EXEC verifyUserCredential ?, ?", email, password)
        rows = cursor.fetchall()
        users = [User(user_id=row[0], u_name=row[1], email=row[2], gender=row[3]) for row in rows]
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during login: {str(e)}")
    finally:
        cursor.close()
        conn.close()
