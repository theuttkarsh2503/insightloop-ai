# backend/extractor.py
# Extract readable text from HTML using BeautifulSoup

from bs4 import BeautifulSoup

def extract_information(html: str) -> str:
    """
    Extract meaningful text from HTML content.
    """
    try:
        soup = BeautifulSoup(html, "lxml")

        # Remove scripts, styles
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        text = soup.get_text(separator=" ", strip=True)

        # Limit max length (avoid huge pages)
        return text[:2000]  # first 2000 characters

    except Exception as e:
        return f"Error during extraction: {e}"
