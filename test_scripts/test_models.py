#!/usr/bin/env python
"""
Simple test to check if the models can be imported and basic functionality works.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestatetracker.settings")

# Setup Django
django.setup()

try:
    from addresses.models import Address, AddressConfig, PropertyInfo

    print("✓ Models imported successfully")

    # Test creating objects
    addr = Address(street_address="Test St", suburb="Test Suburb", state="NSW")
    print("✓ Address object created")

    # Test PropertyInfo
    info = PropertyInfo(
        address=addr, is_for_sale=True, sale_type="auction", source_domain="test.com"
    )
    print("✓ PropertyInfo object created")

    print("All basic tests passed!")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback

    traceback.print_exc()
