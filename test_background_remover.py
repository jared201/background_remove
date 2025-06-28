import requests
import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def get_auth_token(server_url="http://localhost:8000"):
    """
    Get an authentication token from the server.

    Args:
        server_url: URL of the server running the service

    Returns:
        The authentication token or None if authentication failed
    """
    try:
        # Get a token
        url = f"{server_url}/token"
        print(f"Authenticating with {url}...")

        # For demo purposes, we're using hardcoded credentials
        # In a real application, you might want to pass these as parameters
        data = {
            "username": "user",
            "password": "password"
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            print("Authentication successful!")
            return token
        else:
            print(f"Authentication failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error during authentication: {str(e)}")
        return None

def test_background_removal(image_path, output_path="result.png", server_url="http://localhost:8000"):
    """
    Test the background removal service with a local image.

    Args:
        image_path: Path to the input image
        output_path: Path where the result will be saved
        server_url: URL of the server running the service
    """
    # Check if the image exists
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return False

    # Get authentication token
    token = get_auth_token(server_url)
    if not token:
        print("Cannot proceed without authentication.")
        return False

    try:
        # Send the request to the server
        url = f"{server_url}/remove-background"
        print(f"Sending image to {url}...")

        # Set up headers with authentication token
        headers = {
            "Authorization": f"Bearer {token}"
        }

        with open(image_path, "rb") as img_file:
            files = {"image": (os.path.basename(image_path), img_file, "image/jpeg")}
            response = requests.post(url, headers=headers, files=files)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the result
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Background removed successfully! Result saved to {output_path}")
            return True
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print(response.text)
            return False

    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the server at {server_url}")
        print("Make sure the server is running with: uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python test_background_remover.py <path_to_image> [output_path]")
        sys.exit(1)

    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "result.png"

    # Run the test
    success = test_background_removal(image_path, output_path)

    # Open the result if successful
    if success:
        try:
            # Try to open the image with the default viewer
            output_path_abs = os.path.abspath(output_path)
            print(f"Opening result: {output_path_abs}")

            if sys.platform == 'darwin':  # macOS
                subprocess.call(('open', output_path_abs))
            elif sys.platform == 'win32':  # Windows
                os.startfile(output_path_abs)
            else:  # Linux and other Unix-like
                subprocess.call(('xdg-open', output_path_abs))
        except Exception as e:
            print(f"Could not open the result automatically: {str(e)}")
            print(f"Please open {output_path} manually to view the result.")
