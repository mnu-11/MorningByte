# 🗞️ MorningByte

This is a personal automation project that delivers a curated daily newsletter covering **technology, AI, gaming, anime, and developer culture** — straight to my inbox every morning.

The entire system runs autonomously in the cloud using **GitHub Actions**. It collects news from multiple RSS feeds, uses **Google Gemini AI** to select and summarize the most important stories, and sends a beautifully formatted, newspaper-style HTML email via Gmail.

The goal was simple: build a high-signal, zero-effort daily news experience tailored to my interests.

---

## ✨ How It Works

1. **Fetch**
   Every morning at **7:50 AM IST**, the workflow wakes up and scans multiple RSS feeds, collecting 100+ fresh articles.

2. **Store & Track**
   All articles are stored in **MongoDB** to maintain history and avoid duplicates.

3. **AI Curation**
   The article list is sent to **Google Gemini Flash**, which:

   * Selects the top 5 stories in each category:

     * Artificial Intelligence
     * Gaming
     * Anime
     * Coding
   * Writes crisp, two-sentence summaries for each story.

4. **Deliver**
   The system authenticates with Gmail using OAuth and sends a clean, newspaper-style HTML newsletter directly to my inbox.

No manual work. No dashboards. Just a fresh, relevant newsletter every morning.

---

## 🧱 Project Structure

* **main.py** – The orchestrator. Controls the entire pipeline end-to-end
* **rss_fetcher.py** – The collector. Fetches and parses RSS feeds
* **llm_client.py** – The writer. Communicates with Google Gemini to generate summaries
* **email_sender.py** – The postman. Handles Gmail OAuth and email delivery
* **db.py** – The memory. Manages MongoDB operations
* **.github/workflows/daily_digest.yml** – The alarm clock. Schedules the daily run using GitHub Actions

---

## 💻 Local Setup (Optional)

You normally don’t need to run this locally since everything runs on GitHub Actions, but for testing or development:

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment variables

Create a `.env` file:

```ini
MONGO_URI=mongodb+srv://...
GOOGLE_API_KEY=AIzaSy...
EMAIL_RECIPIENT=your_email@gmail.com
RSS_FEED_URLS=http://feed1.com,http://feed2.com
```

### 3. Gmail Authentication

* Download `credentials.json` from Google Cloud Console
* Run the script once
* A browser window will open for login
* This generates `token.json`, which keeps you authenticated

### 4. Run

```bash
python main.py
```

---

## ☁️ Deployment (GitHub Actions)

The project is fully automated via GitHub Actions.

Configure the following secrets:

* `MONGO_URI` – MongoDB connection string
* `GOOGLE_API_KEY` – Gemini API key
* `EMAIL_RECIPIENT` – Destination email address
* `RSS_FEED_URLS` – Comma-separated RSS URLs
* `GMAIL_TOKEN_JSON` – Full contents of your local `token.json` file

This allows the cloud workflow to securely authenticate and send emails on your behalf.

---

## 🛠️ Tech Stack

* **Language:** Python 3.12
* **AI Model:** Google Gemini 3.0 Flash
* **Database:** MongoDB Atlas
* **Automation:** GitHub Actions (Cron scheduling)
* **Email:** Gmail API (OAuth)

---

⭐ If you like this project, feel free to star the repo!
