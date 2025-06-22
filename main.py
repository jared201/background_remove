from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import Response, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io
from services.background_remover import BackgroundRemover

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
background_remover = BackgroundRemover()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/remove-background")
async def remove_background(image: UploadFile = File(...)):
    """
    Remove the background from an uploaded image.

    Returns the processed image with a transparent background.
    """
    # Read the image data
    # The frontend XMLHttpRequest will track the upload progress automatically
    # as the data is being received by the server
    image_data = await image.read()

    # Process the image
    output_data = background_remover.remove_background(image_data)

    # Determine the output format based on the input format
    # Default to PNG for transparency support
    content_type = "image/png"

    # Return the processed image
    return Response(content=output_data, media_type=content_type)
