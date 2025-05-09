from pdf2image import convert_from_bytes
from PIL import Image
import io
from loguru import logger
from typing import Optional, Dict, Any, List
from .config import Config

class ImageConverter:
    def __init__(self, config: Optional[Config] = None):
        """Initialize image converter with configuration."""
        self.config = config or Config()
        logger.info("Image Converter initialized")

    def pdf_to_image(self, pdf_bytes: bytes, options: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Convert PDF bytes to image bytes.
        
        Args:
            pdf_bytes (bytes): PDF content to convert
            options (dict, optional): Conversion options
            
        Returns:
            bytes: Generated image content
        """
        try:
            logger.info("Starting PDF to image conversion")
            
            # Set default options
            conversion_options = {
                'dpi': self.config.PDF_DPI,
                'fmt': self.config.IMAGE_FORMAT.lower(),
                'quality': self.config.IMAGE_QUALITY,
                **(options or {})
            }
            
            # Convert PDF to images
            images = convert_from_bytes(pdf_bytes, **conversion_options)
            
            if not images:
                raise ValueError("No images generated from PDF")
            
            # Convert first page to bytes
            img_byte_arr = io.BytesIO()
            images[0].save(img_byte_arr, format=self.config.IMAGE_FORMAT, 
                         quality=self.config.IMAGE_QUALITY)
            
            logger.info("PDF to image conversion completed successfully")
            return img_byte_arr.getvalue()
            
        except Exception as e:
            logger.error(f"Error converting PDF to image: {str(e)}")
            raise

    def pdf_to_images(self, pdf_bytes: bytes, options: Optional[Dict[str, Any]] = None) -> List[bytes]:
        """
        Convert PDF bytes to multiple image bytes (one per page).
        
        Args:
            pdf_bytes (bytes): PDF content to convert
            options (dict, optional): Conversion options
            
        Returns:
            List[bytes]: List of generated image contents
        """
        try:
            logger.info("Starting PDF to multiple images conversion")
            
            # Set default options
            conversion_options = {
                'dpi': self.config.PDF_DPI,
                'fmt': self.config.IMAGE_FORMAT.lower(),
                'quality': self.config.IMAGE_QUALITY,
                **(options or {})
            }
            
            # Convert PDF to images
            images = convert_from_bytes(pdf_bytes, **conversion_options)
            
            if not images:
                raise ValueError("No images generated from PDF")
            
            # Convert each page to bytes
            image_bytes = []
            for img in images:
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format=self.config.IMAGE_FORMAT, 
                        quality=self.config.IMAGE_QUALITY)
                image_bytes.append(img_byte_arr.getvalue())
            
            logger.info(f"PDF to multiple images conversion completed successfully. Generated {len(image_bytes)} images.")
            return image_bytes
            
        except Exception as e:
            logger.error(f"Error converting PDF to multiple images: {str(e)}")
            raise

    def optimize_image(self, image_bytes: bytes, options: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Optimize image bytes for web delivery.
        
        Args:
            image_bytes (bytes): Image content to optimize
            options (dict, optional): Optimization options
            
        Returns:
            bytes: Optimized image content
        """
        try:
            logger.info("Starting image optimization")
            
            # Set default options
            optimization_options = {
                'quality': self.config.IMAGE_QUALITY,
                'optimize': True,
                **(options or {})
            }
            
            # Open image from bytes
            img = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Optimize and save
            output = io.BytesIO()
            img.save(output, format=self.config.IMAGE_FORMAT, **optimization_options)
            
            logger.info("Image optimization completed successfully")
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error optimizing image: {str(e)}")
            raise
