# services/auth_service.py
from flask import Flask, request, jsonify
from services.email_verification import verify_email_domain

# Simple in-memory database for users
users_db = {}

def register_user(email, password):
    # Check if email is allowed
    if not verify_email_domain(email):
        return {"status": "rejected", "message": "Only university emails allowed"}

    # Check if user already exists
    if email in users_db:
        return {"status": "rejected", "message": "User already exists"}

    # Save user
    users_db[email] = {"password": password}
    return {"status": "approved", "message": "Registration successful"}

def login_user(email, password):
    if email not in users_db:
        return {"status": "rejected", "message": "User not found"}
    if users_db[email]["password"] != password:
        return {"status": "rejected", "message": "Incorrect password"}
    return {"status": "approved", "message": "Login successful"}