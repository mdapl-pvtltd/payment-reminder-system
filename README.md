# HTML Conversion API

A REST API service that converts HTML to PDF and images using Puppeteer. This service provides high-fidelity conversion with support for styling, fonts, and JavaScript.

## Features

- HTML to PDF conversion with full styling support
- HTML to Image conversion (PNG/JPEG)
- High fidelity rendering
- Fast cold-start performance
- Docker support
- Simple JSON API
- Base64 output support
- PDF pagination support

## Prerequisites

- Node.js 20+
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd html-conversion-api
```

2. Install dependencies:
```bash
npm install
```

3. Create a .env file:
```bash
PORT=3000
```

## Running the Service

### Development
```bash
npm run dev
```

### Production
```bash
npm start
```

### Docker
```bash
# Build and run
docker compose up --build

# Run in detached mode
docker compose up -d --build

# Stop the service
docker compose down
```

## API Endpoints

### Convert HTML to PDF
```bash
# Binary response
curl -X POST http://localhost:3000/api/pdf/convert \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><body><h1>Hello</h1></body></html>",
    "options": {
      "format": "A4",
      "margin": {
        "top": "1cm",
        "bottom": "1cm"
      },
      "pageNumbers": true
    }
  }' \
  --output output.pdf

# Base64 response
curl -X POST http://localhost:3000/api/pdf/convert \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><body><h1>Hello</h1></body></html>",
    "options": {
      "base64": true,
      "pageNumbers": true
    }
  }'
```

### Convert HTML to Image
```bash
# Binary response
curl -X POST http://localhost:3000/api/image/convert \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><body><h1>Hello</h1></body></html>",
    "options": {
      "type": "png",
      "fullPage": true
    }
  }' \
  --output output.png

# Base64 response
curl -X POST http://localhost:3000/api/image/convert \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><body><h1>Hello</h1></body></html>",
    "options": {
      "base64": true,
      "type": "png"
    }
  }'
```

## Options

### PDF Options
```json
{
  "format": "A4",
  "margin": {
    "top": "1cm",
    "bottom": "1cm",
    "left": "1cm",
    "right": "1cm"
  },
  "pageNumbers": true,
  "base64": false
}
```

### Image Options
```json
{
  "type": "png",
  "fullPage": true,
  "transparent": false,
  "base64": false
}
```

## Deployment

### Render.com Deployment

1. Create a new Web Service in Render
2. Connect your GitHub repository
3. Use these settings:
   - **Environment**: Node
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Environment Variables**:
     ```
     PORT=3000
     NODE_ENV=production
     ```

4. Choose an appropriate plan:
   - Free tier for testing
   - Starter plan ($7/month) or higher for production

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| PORT | Server port | 3000 |
| NODE_ENV | Environment | development |

## Error Handling

The API returns JSON error responses in the following format:
```json
{
  "error": "Error message"
}
```

## Response Formats

### Binary Response
- PDF: `application/pdf`
- Image: `image/png` or `image/jpeg`

### Base64 Response
```json
{
  "data": "base64_encoded_string",
  "type": "application/pdf",
  "filename": "converted.pdf"
}
```

## Security

- Rate limiting enabled (100 requests per 15 minutes)
- CORS enabled
- Helmet security headers
- Non-root user in Docker container
- Input size limit (5MB)

## License

MIT 