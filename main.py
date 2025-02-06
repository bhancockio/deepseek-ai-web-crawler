import asyncio

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from models.price import DivGooglePrices
from utils.data_utils import (
    save_venues_to_csv,
)
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()


async def crawl_venues():
    """
    Main function to crawl venue data from the website.
    """
    # Initialize configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "price_crawl_session"

    # Initialize state variables
    all_venues = []
    seen_names = set()

    # Start the web crawler context
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Fetch and process data from the page
        venues, no_results_found = await fetch_and_process_page(
            crawler,
            1,  # Always first page
            BASE_URL,
            CSS_SELECTOR,
            llm_strategy,
            session_id,
            REQUIRED_KEYS,
            seen_names,
        )

        if no_results_found or not venues:
            print("No venues found.")
            return

        # Add the venues to the total list
        all_venues.extend(venues)

    # Save the collected venues to a CSV file
    if all_venues:
        save_venues_to_csv(all_venues, "complete_venues.csv")
        print(f"Saved {len(all_venues)} venues to 'complete_venues.csv'.")
    else:
        print("No venues were found during the crawl.")

    # Display usage statistics for the LLM strategy
    llm_strategy.show_usage()


async def main():
    """
    Entry point of the script.
    """
    await crawl_venues()


if __name__ == "__main__":
    asyncio.run(main())
