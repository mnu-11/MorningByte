import feedparser
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

def fetch_rss_feeds(max_articles=200):
    """
    Browses the RSS feeds listed in the .env file and collects the latest news.
    Stops once we reach 'max_articles' to keep things fast.
    """
    rss_urls_str = os.getenv("RSS_FEED_URLS", "")
    if not rss_urls_str:
        print("❌ No RSS Feeds found! Please check your .env file.")
        return []

    # Clean up the list of URLs (remove spaces, duplicates)
    rss_urls = [url.strip() for url in rss_urls_str.split(",") if url.strip()]
    rss_urls = list(set(rss_urls))

    collected_articles = []
    
    print(f"📡 Scanning {len(rss_urls)} sources for news...")

    for url in rss_urls:
        # Stop if we already have enough news for today
        if len(collected_articles) >= max_articles:
            print("🛑 Collected enough articles. Stopping fetch.")
            break
            
        try:
            print(f"   ↳ Checking: {url}")
            feed = feedparser.parse(url)
            
            for entry in feed.entries:
                if len(collected_articles) >= max_articles:
                    break
                
                # Extract image if available (checks multiple standard RSS tags)
                image_url = "NONE"
                if 'media_content' in entry and entry.media_content:
                    image_url = entry.media_content[0].get('url', 'NONE')
                elif 'media_thumbnail' in entry and entry.media_thumbnail:
                    image_url = entry.media_thumbnail[0].get('url', 'NONE')
                elif 'enclosures' in entry and entry.enclosures:
                    for enc in entry.enclosures:
                         if enc.get('type', '').startswith('image/'):
                            image_url = enc.get('href', 'NONE')
                            break

                # Parse the date, defaulting to "Now" if missing
                published_date = entry.get('published', entry.get('updated', str(datetime.datetime.now())))

                # Create our clean article object
                article = {
                    "title": entry.get('title', 'No Title'),
                    "summary": entry.get('summary', entry.get('description', 'No summary'))[:1000],
                    "url": entry.get('link', '#'),
                    "image_url": image_url,
                    "source": feed.feed.get('title', 'Unknown Source'),
                    "published_at": published_date,
                    "created_at": datetime.datetime.now()
                }
                
                collected_articles.append(article)
                
        except Exception as e:
            print(f"⚠️ Failed to read feed {url}: {e}")

    print(f"✅ Total articles gathered: {len(collected_articles)}")
    return collected_articles
