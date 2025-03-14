import os
import asyncio
from dotenv import load_dotenv
from newsapi.newsapi_client import NewsApiClient
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator  # NEW IMPORT

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY_2")

# Initialize NewsAPI client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# File path for storing scraped news
raw_output_file = "yahoo_amazon_news.txt"

# Fetch Amazon-related news
articles = newsapi.get_everything(
    q="AMAZON OR AMZN OR stock market OR investing OR finance",
    domains="finance.yahoo.com,bloomberg.com,cnbc.com,marketwatch.com,forbes.com,investing.com,reuters.com,economictimes.india.com",
    from_param="2025-03-01",
    sort_by="publishedAt",
    language="en",
    page_size=2
)

async def scrape_and_save():
    """Scrapes Amazon news articles and saves them to a text file."""
    # Configure link removal settings [1][2][4]
    md_generator = DefaultMarkdownGenerator(
        options={"ignore_links": True}  # Remove markdown link syntax
    )
    
    crawler_config = CrawlerRunConfig(
        markdown_generator=md_generator,
        excluded_tags=["a"],  # Remove anchor tags from HTML
        # exclude_external_links=True  # Optional: Remove external links
    )

    async with AsyncWebCrawler() as crawler:
        with open(raw_output_file, "w", encoding="utf-8") as file:
            for article in articles["articles"]:
                title = article["title"]
                url = article["url"]

                try:
                    result = await crawler.arun(url=url, config=crawler_config)
                    # Use result.text instead of markdown for clean text [2][4]
                    content = result.text  
                    
                    file.write(f"### {title}\n\n")
                    file.write(content + "\n\n" + "=" * 80 + "\n\n")
                    print(f"Scraped: {title}")

                except Exception as e:
                    print(f"Failed to scrape {title}: {e}")

# Run the scraping function
asyncio.run(scrape_and_save())
print(f"Scraped news saved to {raw_output_file}")
