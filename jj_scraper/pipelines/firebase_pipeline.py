import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from ..firebase_config import COLLECTIONS
import logging

class FirebasePipeline:
    def __init__(self):
        # Initialize Firebase Admin SDK
        try:
            # Try to get default app
            firebase_admin.get_app()
        except ValueError:
            try:
                # Initialize app if it doesn't exist
                cred = credentials.Certificate('firebase-credentials.json')
                firebase_admin.initialize_app(cred)
            except Exception as e:
                logging.error(f"Failed to initialize Firebase: {str(e)}")
                raise
        
        self.db = firestore.client()
        self.batch = self.db.batch()
        self.batch_count = 0
        self.max_batch_size = 500  # Firestore batch limit is 500

    def process_item(self, item, spider):
        try:
            # Convert item to dict and add timestamp
            data = dict(item)
            current_time = firestore.SERVER_TIMESTAMP
            data['scraped_at'] = current_time
            
            # Create a reference to the document
            doc_ref = self.db.collection(COLLECTIONS['products']).document(str(item['product_id']))
            
            # Add to batch
            self.batch.set(doc_ref, data, merge=True)
            self.batch_count += 1

            # If batch is full, commit it
            if self.batch_count >= self.max_batch_size:
                try:
                    self.batch.commit()
                    self.batch = self.db.batch()
                    self.batch_count = 0
                except Exception as e:
                    logging.error(f"Error committing batch: {str(e)}")
                    raise

            return item
        except Exception as e:
            logging.error(f"Error processing item: {str(e)}")
            raise

    def close_spider(self, spider):
        try:
            # Commit any remaining items in the batch
            if self.batch_count > 0:
                self.batch.commit()
            
            # Log completion
            spider.logger.info("Data successfully stored in Firebase")
        except Exception as e:
            spider.logger.error(f"Error in close_spider: {str(e)}")
            raise 