const { convertToImage } = require('../services/image.service');

const convert = async (req, res, next) => {
  try {
    const { html, options } = req.body;

    if (!html) {
      return res.status(400).json({ error: 'HTML content is required' });
    }

    const image = await convertToImage(html, options);
    
    if (options?.base64) {
      const contentType = options?.type === 'jpeg' ? 'image/jpeg' : 'image/png';
      return res.json({
        data: image.toString('base64'),
        type: contentType,
        filename: `converted.${options?.type || 'png'}`
      });
    }
    
    const contentType = options?.type === 'jpeg' ? 'image/jpeg' : 'image/png';
    res.setHeader('Content-Type', contentType);
    res.setHeader('Content-Disposition', `attachment; filename=converted.${options?.type || 'png'}`);
    res.send(image);
  } catch (error) {
    next(error);
  }
};

module.exports = {
  convert
}; 