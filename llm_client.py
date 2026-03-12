import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def generate_newsletter(articles):
    """
    Sends the gathered news to Google's Gemini AI to write a professional newsletter.
    """
    
    if not articles:
        print("⚠️ No articles provided to the AI. Skipping generation.")
        return None

    # Format the articles into a simple text list for the AI to read
    articles_data = ""
    for i, art in enumerate(articles):
        articles_data += f"""
        --- Story {i+1} ---
        Headline: {art.get('title')}
        Source: {art.get('source')}
        Link: {art.get('url')}
        Image: {art.get('image_url')}
        Summary: {art.get('summary')}
        """

    # The Prompt: Instructing the AI on how to act and what to create
    system_instruction = "You are a professional technology newspaper editor."
    
    user_prompt = f"""
Write a 'MorningByte' HTML email newsletter based on the stories below.

===============================
VISUAL STYLE (VERY IMPORTANT)
===============================

Design the layout to resemble a **classic vintage / old-town newspaper front page**.

Use these concepts:
- Serif typography
- Multi-column layout (2 or 3 columns) using tables
- Boxed article sections like newspaper clippings
- Minimal colors (black, dark gray, beige)
- Light beige paper background (#f5f1e6 or similar)
- Thin borders around article blocks
- Dense but clean typography

===============================
MASTHEAD DESIGN (TOP HEADING)
===============================

Design the title "MorningByte" to visually resemble a **traditional gothic / blackletter newspaper masthead**, using ONLY email-safe fonts.

Font stack:
"Times New Roman", Georgia, "Palatino Linotype", serif

Styling:
- Font size: 48px–56px
- Font weight: 800–900
- Letter spacing: 2px–3px
- Uppercase text
- Slight text shadow for printed ink feel
- Dark ink color (#1a1a1a or black)
- Thick bottom border line
- Center aligned
- Full width row
- Light beige background
- Padding top & bottom (16px–24px)

Add subtitle below masthead:
"DAILY TECH & POP CULTURE GAZETTE"
Small font, letter spaced.

Add thin decorative horizontal lines above and below the masthead.

Do NOT use external fonts, SVG, images, or web fonts for the masthead.

===============================
TECHNICAL HTML RULES
===============================

- Use ONLY table-based layout (email compatible)
- Inline CSS only
- No external CSS or fonts
- Max width: 800px, centered
- Gmail and Outlook safe HTML
- Images (if used):
  - Optional
  - Max width: 100%
  - Rounded corners (6–8px)
  - Placed above article text

===============================
LAYOUT STRUCTURE
===============================

1. Masthead section
2. Subtitle line
3. Horizontal divider
4. Main content in 2 or 3 columns
5. Articles stacked vertically inside each column

Each article block:
- Bold clickable headline
- Small italic source line (e.g., "via TechCrunch")
- 2 sentence neutral journalistic summary
- Optional image (if valid URL)
- make sure that many articles have images for the resultant summarized article

===============================
CONTENT RULES
===============================

Select exactly **20 articles** from the provided data:

1. Anime & Manga – 5
2. Artificial Intelligence – 5
3. Gaming – 5
4. Coding & Development – 5

If any category has insufficient data, fill with closest tech news.

Group articles by category with clear section headers.

===============================
OUTPUT RULES
===============================

- Output ONLY raw HTML
- No markdown
- No explanation
- No ```html wrappers

===============================
DATA
===============================

{articles_data}
"""



    print("🧠 Sending data to Google Gemini AI...")

    google_key = os.getenv("GOOGLE_API_KEY")
    if not google_key:
        print("❌ Error: GOOGLE_API_KEY is missing.")
        return None

    try:
        # Initialize Google's Generative AI Client
        client = genai.Client(api_key=google_key)
        
        # We use Gemini 3.0 Flash for its speed and context handling
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=[
                {"role": "user", "parts": [{"text": system_instruction}]},
                {"role": "user", "parts": [{"text": user_prompt}]}
            ]
        )
        
        # Clean up the output to ensure it's pure HTML
        html_output = response.text.replace("```html", "").replace("```", "").strip()
        
        print("✨ Newsletter HTML generated successfully!")
        return html_output

    except Exception as e:
        print(f"❌ AI Generation Failed: {e}")
        return "<h1>Details Unavailable</h1><p>Sorry, the AI could not generate the newsletter today.</p>"
