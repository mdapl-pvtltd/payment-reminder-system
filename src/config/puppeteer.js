const puppeteer = require('puppeteer');

let browser;

const getBrowser = async () => {
  if (!browser) {
    browser = await puppeteer.launch({
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
      headless: 'new'
    });
  }
  return browser;
};

const closeBrowser = async () => {
  if (browser) {
    await browser.close();
    browser = null;
  }
};

module.exports = {
  getBrowser,
  closeBrowser
}; 