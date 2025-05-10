# HTML Conversion API

A REST API service that converts HTML to PDF and images using Puppeteer.

## Features

- HTML to PDF conversion with full styling support
- HTML to Image conversion (PNG/JPEG)
- High fidelity rendering
- Fast cold-start performance
- Docker support
- Simple JSON API

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
docker build -t html-conversion-api .
docker run -p 3000:3000 html-conversion-api
```

## API Endpoints

### Convert HTML to PDF
```bash
curl -X POST http://localhost:3000/api/pdf/convert \
  -H "Content-Type: application/json" \
  -d '{"html":"<html><body><h1>Hello</h1></body></html>"}' \
  --output output.pdf
```

### Convert HTML to Image
```bash
curl -X POST http://localhost:3000/api/image/convert \
  -H "Content-Type: application/json" \
  -d '{"html":"<html><body><h1>Hello</h1></body></html>"}' \
  --output output.png
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
  }
}
```

### Image Options
```json
{
  "type": "png",
  "fullPage": true,
  "transparent": false
}
```

## Error Handling

The API returns JSON error responses in the following format:
```json
{
  "error": "Error message"
}
```

## License

MIT 