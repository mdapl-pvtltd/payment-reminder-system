const { getBrowser } = require('../config/puppeteer');

const convertToPDF = async (html, options = {}) => {
  const browser = await getBrowser();
  const page = await browser.newPage();

  try {
    await page.setContent(html, {
      waitUntil: 'networkidle0'
    });

    const pdfOptions = {
      format: options.format || 'A4',
      margin: options.margin || {
        top: '1cm',
        bottom: '1cm',
        left: '1cm',
        right: '1cm'
      },
      printBackground: true
    };

    const pdf = await page.pdf(pdfOptions);
    return pdf;
  } finally {
    await page.close();
  }
};

module.exports = {
  convertToPDF
}; 