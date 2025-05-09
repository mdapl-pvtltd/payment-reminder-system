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

@app.route('/generate/invoice', methods=['POST'])
def generate_invoice():
    """API endpoint to generate invoice PDF or image."""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Get query parameters with defaults
        output_format = request.args.get('output_format', 'pdf').lower()
        red_threshold = int(request.args.get('red', 30))
        yellow_threshold = int(request.args.get('yellow', 15))

        logger.info(f"Processing invoice generation request - Format: {output_format}, "
                   f"Thresholds - Red: {red_threshold}, Yellow: {yellow_threshold}")

        # Initialize processors with custom thresholds
        pdf_generator = PDFGenerator(config)
        image_converter = ImageConverter(config)
        invoice_processor = InvoiceDataProcessor(
            red_threshold=red_threshold,
            yellow_threshold=yellow_threshold
        )

        # Process invoice data
        template_data = invoice_processor.process_invoices(data)
        
        # Render template
        html_content = render_template_with_data('outstanding_invoices.html', template_data)
        
        # Generate PDF
        pdf_bytes = pdf_generator.generate_pdf(html_content)
        
        # Convert to requested format
        if output_format == 'image':
            output_bytes = image_converter.pdf_to_image(pdf_bytes)
            mime_type = f'image/{config.IMAGE_FORMAT.lower()}'
        else:
            output_bytes = pdf_bytes
            mime_type = 'application/pdf'

        # Encode to base64
        base64_output = base64.b64encode(output_bytes).decode('utf-8')
        
        logger.info("Invoice generation completed successfully")
        
        return jsonify({
            "status": "success",
            "data": base64_output,
            "mime_type": mime_type
        })

    except Exception as e:
        logger.error(f"Error processing invoice generation request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    logger.info("Starting application...")
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
