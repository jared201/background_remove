# Background Remover Service

A FastAPI service that removes backgrounds from images using the `rembg` library.

## Features

- Remove backgrounds from images via API
- Returns images with transparent backgrounds
- JWT authentication for API security
- Simple to use and integrate

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd BackgroundRemover
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Service

Start the service using uvicorn:

```
uvicorn main:app --reload
```

The service will be available at http://localhost:8000

## Authentication

The API uses JWT (JSON Web Token) authentication to protect endpoints from unauthorized access.

### Generating a Secret Key

The service includes a script to generate a secure random key for JWT token signing:

```bash
python generate_jwt_secret.py
```

This will output a secure random key that you should store in environment variables rather than hardcoding in your application. The script also supports customizing the key length:

```bash
python generate_jwt_secret.py --length 64  # Generate a 64-byte (512-bit) key
```

### Obtaining a Token

**Endpoint:** `POST /token`

**Request:**
- Form data with username and password fields

**Response:**
- JSON object containing the access token and token type

**Example:**
```bash
curl -X POST -F "username=user" -F "password=password" http://localhost:8000/token
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using the Token

Include the token in the Authorization header of your requests:
```
Authorization: Bearer <your_token>
```

## API Usage

### Remove Background from Image

**Endpoint:** `POST /remove-background`

**Authentication:**
- Required: JWT token in Authorization header

**Request:**
- Form data with an image file

**Response:**
- Image with transparent background (PNG format)

## Testing the Service

A test script is included to help you verify the service is working correctly. Note that the test script may need to be updated to include authentication:

```bash
# Start the server in one terminal
uvicorn main:app --reload

# In another terminal, run the test script with an image
python test_background_remover.py path/to/your/image.jpg [output_path.png]
```

The script will:
1. Authenticate with the API to get a token
2. Send the image to the API with the authentication token
3. Save the result (default: result.png)
4. Open the result with your default image viewer

### Example Usage

Using curl:
```bash
# First, get a token
TOKEN=$(curl -s -X POST -F "username=user" -F "password=password" http://localhost:8000/token | jq -r '.access_token')

# Then use the token to access the protected endpoint
curl -X POST -H "Authorization: Bearer $TOKEN" -F "image=@/path/to/your/image.jpg" http://localhost:8000/remove-background --output result.png
```

Using Python requests:
```python
import requests

# Get a token
token_url = "http://localhost:8000/token"
token_data = {"username": "user", "password": "password"}
token_response = requests.post(token_url, data=token_data)
token = token_response.json()["access_token"]

# Use the token to access the protected endpoint
url = "http://localhost:8000/remove-background"
headers = {"Authorization": f"Bearer {token}"}
files = {"image": open("path/to/your/image.jpg", "rb")}
response = requests.post(url, headers=headers, files=files)

# Save the result
with open("result.png", "wb") as f:
    f.write(response.content)
```

## API Documentation

FastAPI automatically generates interactive API documentation.
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Notes

- The service uses the `rembg` library which downloads a model on first use
- For best results, use images with clear subjects and contrasting backgrounds
- The service returns PNG images to preserve transparency
