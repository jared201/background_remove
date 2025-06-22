# Background Remover Service

A FastAPI service that removes backgrounds from images using the `rembg` library.

## Features

- Remove backgrounds from images via API
- Returns images with transparent backgrounds
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

## API Usage

### Remove Background from Image

**Endpoint:** `POST /remove-background`

**Request:**
- Form data with an image file

**Response:**
- Image with transparent background (PNG format)

## Testing the Service

A test script is included to help you verify the service is working correctly:

```bash
# Start the server in one terminal
uvicorn main:app --reload

# In another terminal, run the test script with an image
python test_background_remover.py path/to/your/image.jpg [output_path.png]
```

The script will:
1. Send the image to the API
2. Save the result (default: result.png)
3. Open the result with your default image viewer

### Example Usage

Using curl:
```bash
curl -X POST -F "image=@/path/to/your/image.jpg" http://localhost:8000/remove-background --output result.png
```

Using Python requests:
```python
import requests

url = "http://localhost:8000/remove-background"
files = {"image": open("path/to/your/image.jpg", "rb")}
response = requests.post(url, files=files)

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
