# Real Estate Address Tracker

A Django application for tracking addresses and scraping property information from Australian real estate websites.

## Features

- Store and manage addresses with street, suburb, and state information
- Web scraping integration with domain.com.au and realestate.com.au
- Automatic property status detection (for sale, auction, sold)
- Price information extraction
- Inspection and auction date tracking

## Installation

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run database migrations:
   ```bash
   python manage.py migrate
   ```

## Usage

### Adding Addresses

1. Navigate to the addresses page
2. Use the form to add new addresses
3. Support for various input formats:
   - Tab-separated: "14 Weil Avenue	Croydon Park"
   - Comma-separated: "3a King Edward Street, Croydon"
   - Space-separated: "14 Weil Avenue Croydon Park"

### Scraping Property Information

1. For each address, click the "Scrape" button
2. The system will search both domain.com.au and realestate.com.au
3. Property information will be displayed in the table

### Property Information Displayed

For properties currently for sale:
- Sale type (auction or private sale)
- Price information (actual price, price guide, or "contact agent")
- Next inspection date (if available)
- Auction date (if applicable)

For properties not for sale:
- Last sale price (if available)

## Technical Notes

### Web Scraping Implementation

The scraping functionality uses:
- `requests` for HTTP requests
- `BeautifulSoup` with `lxml` parser for HTML parsing
- Basic regex patterns for data extraction

### Limitations

- Basic HTML parsing (no JavaScript rendering)
- May not work with all properties
- Website structure changes can break scraping
- No handling of anti-scraping measures
- Simplified date parsing

### Production Considerations

For production use, consider:
- Using official real estate APIs
- Implementing Selenium for JavaScript-heavy sites
- Adding rate limiting and respectful scraping practices
- Using proxy services for large-scale scraping
- Implementing proper error handling and retries

## API Endpoints

- `GET/POST /addresses/` - List and create addresses
- `POST /addresses/delete/<id>/` - Delete an address
- `POST /addresses/scrape/<id>/` - Scrape property info for an address

## Models

### Address
- `street_address`: Property street address
- `suburb`: Suburb name
- `state`: State (defaults to configured default)
- `created_at`: Creation timestamp

### PropertyInfo
- `address`: Foreign key to Address
- `is_for_sale`: Boolean indicating if property is for sale
- `sale_type`: "auction" or "sale"
- `price_info`: Price, guide, or contact agent text
- `next_inspection`: Next inspection datetime
- `auction_date`: Auction datetime
- `last_sale_price`: Last sale price text
- `scraped_at`: Last scraping timestamp
- `source_domain`: Website source (domain.com.au or realestate.com.au)