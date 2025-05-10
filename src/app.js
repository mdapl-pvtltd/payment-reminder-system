const express = require('express');
const pdfRoutes = require('./routes/pdf.routes');
const imageRoutes = require('./routes/image.routes');
const errorHandler = require('./middlewares/errorHandler');

const app = express();

// Middleware
app.use(express.json({ limit: '5mb' }));

// Routes
app.use('/api/pdf', pdfRoutes);
app.use('/api/image', imageRoutes);

// Error handling
app.use(errorHandler);

module.exports = app; 