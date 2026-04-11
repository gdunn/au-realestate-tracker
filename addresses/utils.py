import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin

logger = logging.getLogger(__name__)


class PropertyURLFinder:
    """Simple utility to find property URLs on realestate.com.au."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def get_realestate_search_url(self, address):
        """Build the realestate.com.au search page URL for an address."""
        encoded = quote_plus(address)
        return f"https://www.realestate.com.au/buy/in-{encoded}/list-1?activeSort=list-date"

    def parse_realestate_search_results(self, html):
        """Parse realestate.com.au search HTML and return property detail URLs."""
        soup = BeautifulSoup(html, "html.parser")
        urls = []

        for anchor in soup.select('a.details-link[href^="/property-"]'):
            href = anchor.get("href", "").strip()
            if not href:
                continue
            absolute_url = urljoin("https://www.realestate.com.au", href)
            if absolute_url not in urls:
                urls.append(absolute_url)

        logger.debug(
            "Parsed %d property URLs from search HTML: %s",
            len(urls),
            urls[:10],
        )
        return urls

    def find_property_urls(self, address):
        """Find property URLs for an address by scraping realestate.com.au search results."""
        search_url = self.get_realestate_search_url(address)
        logger.info("Searching realestate.com.au for address %s", address)
        logger.debug("Realestate search URL: %s", search_url)

        try:
            response = self.session.get(search_url, timeout=10)
            logger.debug(
                "Received response for search URL %s with status %s",
                search_url,
                response.status_code,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.exception(
                "Failed to fetch realestate search page for %s: %s",
                address,
                exc,
            )
            return []

        urls = self.parse_realestate_search_results(response.text)
        logger.info(
            "Found %d property URLs for address %s",
            len(urls),
            address,
        )
        return urls
