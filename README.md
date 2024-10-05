# WebCrawler.AI

## Overview

This documentation provides an overview of using the **Async Web Crawler**, which leverages **Playwright** and **aiohttp** to scrape data from dynamic websites asynchronously. The crawler can execute JavaScript, filter data with CSS selectors, and extract structured data efficiently.

## Table of Contents

- [First Steps](#first-steps)
- [Introduction](#introduction)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Examples](#examples)
  - [JS Execution & CSS Filtering](#js-execution--css-filtering)
  - [Extracting Structured Data Asynchronously](#extracting-structured-data-asynchronously)
  - [Advanced Usage](#advanced-usage)
- [Try It Yourself](#try-it-yourself)
- [License](#license)

## First Steps

### Introduction

The Async Web Crawler is designed to handle complex web interactions and extract meaningful data asynchronously. It supports executing JavaScript, which is essential for interacting with dynamic web content.

### Installation

To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-username/async-web-crawler.git
cd async-web-crawler
python3 -m venv venv
source venv/bin/activate  # For Windows use `venv\Scripts\activate`
pip install aiohttp beautifulsoup4 lxml nest_asyncio playwright
playwright install

Quick Start
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://www.example.com")
        print(result.extracted_content)

asyncio.run(main())


import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.chunking_strategy import RegexChunking
from crawl4ai.extraction_strategy import CosineStrategy

async def main():
    # Define the JavaScript code to click the "Load More" button
    js_code = """
    const loadMoreButton = Array.from(document.querySelectorAll('button')).find(button => button.textContent.includes('Load More'));
    if (loadMoreButton) {
        loadMoreButton.click();
        // Wait for new content to load
        await new Promise(resolve => setTimeout(resolve, 2000));
    }
    """

    # Define a wait_for function to ensure content is loaded
    wait_for = """
    () => {
        const articles = document.querySelectorAll('article.tease-card');
        return articles.length > 10;
    }
    """

    async with AsyncWebCrawler(verbose=True) as crawler:
        # Run the crawler with keyword filtering and CSS selector
        result = await crawler.arun(
            url="https://www.nbcnews.com/business",
            js_code=js_code,
            wait_for=wait_for,
            css_selector="article.tease-card",
            extraction_strategy=CosineStrategy(semantic_filter="technology"),
            chunking_strategy=RegexChunking(),
        )

    # Display the extracted result
    print(result.extracted_content)

# Run the async function
asyncio.run(main())
Asynchronous Execution: We use AsyncWebCrawler with async/await syntax for non-blocking execution.
JavaScript Execution: The js_code variable simulates clicking a "Load More" button.
Wait Condition: The wait_for function checks that more than 10 articles have loaded before extraction.
CSS Selector: The css_selector="article.tease-card" parameter filters to ensure only relevant articles are extracted.
Extraction Strategy: The CosineStrategy filters content semantically based on "technology."
Chunking Strategy: RegexChunking() splits the content into manageable chunks.



Advanced Usage: Custom Session and Multiple Requests

async def advanced_crawl():
    async with AsyncWebCrawler(verbose=True) as crawler:
        # Initial crawl with custom session
        result1 = await crawler.arun(
            url="https://www.nbcnews.com/business",
            js_code=js_code,
            wait_for=wait_for,
            css_selector="article.tease-card",
            session_id="business_session"
        )

        # Execute additional JavaScript in the same session
        result2 = await crawler.crawler_strategy.execute_js(
            session_id="business_session",
            js_code="window.scrollTo(0, document.body.scrollHeight);",
            wait_for_js="() => window.innerHeight + window.scrollY >= document.body.offsetHeight"
        )

        # Process results
        print("Initial crawl result:", result1.extracted_content)
        print("Additional JS execution result:", result2.html)

# Run the advanced crawl function
asyncio.run(advanced_crawl())
#### Try It Yourself


Here’s a README-style documentation for your Async Web Crawler project, incorporating the content you've provided. This documentation outlines the functionality, usage, and advanced features of the crawler.

README.md
markdown
Copy code
# Async Web Crawler Documentation

## Overview

This documentation provides an overview of using the **Async Web Crawler**, which leverages **Playwright** and **aiohttp** to scrape data from dynamic websites asynchronously. The crawler can execute JavaScript, filter data with CSS selectors, and extract structured data efficiently.

## Table of Contents

- [First Steps](#first-steps)
- [Introduction](#introduction)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Examples](#examples)
  - [JS Execution & CSS Filtering](#js-execution--css-filtering)
  - [Extracting Structured Data Asynchronously](#extracting-structured-data-asynchronously)
  - [Advanced Usage](#advanced-usage)
- [Try It Yourself](#try-it-yourself)
- [License](#license)

## First Steps

### Introduction

The Async Web Crawler is designed to handle complex web interactions and extract meaningful data asynchronously. It supports executing JavaScript, which is essential for interacting with dynamic web content.

### Installation

To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-username/async-web-crawler.git
cd async-web-crawler
python3 -m venv venv
source venv/bin/activate  # For Windows use `venv\Scripts\activate`
pip install aiohttp beautifulsoup4 lxml nest_asyncio playwright
playwright install
Quick Start
Here’s a simple example of how to use the Async Web Crawler:

python
Copy code
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://www.example.com")
        print(result.extracted_content)

asyncio.run(main())
Examples
JS Execution & CSS Filtering
In this example, we'll demonstrate how to use AsyncWebCrawler to execute JavaScript and filter data with CSS selectors. This approach is useful for interacting with dynamic content, such as clicking "Load More" buttons.

Example: Extracting Structured Data Asynchronously
python
Copy code
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.chunking_strategy import RegexChunking
from crawl4ai.extraction_strategy import CosineStrategy

async def main():
    # Define the JavaScript code to click the "Load More" button
    js_code = """
    const loadMoreButton = Array.from(document.querySelectorAll('button')).find(button => button.textContent.includes('Load More'));
    if (loadMoreButton) {
        loadMoreButton.click();
        // Wait for new content to load
        await new Promise(resolve => setTimeout(resolve, 2000));
    }
    """

    # Define a wait_for function to ensure content is loaded
    wait_for = """
    () => {
        const articles = document.querySelectorAll('article.tease-card');
        return articles.length > 10;
    }
    """

    async with AsyncWebCrawler(verbose=True) as crawler:
        # Run the crawler with keyword filtering and CSS selector
        result = await crawler.arun(
            url="https://www.nbcnews.com/business",
            js_code=js_code,
            wait_for=wait_for,
            css_selector="article.tease-card",
            extraction_strategy=CosineStrategy(semantic_filter="technology"),
            chunking_strategy=RegexChunking(),
        )

    # Display the extracted result
    print(result.extracted_content)

# Run the async function
asyncio.run(main())
Explanation
Asynchronous Execution: We use AsyncWebCrawler with async/await syntax for non-blocking execution.
JavaScript Execution: The js_code variable simulates clicking a "Load More" button.
Wait Condition: The wait_for function checks that more than 10 articles have loaded before extraction.
CSS Selector: The css_selector="article.tease-card" parameter filters to ensure only relevant articles are extracted.
Extraction Strategy: The CosineStrategy filters content semantically based on "technology."
Chunking Strategy: RegexChunking() splits the content into manageable chunks.
Advanced Usage: Custom Session and Multiple Requests
For scenarios where you need to maintain state across requests or execute additional JavaScript:

python
Copy code
async def advanced_crawl():
    async with AsyncWebCrawler(verbose=True) as crawler:
        # Initial crawl with custom session
        result1 = await crawler.arun(
            url="https://www.nbcnews.com/business",
            js_code=js_code,
            wait_for=wait_for,
            css_selector="article.tease-card",
            session_id="business_session"
        )

        # Execute additional JavaScript in the same session
        result2 = await crawler.crawler_strategy.execute_js(
            session_id="business_session",
            js_code="window.scrollTo(0, document.body.scrollHeight);",
            wait_for_js="() => window.innerHeight + window.scrollY >= document.body.offsetHeight"
        )

        # Process results
        print("Initial crawl result:", result1.extracted_content)
        print("Additional JS execution result:", result2.html)

# Run the advanced crawl function
asyncio.run(advanced_crawl())
Explanation
Custom Session: Maintains state across requests, allowing for complex interactions.
Additional JavaScript Execution: Executes more JavaScript after the initial page load.
Waiting for Conditions: Ensures that specific conditions are met using JavaScript functions.
Try It Yourself
These examples demonstrate the power and flexibility of the AsyncWebCrawler in handling complex web interactions. Customize the JavaScript code, CSS selectors, extraction strategies, and waiting conditions to suit your specific requirements.

License
This project is licensed under the MIT License - see the LICENSE file for details.
**Author**
Your Name - Kangkan patowary
Your Email - kangkanpatowary18@gmail.com
Your GitHub Profile -


### Customization Instructions

1. **Replace `your-username`**: Update all instances of `your-username` with your actual GitHub username.
2. **Author Information**: Fill in your name and email in the author section.
3. **URL Links**: If applicable, update links to point to your documentation or other resources.

### How to Use

1. Create a file named `README.md` in the root directory of your project.
2. Copy and paste the above content into the file.
3. Save the changes.

This documentation provides users with a comprehensive understanding of how to use your crawler, including setup, examples, and advanced usage scenarios. Let me know if you need further modifications or additions!
