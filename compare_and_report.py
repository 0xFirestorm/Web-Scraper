import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from jj_scraper.firebase_config import COLLECTIONS
from jj_scraper.spiders.kameez_shalwar_spider import KameezShalwarSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import sys
import time

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_firestore_products():
    # Initialize Firebase Admin SDK
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate('firebase-credentials.json')
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    # Get all products from Firebase
    products_ref = db.collection(COLLECTIONS['products'])
    products = products_ref.stream()
    
    # Convert to dictionary with product_id as key
    return {doc.id: doc.to_dict() for doc in products}

def format_price(price_str):
    """Convert price string to float, handling PKR and comma formatting."""
    try:
        # Remove PKR, commas, and whitespace, then convert to float
        return float(price_str.replace('PKR', '').replace(',', '').strip())
    except (ValueError, AttributeError):
        return 0.0

def compare_and_generate_report():
    # First get existing data from Firestore
    firestore_products = get_firestore_products()
    if not firestore_products:
        print("No existing data found in Firestore")
        return

    # Run the scraper to get current website data
    process = CrawlerProcess(get_project_settings())
    process.crawl(KameezShalwarSpider)
    process.start()

    # Wait a bit for the scraper to finish and save data
    time.sleep(5)

    # Get the current data from Firestore (after scraper has updated it)
    current_products = get_firestore_products()
    if not current_products:
        print("No current data found in Firestore")
        return

    # Initialize lists for changes
    new_ids = []
    removed_ids = []
    out_of_stock_ids = []
    price_increased_ids = []
    price_decreased_ids = []

    # Find new and removed products
    current_ids = set(current_products.keys())
    previous_ids = set(firestore_products.keys())
    
    new_ids = list(current_ids - previous_ids)
    removed_ids = list(previous_ids - current_ids)

    # Compare existing products for changes
    for prod_id, product in current_products.items():
        if prod_id in firestore_products:
            prev_product = firestore_products[prod_id]
            
            # Check stock status
            if product['availability'] == 'Out of Stock' and prev_product['availability'] != 'Out of Stock':
                out_of_stock_ids.append(prod_id)
            
            # Compare prices
            try:
                old_price = format_price(prev_product['price'])
                new_price = format_price(product['price'])
                
                if new_price > old_price:
                    price_increased_ids.append(prod_id)
                elif new_price < old_price:
                    price_decreased_ids.append(prod_id)
            except (ValueError, AttributeError) as e:
                print(f"Error comparing prices for product {prod_id}: {e}")

    # Generate report
    report = {
        'Products scraped': len(current_products),
        'New products': len(new_ids),
        'New product IDs': new_ids,
        'Removed products': len(removed_ids),
        'Removed product IDs': removed_ids,
        'Out-of-stock products': len(out_of_stock_ids),
        'Out-of-stock product IDs': out_of_stock_ids,
        'Price increased': len(price_increased_ids),
        'Price increased IDs': price_increased_ids,
        'Price decreased': len(price_decreased_ids),
        'Price decreased IDs': price_decreased_ids
    }

    # Save report to Firestore
    db = firestore.client()
    timestamp = datetime.now()
    report_ref = db.collection('reports').document(timestamp.strftime('%Y%m%d_%H%M%S'))
    report['timestamp'] = timestamp
    report_ref.set(report)

    # Print report
    print("\nComparison Report:")
    print(f"Products scraped: {report['Products scraped']}")
    print(f"New products: {report['New products']}")
    print(f"→ Product IDs: {report['New product IDs']}")
    print(f"Removed products: {report['Removed products']}")
    print(f"→ Product IDs: {report['Removed product IDs']}")
    print(f"Out-of-stock products: {report['Out-of-stock products']}")
    print(f"→ Product IDs: {report['Out-of-stock product IDs']}")
    print(f"Price increased: {report['Price increased']}")
    print(f"→ Product IDs: {report['Price increased IDs']}")
    print(f"Price decreased: {report['Price decreased']}")
    print(f"→ Product IDs: {report['Price decreased IDs']}")
    
    print(f"\nReport saved to Firestore with ID: {report_ref.id}")

if __name__ == '__main__':
    compare_and_generate_report()
