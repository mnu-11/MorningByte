import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables just in case
load_dotenv()

def get_db_connection():
    """
    Establishes a secure connection to the MongoDB Atlas database.
    """
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        print("❌ Error: MONGO_URI is missing from environment variables.")
        return None
    
    try:
        # We use certifi to ensure SSL certificates work correctly on all machines
        client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
        db = client['news_digest_db']
        return db['raw_articles']
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def clear_old_articles():
    """
    Wipes the database clean before we add today's fresh news.
    """
    collection = get_db_connection()
    if collection is None:
        return

    try:
        result = collection.delete_many({})
        print(f"🧹 Database cleaned! Removed {result.deleted_count} old articles.")
    except Exception as e:
        print(f"⚠️ Warning: Could not clear database: {e}")

def save_articles(articles):
    """
    Saves a list of article dictionaries to the database.
    """
    if not articles:
        print("⚠️ No articles to save.")
        return

    collection = get_db_connection()
    if collection is None:
        return
    
    try:
        result = collection.insert_many(articles)
        print(f"💾 Successfully saved {len(result.inserted_ids)} articles to MongoDB.")
    except Exception as e:
        print(f"❌ Error saving articles: {e}")

def get_all_articles():
    """
    Fetches all currently stored articles to send to the AI.
    """
    collection = get_db_connection()
    if collection is None:
        return []
    
    try:
        articles = list(collection.find({}))
        print(f"📖 Retrieved {len(articles)} articles from storage.")
        return articles
    except Exception as e:
        print(f"❌ Error reading articles: {e}")
        return []
