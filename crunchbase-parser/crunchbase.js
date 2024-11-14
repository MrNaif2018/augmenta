const express = require("express");
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
const bodyParser = require("body-parser");

puppeteer.use(StealthPlugin());

const app = express();
const port = 3000;

app.use(bodyParser.json());

async function scrapeData(url, page) {
  const cookies = [
    {
      name: "cookieName",
      value: "cookieValue",
      domain: "www.crunchbase.com",
    },
  ];

  await page.setCookie(...cookies);

  const headers = {
    accept: "application/json, text/plain, */*",
    "accept-language": "en-IN,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    pragma: "no-cache",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "x-cb-client-app-instance-id": "a9318595-d00b-4f8f-8739-99dab0f0b793",
    "x-requested-with": "XMLHttpRequest",
    "x-xsrf-token": "d7Q4dVVFSBqpMmXMYWpfhQPhnaMpLfl0vDPkOa2ZqxQ",
    cookie: "cid=CiirNWUwKhc0uQAbwq5cAg==; featuILsw",
    Referer: "https://www.crunchbase.com/organization/cerkl",
    "Referrer-Policy": "same-origin",
  };

  await page.setExtraHTTPHeaders(headers);
  await page.goto(url, { waitUntil: "networkidle2" });

  return page.evaluate(() => {
    const extractText = (selector) => {
      const element = document.querySelector(selector);
      return element ? element.innerText.trim() : null;
    };

    let text = extractText("script#ng-state");
    if (!text) {
      text = extractText("script#client-app-state");
    }
    return text;
  });
}

app.post("/scrape", async (req, res) => {
  let { name } = req.body;

  if (!name) {
    return res.status(400).send({ error: "Name is required" });
  }
  // to lower case
  name = name.toLowerCase();
  try {
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();
    await page.setViewport({ width: 384, height: 832 });
    await page.setUserAgent(
      "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    );
    const url = `https://www.crunchbase.com/organization/${name}`;
    const data = await scrapeData(url, page);
    await browser.close();

    res.json(data);
  } catch (error) {
    console.error("Error scraping data:", error);
    res.status(500).send({ error: "Error scraping data" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});