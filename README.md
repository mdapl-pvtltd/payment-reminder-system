# HTML to PDF/Image Converter API

This is a Python-based API service that converts HTML templates into PDFs or images, returning the output as a base64-encoded string.

## Features

- Convert HTML templates to PDF or images
- Dynamic content injection via JSON payload
- Support for image URLs in templates
- Detailed logging
- Base64 encoded output

## Prerequisites

- Python 3.8 or higher
- Poppler (for PDF to image conversion)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd payment-reminder-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Poppler:
- On macOS: `brew install poppler`
- On Ubuntu: `sudo apt-get install poppler-utils`
- On Windows: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/)

## Usage

1. Start the server:
```bash
python src/app.py
```

2. Send a POST request to `http://localhost:5000/convert` with the following JSON structure:
```json
{
    "template_name": "outstanding_invoices.html",
    "output_format": "pdf",  // or "image"
    "data": {
        // Your template data here
    }
}
```

3. The API will return a JSON response with the base64-encoded output:
```json
{
    "status": "success",
    "data": "base64_encoded_string",
    "mime_type": "application/pdf"  // or "image/png"
}
```

## Configuration

The application can be configured using environment variables or a `.env` file. See `src/config.py` for available options.

## Logging

Logs are stored in the `logs` directory with rotation and retention policies.

## Error Handling

The API returns appropriate HTTP status codes and error messages in case of failures.

## License

[Your License Here]