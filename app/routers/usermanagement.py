from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal
import pyodbc
import os

router = APIRouter(
    prefix="/usermanagement",
    tags=["User Management"],
)

# Database connection setup
def get_connection():
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

@router.get("/")
async def read_root():
    return {"message": "User Management root endpoint"}

@router.post("/users/save", response_model=schemas.UserCustom)
def create_user(user: schemas.UserCustomCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO [dbo].[User] (u_name, email, gender, mobile_no, role_id, u_password)
        OUTPUT INSERTED.user_id
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (user.u_name, user.email, user.gender, user.mobile_no, user.role_id, user.u_password))
        inserted_id = cursor.fetchone()[0]
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    return schemas.UserCustom(
        id=inserted_id,
        u_name=user.u_name,
        email=user.email,
        gender=user.gender,
        mobile_no=user.mobile_no,
        role_id=user.role_id,
    )

@router.get("/users/{user_id}", response_model=schemas.UserCustom)
def read_user(user_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT user_id, u_name, email, gender, mobile_no, role_id FROM [dbo].[User] WHERE user_id = ?"
        cursor.execute(sql, (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return {
                "id": row[0],
                "u_name": row[1],
                "email": row[2],
                "gender": row[3],
                "mobile_no": row[4],
                "role_id": row[5],
            }
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading user: {str(e)}")

@router.put("/users/{user_id}", response_model=schemas.UserCustom)
def update_user(user_id: int, user: schemas.UserCustomUpdate):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        update_fields = []
        params = []
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            update_fields.append(f"{key} = ?")
            params.append(value)
        params.append(user_id)
        sql = f"UPDATE [dbo].[User] SET {', '.join(update_fields)} WHERE user_id = ?"
        cursor.execute(sql, params)
        conn.commit()
        cursor.close()
        conn.close()
        return {**user_data, "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM [dbo].[User] WHERE user_id = ?"
        cursor.execute(sql, (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"detail": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")

@router.get("/users/", response_model=list[schemas.UserCustom])
def list_users():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "SELECT user_id, u_name, email, gender, mobile_no, role_id FROM [dbo].[User]"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        users = []
        for row in rows:
            users.append({
                "id": row[0],
                "u_name": row[1],
                "email": row[2],
                "gender": row[3],
                "mobile_no": row[4],
                "role_id": row[5],
            })
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing users: {str(e)}")
