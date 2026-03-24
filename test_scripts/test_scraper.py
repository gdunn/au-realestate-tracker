#!/usr/bin/env python
"""
Simple test script to verify the scraping functionality works.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestatetracker.settings")

# Setup Django
django.setup()

from addresses.models import Address
from addresses.utils import RealEstateScraper, update_property_info


def test_scraper():
    """Test the scraper with a sample address."""
    print("Testing RealEstateScraper...")

    # Create a test address
    test_address = Address(
        street_address="14 Weil Avenue", suburb="Croydon Park", state="NSW"
    )

    scraper = RealEstateScraper()

    print("Testing domain.com.au scraping...")
    domain_result = scraper.search_domain_com_au(test_address)
    print(f"Domain result: {domain_result}")

    print("Testing realestate.com.au scraping...")
    rea_result = scraper.search_realestate_com_au(test_address)
    print(f"REA result: {rea_result}")

    print("Test completed!")


if __name__ == "__main__":
    test_scraper()
