import json
import os
from typing import List, Set, Tuple

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)

from models.venue import Venue
from utils.data_utils import is_complete_venue, is_duplicate_venue
from models.locations import Locations



def get_browser_config() -> BrowserConfig:
    """
    Returns the browser configuration for the crawler.

    Returns:
        BrowserConfig: The configuration settings for the browser.
    """
    # https://docs.crawl4ai.com/core/browser-crawler-config/
    return BrowserConfig(
        browser_type="chromium",  
        headless=False,  
        verbose=True,  
    )


def get_llm_strategy() -> LLMExtractionStrategy:
    """
    Retorna a configuração para a estratégia de extração do modelo de linguagem.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("A chave de API da OpenAI não foi encontrada. Defina OPENAI_API_KEY no arquivo .env.")

    return LLMExtractionStrategy(
        provider="openai/gpt-4o-mini",  
        api_token=api_key,  
        schema=Locations.model_json_schema(),  
        extraction_type="schema",  
        instruction=(
            "Extraia todos os locais na região "
            "Para cada card de localização, forneça: "
            "- Nome do local "
            "- Avaliação "
            "- Número de avaliações "
            "- Endereço "
            "- Horário de funcionamento "
            "- Telefone "
            "Foque apenas nos resultados de comparação de preços."
        ),  
        input_format="markdown",  
        verbose=True,  
    )


async def check_no_results(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
) -> bool:
    """
    Checks if the "No Results Found" message is present on the page.

    Args:
        crawler (AsyncWebCrawler): The web crawler instance.
        url (str): The URL to check.
        session_id (str): The session identifier.

    Returns:
        bool: True if "No Results Found" message is found, False otherwise.
    """
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            session_id=session_id,
        ),
    )

    if result.success:
        if "No Results Found" in result.cleaned_html:
            return True
    else:
        print(
            f"Error fetching page for 'No Results Found' check: {result.error_message}"
        )

    return False


async def fetch_and_process_page(
    crawler: AsyncWebCrawler,
    page_number: int,
    base_url: str,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
    required_keys: List[str],
    seen_names: Set[str],
) -> Tuple[List[dict], bool]:
    """
    Fetches and processes a single page of venue data.

    Args:
        crawler (AsyncWebCrawler): The web crawler instance.
        page_number (int): The page number to fetch.
        base_url (str): The base URL of the website.
        css_selector (str): The CSS selector to target the content.
        llm_strategy (LLMExtractionStrategy): The LLM extraction strategy.
        session_id (str): The session identifier.
        required_keys (List[str]): List of required keys in the venue data.
        seen_names (Set[str]): Set of venue names that have already been seen.

    Returns:
        Tuple[List[dict], bool]:
            - List[dict]: A list of processed venues from the page.
            - bool: A flag indicating if the "No Results Found" message was encountered.
    """
    url = f"{base_url}?page={page_number}"
    print(f"Loading page {page_number}...")

    # Check if "No Results Found" message is present
    no_results = await check_no_results(crawler, url, session_id)
    if no_results:
        return [], True  # No more results, signal to stop crawling

    # Fetch page content with the extraction strategy
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Do not use cached data
            extraction_strategy=llm_strategy,  # Strategy for data extraction
            css_selector=css_selector,  # Target specific content on the page
            session_id=session_id,  # Unique session ID for the crawl
        ),
    )

    if not (result.success and result.extracted_content):
        print(f"Error fetching page {page_number}: {result.error_message}")
        return [], False

    # Parse extracted content
    extracted_data = json.loads(result.extracted_content)
    if not extracted_data:
        print(f"No venues found on page {page_number}.")
        return [], False

    # After parsing extracted content
    print("Extracted data:", extracted_data)

    # Process venues
    complete_venues = []
    for venue in extracted_data:
        # Debugging: Print each venue to understand its structure
        print("Processing venue:", venue)

        # Ignore the 'error' key if it's False
        if venue.get("error") is False:
            venue.pop("error", None)  # Remove the 'error' key if it's False

        if not is_complete_venue(venue, required_keys):
            continue  # Skip incomplete venues

        if is_duplicate_venue(venue["name"], seen_names):
            print(f"Duplicate venue '{venue['name']}' found. Skipping.")
            continue  # Skip duplicate venues

        # Add venue to the list
        seen_names.add(venue["name"])
        complete_venues.append(venue)

    if not complete_venues:
        print(f"No complete venues found on page {page_number}.")
        return [], False

    print(f"Extracted {len(complete_venues)} venues from page {page_number}.")
    return complete_venues, False  # Continue crawling
