from PIL import Image
import io
import rembg

class BackgroundRemover:
    """Service for removing backgrounds from images."""
    
    def __init__(self):
        # Import rembg here to avoid loading the model until needed
        try:
            import rembg
            self.rembg = rembg
        except ImportError:
            raise ImportError("rembg library is required. Install it with 'pip install rembg'")
    
    def remove_background(self, image_data: bytes) -> bytes:
        """
        Remove the background from an image.
        
        Args:
            image_data: Image data as bytes
            
        Returns:
            Processed image data as bytes with transparent background
        """
        # Process the image with rembg
        output = self.rembg.remove(image_data)
        return output
    
    def remove_background_from_file(self, input_path: str, output_path: str) -> None:
        """
        Remove the background from an image file and save the result.
        
        Args:
            input_path: Path to the input image
            output_path: Path where the processed image will be saved
        """
        with open(input_path, 'rb') as input_file:
            image_data = input_file.read()
            
        output_data = self.remove_background(image_data)
        
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)