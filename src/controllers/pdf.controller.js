const { convertToPDF } = require('../services/pdf.service');

const convert = async (req, res, next) => {
  try {
    const { html, options } = req.body;

    if (!html) {
      return res.status(400).json({ error: 'HTML content is required' });
    }

    const pdf = await convertToPDF(html, options);
    
    if (options?.base64) {
      return res.json({
        data: pdf.toString('base64'),
        type: 'application/pdf',
        filename: 'converted.pdf'
      });
    }
    
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', 'attachment; filename=converted.pdf');
    res.send(pdf);
  } catch (error) {
    next(error);
  }
};

module.exports = {
  convert
}; 