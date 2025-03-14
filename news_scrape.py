import os
import asyncio
from dotenv import load_dotenv
from newsapi.newsapi_client import NewsApiClient
from crawl4ai import AsyncWebCrawler,CrawlerRunConfig,BrowserConfig



# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Initialize NewsAPI client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# File path for storing scraped news
raw_output_file = "zomato.txt"

# Fetch Amazon-related news
articles = newsapi.get_everything(
    # q="(microsoft OR MSFT OR MICROSOFT )AND (stock OR shares OR earnings OR gains OR losses)",  # Modify based on your topic of interest
    q=("(HAL OR Hindustan Aeronautics Limited ) "),
    domains= "finance.yahoo.com,bloomberg.com,cnbc.com,marketwatch.com,"
        "forbes.com,investing.com,reuters.com,economictimes.indiatimes.com,"
        "moneycontrol.com,financialexpress.com,investopedia.com,nasdaq.com,"
        "fool.com,tradingview.com,nerdwallet.com,business-standard.com",
    # domains="finance.yahoo.com,bloomberg.com,cnbc.com,marketwatch.com,forbes.com,investing.com,reuters.com,economictimes.indiatimes.com",  # Ensure Yahoo Finance is included
    from_param="2025-02-17",
    to="2025-03-13",
    sort_by="relevancy",
    language="en",
    page_size=5
)
browser_config = BrowserConfig(
    headless=True,
    use_managed_browser=True  # Required for async operations
)

# 2. CrawlerRunConfig without browser_config
config = CrawlerRunConfig(
    word_count_threshold=50,
    exclude_external_links=True,
    exclude_internal_links=True,
    exclude_social_media_links=True,
    excluded_tags=['form', 'header', 'footer', 'nav'],
    exclude_social_media_domains=["facebook.com", "twitter.com"]
)

async def scrape_and_save():
    """Scrapes Amazon news articles and saves them to a text file."""
    async with AsyncWebCrawler(config=browser_config) as crawler:
        with open(raw_output_file, "w", encoding="utf-8") as file:
            for article in articles["articles"]:
                title = article["title"]
                url = article["url"]

                try:
                    result = await crawler.arun(url=url,config=config)
                    content = result.markdown  # Extract scraped content in markdown format

                    file.write(f"### {title}\n\n")
                    file.write(content + "\n\n" + "=" * 80 + "\n\n")

                    print(f"Scraped: {title}")

                except Exception as e:
                    print(f"Failed to scrape {title}: {e}")

# Run the scraping function
asyncio.run(scrape_and_save())

print(f"Scraped news saved to {raw_output_file}")
