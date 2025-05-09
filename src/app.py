from flask import Flask, request, jsonify
from jinja2 import Environment, FileSystemLoader
import base64
import os
from loguru import logger
import json
from datetime import datetime
from .config import Config
from .pdf_generator import PDFGenerator
from .image_converter import ImageConverter
from .data_processor import InvoiceDataProcessor

# Configure logger
logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

app = Flask(__name__)
config = Config()

# Initialize converters and processors
pdf_generator = PDFGenerator(config)
image_converter = ImageConverter(config)
invoice_processor = InvoiceDataProcessor()

# Configure Jinja2
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))

def render_template_with_data(template_name, data):
    """Render HTML template with provided data."""
    try:
        template = env.get_template(template_name)
        return template.render(**data)
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        raise

@app.route('/convert', methods=['POST'])
def convert_template():
    """API endpoint to convert HTML template to PDF or image."""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract parameters
        template_name = data.get('template_name', 'outstanding_invoices.html')
        output_format = data.get('output_format', 'pdf')  # 'pdf' or 'image'
        invoices = data.get('invoices', [])
        options = data.get('options', {})

        logger.info(f"Processing request for template: {template_name}, format: {output_format}")

        # Process invoice data
        template_data = invoice_processor.process_invoices(invoices)
        
        # Render template
        html_content = render_template_with_data(template_name, template_data)
        
        # Generate PDF
        pdf_bytes = pdf_generator.generate_pdf(html_content, options.get('pdf_options'))
        
        # Convert to requested format
        if output_format.lower() == 'image':
            output_bytes = image_converter.pdf_to_image(pdf_bytes, options.get('image_options'))
            mime_type = f'image/{config.IMAGE_FORMAT.lower()}'
        else:
            output_bytes = pdf_bytes
            mime_type = 'application/pdf'

        # Encode to base64
        base64_output = base64.b64encode(output_bytes).decode('utf-8')
        
        logger.info("Conversion completed successfully")
        
        return jsonify({
            "status": "success",
            "data": base64_output,
            "mime_type": mime_type
        })

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/convert-multi', methods=['POST'])
def convert_template_multi():
    """API endpoint to convert HTML template to multiple images (one per page)."""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extract parameters
        template_name = data.get('template_name', 'outstanding_invoices.html')
        invoices = data.get('invoices', [])
        options = data.get('options', {})

        logger.info(f"Processing multi-page conversion request for template: {template_name}")

        # Process invoice data
        template_data = invoice_processor.process_invoices(invoices)
        
        # Render template
        html_content = render_template_with_data(template_name, template_data)
        
        # Generate PDF
        pdf_bytes = pdf_generator.generate_pdf(html_content, options.get('pdf_options'))
        
        # Convert to multiple images
        image_bytes_list = image_converter.pdf_to_images(pdf_bytes, options.get('image_options'))
        
        # Encode all images to base64
        base64_outputs = [
            base64.b64encode(img_bytes).decode('utf-8')
            for img_bytes in image_bytes_list
        ]
        
        logger.info(f"Multi-page conversion completed successfully. Generated {len(base64_outputs)} images.")
        
        return jsonify({
            "status": "success",
            "data": base64_outputs,
            "mime_type": f'image/{config.IMAGE_FORMAT.lower()}',
            "page_count": len(base64_outputs)
        })

    except Exception as e:
        logger.error(f"Error processing multi-page conversion request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    logger.info("Starting application...")
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
