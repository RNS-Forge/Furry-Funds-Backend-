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

async def clear_db_and_insert_users():
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
        # Clear the database collections
        collections = await db.list_collection_names()
        print(f"Clearing collections in database '{DB_NAME}': {collections}")
        for col_name in collections:
            await db[col_name].delete_many({})
            print(f"Cleared collection: {col_name}")
            
        # Re-insert the static users
        print("\nInserting static test accounts...")
        for user_data in users_to_create:
            await db.users.insert_one(user_data)
            print(f"Created user: {user_data['email']}")
                
        print("\nDatabase cleared and default accounts successfully setup!")
        
    except Exception as e:
        print(f"Error clearing/populating database: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(clear_db_and_insert_users())
