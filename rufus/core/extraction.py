from bs4 import BeautifulSoup
import re

def extract_text(html_data):
    """Extract and clean text from HTML data."""
    soup = BeautifulSoup(html_data, "html.parser")
    for tag in soup(['style', 'script', 'nav', 'aside', 'footer', 'header']):
        tag.decompose()
    cleaned_txt = re.sub(r'\s+', " ", soup.get_text(separator=" ")).strip()
    return cleaned_txt
