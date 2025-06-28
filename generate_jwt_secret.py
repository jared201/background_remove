#!/usr/bin/env python3
"""
JWT Secret Key Generator

This script generates a secure random key suitable for use as a JWT secret key.
The key is generated using cryptographically secure random functions.

Usage:
    python generate_jwt_secret.py

The script will output a secure random key that can be used as a JWT secret key.
You should store this key securely, typically in environment variables.
"""

import secrets
import base64
import argparse


def generate_secret_key(length=32):
    """
    Generate a secure random key suitable for JWT token signing.
    
    Args:
        length (int): The length of the key in bytes. Default is 32 bytes (256 bits),
                     which is considered secure for HMAC-SHA256.
    
    Returns:
        str: A URL-safe base64-encoded string representing the secret key.
    """
    # Generate random bytes
    random_bytes = secrets.token_bytes(length)
    
    # Encode to base64 for easier handling and storage
    # Using URL-safe base64 encoding to avoid issues with special characters
    encoded_key = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    
    return encoded_key


def main():
    parser = argparse.ArgumentParser(description='Generate a secure JWT secret key')
    parser.add_argument('--length', type=int, default=32,
                        help='Length of the key in bytes (default: 32)')
    args = parser.parse_args()
    
    secret_key = generate_secret_key(args.length)
    
    print("\nGenerated JWT Secret Key:")
    print("-------------------------")
    print(secret_key)
    print("\nStore this key securely, typically in environment variables.")
    print("For example, in your .env file:")
    print(f"JWT_SECRET_KEY=\"{secret_key}\"")
    print("\nOr set it directly in your environment:")
    print(f"export JWT_SECRET_KEY=\"{secret_key}\"")
    print("\nThen update your code to use this environment variable instead of hardcoding the key.")


if __name__ == "__main__":
    main()