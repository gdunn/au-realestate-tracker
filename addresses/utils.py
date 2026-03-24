"""
Real Estate Web Scraping Utilities

This module provides functionality to scrape property information from Australian real estate websites.

IMPORTANT NOTES:
- This is a basic implementation that may not work with all properties or handle all edge cases
- Real estate websites often use JavaScript rendering, anti-scraping measures, and change their HTML structure frequently
- For production use, consider using official APIs, Selenium for JavaScript rendering, or services like Bright Data
- Always respect website terms of service and robots.txt files
- The current implementation uses basic HTML parsing and may miss dynamically loaded content

Current limitations:
- No JavaScript rendering support
- Basic HTML selectors that may break with site changes
- Simplified date/time parsing
- No handling of CAPTCHAs or rate limiting
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from urllib.parse import quote
from .models import PropertyInfo


class RealEstateScraper:
    """Scraper for Australian real estate websites."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def _clean_text(self, text):
        """Clean and normalize text."""
        if not text:
            return ""
        return re.sub(r"\s+", " ", text.strip())

    def search_domain_com_au(self, address):
        """Search domain.com.au for property information."""
        try:
            direct_url = self.find_first_live_property_url(address)
            if direct_url and "domain.com.au" in direct_url:
                response = self.session.get(direct_url, timeout=15)
            else:
                # Create search query fallback
                full_address = (
                    f"{address.street_address} {address.suburb} {address.state}"
                )
                search_query = quote(full_address)
                url = f"https://www.domain.com.au/search/?searchTerm={search_query}"
                response = self.session.get(url, timeout=15)

            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            property_info = {
                "is_for_sale": False,
                "sale_type": "",
                "price_info": "",
                "next_inspection": None,
                "auction_date": None,
                "last_sale_price": "",
                "source_domain": "domain.com.au",
            }

            # Look for property listings - these selectors would need to be updated based on actual site structure
            listings = soup.find_all("div", class_=re.compile(r"listing|property"))

            for listing in listings:
                # Check if this listing matches our address (simplified check)
                address_text = listing.get_text().lower()
                if (
                    address.street_address.lower() in address_text
                    and address.suburb.lower() in address_text
                ):

                    # Check for sale status
                    sale_text = listing.get_text()
                    if re.search(r"for sale|auction", sale_text, re.I):
                        property_info["is_for_sale"] = True
                        if "auction" in sale_text.lower():
                            property_info["sale_type"] = "auction"
                        else:
                            property_info["sale_type"] = "sale"

                        # Extract price
                        price_match = re.search(r"\$[\d,]+(?:\.\d{2})?", sale_text)
                        if price_match:
                            property_info["price_info"] = price_match.group()
                        elif "contact agent" in sale_text.lower():
                            property_info["price_info"] = "Contact Agent"
                        elif "price guide" in sale_text.lower():
                            property_info["price_info"] = "Price Guide"

                        # Look for inspection times (simplified)
                        inspection_match = re.search(
                            r"inspection.*?(\d{1,2}/\d{1,2}/\d{4})", sale_text, re.I
                        )
                        if inspection_match:
                            # This would need proper date parsing
                            property_info["next_inspection"] = datetime.now()

                        # Look for auction dates
                        auction_match = re.search(
                            r"auction.*?(\d{1,2}/\d{1,2}/\d{4})", sale_text, re.I
                        )
                        if auction_match:
                            property_info["auction_date"] = datetime.now()

                        break

            # If no current listing found, check for sold properties
            if not property_info["is_for_sale"]:
                sold_text = soup.get_text()
                sold_match = re.search(r"sold.*?\$[\d,]+", sold_text, re.I)
                if sold_match:
                    property_info["last_sale_price"] = sold_match.group()

            return property_info

        except Exception as e:
            print(f"Error scraping domain.com.au: {e}")
            return None

    def search_realestate_com_au(self, address):
        """Search realestate.com.au for property information."""
        try:
            direct_url = self.find_first_live_property_url(address)
            if direct_url and "realestate.com.au" in direct_url:
                response = self.session.get(direct_url, timeout=15)
            else:
                # Create search query fallback
                suburb_formatted = address.suburb.lower().replace(" ", "-")
                url = f"https://www.realestate.com.au/buy/in-{suburb_formatted}/"
                response = self.session.get(url, timeout=15)

            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            property_info = {
                "is_for_sale": False,
                "sale_type": "",
                "price_info": "",
                "next_inspection": None,
                "auction_date": None,
                "last_sale_price": "",
                "source_domain": "realestate.com.au",
            }

            # Similar logic for realestate.com.au
            # This would need customization based on their HTML structure
            page_text = soup.get_text()

            # Check for our specific address
            if (
                address.street_address.lower() in page_text.lower()
                and address.suburb.lower() in page_text.lower()
            ):
                if re.search(r"for sale|auction", page_text, re.I):
                    property_info["is_for_sale"] = True
                    # Additional parsing logic would go here

            return property_info

        except Exception as e:
            print(f"Error scraping realestate.com.au: {e}")
            return None

    def _slugify_address(self, address):
        """Create a normalized slug for address-based direct property URLs."""
        pa = (
            f"{address.street_address} {address.suburb} {address.state}".strip().lower()
        )
        pa = re.sub(r"[^a-z0-9\s]", "", pa)  # remove punctuation
        pa = re.sub(r"\s+", " ", pa).strip()
        return pa.replace(" ", "-")

    def get_domain_property_url(self, address, postcode=None):
        """Return the domain.com.au direct URL by slug; optionally add postcode."""
        slug = self._slugify_address(address)
        if postcode:
            return f"https://www.domain.com.au/{slug}-{postcode}"
        return f"https://www.domain.com.au/{slug}"

    def get_realestate_property_url(self, address, postcode=None):
        """Return the realestate.com.au direct URL by slug (property path) optionally with postcode."""
        slug = self._slugify_address(address)
        if postcode:
            slug = f"{slug}-{postcode}"
        return f"https://www.realestate.com.au/property/{slug}/"

    def get_candidate_property_urls(self, address):
        """Return a list of candidate property URLs for a given address."""
        candidate_postcodes = []
        lookup_suburb = address.suburb.strip().lower() if address.suburb else ""

        postcode_map = {
            "earlwood": "2206",
            # add more suburb->postcode as needed for reliability
        }

        if address.__dict__.get("postcode"):
            candidate_postcodes.append(address.postcode.strip())

        if lookup_suburb in postcode_map:
            candidate_postcodes.append(postcode_map[lookup_suburb])

        # dedupe and sanitize
        candidate_postcodes = [p for p in dict.fromkeys(candidate_postcodes) if p]

        urls = [
            self.get_domain_property_url(address),
            self.get_realestate_property_url(address),
        ]

        for pc in candidate_postcodes:
            urls.append(self.get_domain_property_url(address, pc))
            urls.append(self.get_realestate_property_url(address, pc))

        return urls

    def find_first_live_property_url(self, address):
        """Get first URL that responds with 200 OK from candidate property URLs."""
        candidates = self.get_candidate_property_urls(address)
        for url in candidates:
            try:
                resp = self.session.head(url, timeout=8, allow_redirects=True)
            except Exception:
                continue
            if resp.status_code == 200:
                return url

            if resp.status_code in (405, 403, 404):
                # If HEAD is not allowed or forbidden, fallback to GET for detail check.
                try:
                    resp_get = self.session.get(url, timeout=8, allow_redirects=True)
                except Exception:
                    continue
                if resp_get.status_code == 200:
                    return url

        return None

    def scrape_property_info(self, address):
        """Scrape property information from both websites."""
        results = []

        # Scrape domain.com.au
        domain_info = self.search_domain_com_au(address)
        if domain_info:
            results.append(domain_info)

        # Scrape realestate.com.au
        rea_info = self.search_realestate_com_au(address)
        if rea_info:
            results.append(rea_info)

        return results


def update_property_info(address):
    """Update property information for an address."""
    scraper = RealEstateScraper()
    results = scraper.scrape_property_info(address)

    # Save results to database
    for result in results:
        PropertyInfo.objects.update_or_create(
            address=address, source_domain=result["source_domain"], defaults=result
        )

    return results
