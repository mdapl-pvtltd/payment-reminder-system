require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const app = require('./src/app');

const PORT = process.env.PORT || 3000;

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

// Apply middleware
app.use(cors());
app.use(helmet());
app.use(limiter);

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
}); 