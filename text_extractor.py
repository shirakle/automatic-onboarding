import requests
from bs4 import BeautifulSoup
import langid
import re

class WebpageTextExtractor:
    def __init__(self, url):
        self.url = url

    def fetch_page_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page content: {e}")
            return None

    def extract_text(self):
        page_content = self.fetch_page_content()
        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            text = soup.get_text().replace("\n", "")
            text = self.filter_english_text(text)
            return text
        else:
            return None

    def filter_english_text(self, text):
        sentences = re.split(r'[.!?]', text)
        english_sentences = []

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 0:
                lang, _ = langid.classify(sentence)
                if lang == 'en':
                    english_sentences.append(sentence)

        filtered_text = ' '.join(english_sentences)
        return filtered_text