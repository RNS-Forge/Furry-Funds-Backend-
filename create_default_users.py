#!/usr/bin/env python3
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from app.common.models import UserRole

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_default_users():
    # Database connection
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://ihub:ihub@harlee.6sokd.mongodb.net/")
    DB_NAME = os.getenv("DB_NAME", "Daily")
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]
    
    # Define target test accounts
    test_password = "San@123"
    password_hash = get_password_hash(test_password)
    
    users_to_create = [
        {
            "email": "operator@gmail.com",
            "name": "Default Operator",
            "phone": "9876543210",
            "password_hash": password_hash,
            "role": UserRole.OPERATOR,
            "first_login": False,
            "is_active": True
        },
        {
            "email": "manager@gmail.com",
            "name": "Default Manager",
            "phone": "9876543211",
            "password_hash": password_hash,
            "role": UserRole.MANAGER,
            "first_login": False,
            "is_active": True
        },
        {
            "email": "admin@gmail.com",
            "name": "Default Admin",
            "phone": "9876543212",
            "password_hash": password_hash,
            "role": UserRole.ADMIN,
            "first_login": False,
            "is_active": True
        },
        {
            "email": "admin1@gmail.com",
            "name": "Default Admin 1",
            "phone": "9876543213",
            "password_hash": password_hash,
            "role": UserRole.ADMIN,
            "first_login": False,
            "is_active": True
        }
    ]
    
    try:
        print("Upserting static test accounts...")
        for user_data in users_to_create:
            existing = await db.users.find_one({"email": user_data["email"]})
            if existing:
                # Update password and status
                await db.users.update_one(
                    {"email": user_data["email"]},
                    {"$set": {
                        "password_hash": user_data["password_hash"],
                        "first_login": False,
                        "is_active": True,
                        "role": user_data["role"]
                    }}
                )
                print(f"Updated password for existing user: {user_data['email']}")
            else:
                # Insert new user
                await db.users.insert_one(user_data)
                print(f"Created new user: {user_data['email']}")
                
        print("\nAll default accounts successfully setup!")
        
    except Exception as e:
        print(f"Error creating users: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(create_default_users())
