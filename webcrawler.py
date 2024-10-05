import aiohttp # type: ignore
import asyncio
from bs4 import BeautifulSoup
import json
from playwright.async_api import async_playwright # type: ignore
import nest_asyncio

# Apply nest_asyncio to allow nested event loops (useful for Jupyter notebooks)
nest_asyncio.apply()

class AsyncWebCrawler:
    def __init__(self, verbose=False, proxy=None):
        self.verbose = verbose
        self.proxy = proxy

    async def fetch(self, session, url):
        proxy = self.proxy if self.proxy else None
        try:
            async with session.get(url, proxy=proxy) as response:
                if self.verbose:
                    print(f"Fetching {url} - Status: {response.status}")
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Failed to fetch {url} with status {response.status}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    async def fetch_with_js(self, url):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=60000)  # 60 seconds timeout
                content = await page.content()
                await browser.close()
                if self.verbose:
                    print(f"Fetched {url} with JavaScript execution")
                return content
        except Exception as e:
            print(f"Error fetching {url} with JS: {e}")
            return None

    def parse(self, html, url):
        soup = BeautifulSoup(html, "lxml")
        headlines = []

        for article in soup.select('article.tease-card'):
            headlines.append(article.h2.get_text(strip=True))
        
        return headlines

    async def arun(self, url, use_js=False):
        async with aiohttp.ClientSession() as session:
            if use_js:
                html = await self.fetch_with_js(url)
            else:
                html = await self.fetch(session, url)
            if html:
                return self.parse(html, url)
            return []

async def crawl_and_save(urls, output_file="output.json"):
    crawler = AsyncWebCrawler(verbose=True)
    tasks = []
    for url in urls:
        tasks.append(crawler.arun(url, use_js=False))
    
    results = await asyncio.gather(*tasks)
    
    # Structure the data
    crawled_data = {}
    for url, headlines in zip(urls, results):
        crawled_data[url] = headlines
    
    # Save to JSON file
    with open(output_file, "w") as f:
        json.dump(crawled_data, f, indent=4)
    
    print(f"Successfully crawled data saved to {output_file}")

if __name__ == "__main__":
    urls = [
        "file:///Users/kangkanpatowary/Downloads/async_web_crawler/index.html"  # Adjust the path to your HTML file
    ]
    asyncio.run(crawl_and_save(urls, output_file="crawled_headlines.json"))
