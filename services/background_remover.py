from PIL import Image
import io
import rembg
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackgroundRemover:
    """Service for removing backgrounds from images."""

    def __init__(self):
        # Import rembg here to avoid loading the model until needed
        try:
            import rembg
            self.rembg = rembg
            # Create a thread pool executor for CPU-bound tasks
            self.executor = ThreadPoolExecutor(max_workers=4)
        except ImportError:
            raise ImportError("rembg library is required. Install it with 'pip install rembg'")

    async def remove_background(self, image_data: bytes) -> bytes:
        """
        Remove the background from an image asynchronously.

        Args:
            image_data: Image data as bytes

        Returns:
            Processed image data as bytes with transparent background
        """
        try:
            # Run the CPU-intensive task in a thread pool
            loop = asyncio.get_running_loop()
            output = await loop.run_in_executor(
                self.executor, 
                self._remove_background_sync, 
                image_data
            )
            return output
        except Exception as e:
            logger.error(f"Error removing background: {str(e)}")
            raise

    def _remove_background_sync(self, image_data: bytes) -> bytes:
        """
        Synchronous method to remove background, to be run in a thread pool.

        Args:
            image_data: Image data as bytes

        Returns:
            Processed image data as bytes with transparent background
        """
        # Process the image with rembg
        return self.rembg.remove(image_data)

    async def remove_background_from_file(self, input_path: str, output_path: str) -> None:
        """
        Remove the background from an image file and save the result asynchronously.

        Args:
            input_path: Path to the input image
            output_path: Path where the processed image will be saved
        """
        try:
            with open(input_path, 'rb') as input_file:
                image_data = input_file.read()

            output_data = await self.remove_background(image_data)

            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)
        except Exception as e:
            logger.error(f"Error processing file {input_path}: {str(e)}")
            raise
