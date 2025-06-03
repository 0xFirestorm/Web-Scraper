# J. Scraper

This  scraper was made as an assignment for a job screening.
A web scraper for J.'s website that tracks product changes and generates comparison reports.

## Features

- Scrapes product data from JJ's website
- Stores data in Firebase Firestore
- Generates comparison reports showing:
  - New products
  - Removed products
  - Out-of-stock products
  - Price changes (increases/decreases)

## Development Approach

### 1. Scraping Strategy
- Used Scrapy framework for efficient web scraping
- Implemented dynamic pagination handling to navigate through all product pages
- Added robust error handling and logging for debugging
- Used CSS selectors for reliable data extraction
- Implemented rate limiting to avoid overwhelming the server

### 2. Comparison Logic
- Implemented a two-phase comparison:
  1. Get existing data from Firestore
  2. Run scraper to get current website data
  3. Compare both datasets to identify:
     - New products (in current but not in existing)
     - Removed products (in existing but not in current)
     - Price changes (comparing formatted prices)
     - Stock status changes (tracking availability)
- Used set operations for efficient comparison
- Implemented proper price formatting to handle currency symbols and commas

### 3. Report Generation
- Created a structured report format with:
  - Summary counts for each type of change
  - Detailed lists of affected product IDs
  - Timestamp for tracking when the comparison was made
- Stored reports in Firestore for historical tracking
- Implemented console output for immediate visibility

## Project Structure

```
jj_scraper/
├── jj_scraper/
│   ├── spiders/
│   │   └── kameez_shalwar_spider.py    # Main scraper
│   ├── pipelines/
│   │   └── firebase_pipeline.py        # Firebase data storage
│   ├── firebase_config.py              # Firebase configuration
│   └── settings.py                     # Scrapy settings
├── compare_and_report.py               # Comparison and reporting script
├── firebase-credentials.json           # Firebase credentials
├── scrapy.cfg                          # Scrapy configuration
└── requirements.txt                    # Project dependencies
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Firebase:
   - Create a Firebase project
   - Download your service account credentials
   - Save as `firebase-credentials.json` in the project root

## Usage

1. Run the scraper:
```bash
scrapy crawl kameez_shalwar
```

2. Generate comparison report:
```bash
python compare_and_report.py
```

The report will show:
- Total products scraped
- New products with their IDs
- Removed products with their IDs
- Out-of-stock products with their IDs
- Products with price increases/decreases

## Output Format

```
Comparison Report:
Products scraped: 331
New products: 1
→ Product IDs: ['123456']
Removed products: 0
→ Product IDs: []
Out-of-stock products: 0
→ Product IDs: []
Price increased: 1
→ Product IDs: ['789012']
Price decreased: 0
→ Product IDs: []
```

## Dependencies

- Scrapy: Web scraping framework
- Firebase Admin SDK: Firebase integration
- Python-dotenv: Environment variable management 