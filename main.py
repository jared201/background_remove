from fastapi import FastAPI, File, UploadFile, Request, Depends, HTTPException, status
from fastapi.responses import Response, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
import io
from datetime import timedelta
from services.background_remover import BackgroundRemover
from services.auth import (
    authenticate_user, create_access_token, get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES, Token, User, fake_users_db
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
background_remover = BackgroundRemover()


@app.get("/", response_class=HTMLResponse)
@app.head("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Generate a JWT token for authentication.

    This endpoint follows the OAuth2 password flow standard.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/remove-background")
async def remove_background(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove the background from an uploaded image.

    This endpoint requires authentication with a valid JWT token.
    Returns the processed image with a transparent background.
    """
    try:
        # Read the image data
        # The frontend XMLHttpRequest will track the upload progress automatically
        # as the data is being received by the server
        image_data = await image.read()

        # Process the image asynchronously
        output_data = await background_remover.remove_background(image_data)

        # Determine the output format based on the input format
        # Default to PNG for transparency support
        content_type = "image/png"

        # Return the processed image
        return Response(content=output_data, media_type=content_type)
    except Exception as e:
        import logging
        logging.error(f"Error processing image: {str(e)}")
        return Response(content=str(e), status_code=500)
