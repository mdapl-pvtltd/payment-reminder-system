from weasyprint import HTML
from loguru import logger
import os
from typing import Optional, Dict, Any
from .config import Config

class PDFGenerator:
    def __init__(self, config: Optional[Config] = None):
        """Initialize PDF generator with configuration."""
        self.config = config or Config()
        logger.info("PDF Generator initialized")

    def generate_pdf(self, html_content: str, options: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Generate PDF from HTML content with optional configuration.
        
        Args:
            html_content (str): HTML content to convert
            options (dict, optional): PDF generation options
            
        Returns:
            bytes: Generated PDF content
        """
        try:
            logger.info("Starting PDF generation")
            
            # Set default options
            pdf_options = {
                'dpi': self.config.PDF_DPI,
                'format': self.config.PDF_FORMAT,
                **(options or {})
            }
            
            # Create HTML object
            html = HTML(string=html_content)
            
            # Generate PDF
            pdf_bytes = html.write_pdf(**pdf_options)
            
            logger.info("PDF generation completed successfully")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise

    def generate_pdf_from_template(self, template_name: str, template_data: Dict[str, Any], 
                                 options: Optional[Dict[str, Any]] = None) -> bytes:
        """
        Generate PDF from a template file with data.
        
        Args:
            template_name (str): Name of the template file
            template_data (dict): Data to inject into template
            options (dict, optional): PDF generation options
            
        Returns:
            bytes: Generated PDF content
        """
        try:
            logger.info(f"Generating PDF from template: {template_name}")
            
            # Load and render template
            template_path = os.path.join(self.config.TEMPLATE_DIR, template_name)
            if not os.path.exists(template_path):
                raise FileNotFoundError(f"Template not found: {template_name}")
            
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Generate PDF
            return self.generate_pdf(html_content, options)
            
        except Exception as e:
            logger.error(f"Error generating PDF from template: {str(e)}")
            raise
