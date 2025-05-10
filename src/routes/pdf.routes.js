const express = require('express');
const { convert } = require('../controllers/pdf.controller');

const router = express.Router();

router.post('/convert', convert);

module.exports = router; 