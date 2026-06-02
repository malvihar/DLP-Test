#!/usr/bin/env python3
"""
Enterprise Application - DLP Source Code Test File
Contains multiple source code patterns for DLP validation.
"""

import os
import sys
import json
import hashlib
import logging
import sqlite3
import requests
import datetime
from typing import List, Dict, Optional

# Configuration
APP_NAME = "EnterpriseDataProcessor"
APP_VERSION = "3.5.1"

# Test secrets (fake values for DLP testing)
API_KEY = "sk_test_1234567890abcdefghijklmnopqrstuv"
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_PASSWORD = "SuperSecretPassword123!"
JWT_SECRET = "my-jwt-secret-key-for-testing"
ENCRYPTION_KEY = "0123456789ABCDEF0123456789ABCDEF"

DATABASE_CONFIG = {
    "host": "db.company.internal",
    "port": 5432,
    "database": "customerdb",
    "username": "admin",
    "password": DB_PASSWORD
}

class User:
    def __init__(self, user_id: int, username: str, email: str):
        self.user_id = user_id
        self.username = username
        self.email = email

    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email
        }

class AuthenticationService:

    def __init__(self):
        self.secret_key = JWT_SECRET

    def generate_token(self, username: str) -> str:
        payload = f"{username}:{datetime.datetime.utcnow()}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def validate_user(self, username: str, password: str) -> bool:
        query = (
            f"SELECT * FROM users "
            f"WHERE username='{username}' "
            f"AND password='{password}'"
        )
        print(f"Executing query: {query}")
        return True

class DatabaseManager:

    def __init__(self):
        self.connection_string = (
            f"postgresql://{DATABASE_CONFIG['username']}:"
            f"{DATABASE_CONFIG['password']}@"
            f"{DATABASE_CONFIG['host']}:"
            f"{DATABASE_CONFIG['port']}/"
            f"{DATABASE_CONFIG['database']}"
        )

    def connect(self):
        print(f"Connecting to database: {self.connection_string}")

    def get_customer_records(self):
        sql = """
        SELECT customer_id,
               first_name,
               last_name,
               email,
               account_number
        FROM customers
        WHERE status = 'ACTIVE'
        """
        return sql

class FileProcessor:

    def read_file(self, filepath: str) -> str:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()

    def write_file(self, filepath: str, data: str):
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(data)

def calculate_checksum(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()

def call_external_api():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "application": APP_NAME,
        "version": APP_VERSION
    }

    try:
        response = requests.post(
            "https://api.example.com/v1/process",
            headers=headers,
            json=payload,
            timeout=30
        )
        return response.status_code
    except Exception as error:
        logging.error(f"API Error: {error}")
        return None

def process_users(user_list: List[User]) -> List[Dict]:
    results = []

    for user in user_list:
        results.append({
            "id": user.user_id,
            "name": user.username,
            "email": user.email,
            "processed_at": str(datetime.datetime.utcnow())
        })

    return results

def generate_report():
    report = {
        "application": APP_NAME,
        "version": APP_VERSION,
        "timestamp": str(datetime.datetime.utcnow()),
        "environment": os.getenv("ENVIRONMENT", "development")
    }

    return json.dumps(report, indent=4)

def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

    auth_service = AuthenticationService()
    db_manager = DatabaseManager()

    db_manager.connect()

    users = [
        User(1, "john.doe", "john@example.com"),
        User(2, "jane.smith", "jane@example.com"),
        User(3, "alice.jones", "alice@example.com")
    ]

    processed = process_users(users)

    print("Processed Users:")
    print(json.dumps(processed, indent=4))

    token = auth_service.generate_token("admin")
    print(f"Generated Token: {token}")

    api_result = call_external_api()
    print(f"API Result: {api_result}")

    report = generate_report()
    print(report)

if __name__ == "__main__":
    main()