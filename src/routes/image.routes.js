const express = require('express');
const { convert } = require('../controllers/image.controller');

const router = express.Router();

router.post('/convert', convert);

module.exports = router; 