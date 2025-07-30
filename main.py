from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routers import users, usermanagement
from app.database import engine
from app import models
import azure_sql_api

# Skipping database initialization to avoid connection errors
# Commenting out the DB initialization code to allow app to start without DB connection
# import os
# from app.database import DATABASE_URL

# if DATABASE_URL:
#     models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI User Management",
    description="A simple RESTful API for user management using FastAPI and SQLAlchemy",
    version="0.1.0",
    docs_url="/swagger",  # Change Swagger UI path to /swagger
    redoc_url="/redoc",   # Keep ReDoc at /redoc
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(azure_sql_api.router)
app.include_router(usermanagement.router)


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the User Management API"}

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
