const { getBrowser } = require('../config/puppeteer');

const convertToImage = async (html, options = {}) => {
  const browser = await getBrowser();
  const page = await browser.newPage();

  try {
    await page.setContent(html, {
      waitUntil: 'networkidle0'
    });

    const screenshotOptions = {
      type: options.type || 'png',
      fullPage: options.fullPage || true,
      omitBackground: options.transparent || false
    };

    const image = await page.screenshot(screenshotOptions);
    return image;
  } finally {
    await page.close();
  }
};

module.exports = {
  convertToImage
}; 