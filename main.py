import db
import rss_fetcher
import llm_client
import email_sender

def run_pipeline():
    """
    The main orchestrator function.
    Runs the news processing steps in order.
    """
    print("\n🚀 Starting MorningByte Pipeline...")
    print("---------------------------------------")

    # Step 1: Clean the Database
    # We want fresh news only, so we remove yesterday's data.
    db.clear_old_articles()
    
    # Step 2: Fetch News
    # Go to the internet and grab the latest RSS feeds.
    # We fetch a larger pool (up to 200) so the AI has enough specific content to choose from.
    articles = rss_fetcher.fetch_rss_feeds(max_articles=200)
    
    if not articles:
        print("⚠️ No articles found today. Aborting pipeline.")
        return

    # Step 3: Save to Storage
    # Keep a copy in MongoDB.
    db.save_articles(articles)
    
    # Step 4: Generate Content
    # Ask the AI to write the newsletter based on the saved articles.
    # Note: We can pass the 'articles' list directly since we just fetched it.
    newsletter_html = llm_client.generate_newsletter(articles)
    
    if not newsletter_html or len(newsletter_html) < 100:
        print("❌ Failed to generate valid newsletter content.")
        return

    # Step 5: Deliver
    # Send the email to the user.
    email_sender.send_email(newsletter_html)
    
    print("---------------------------------------")
    print("✅ Pipeline Completed Successfully.\n")

if __name__ == "__main__":
    run_pipeline()
