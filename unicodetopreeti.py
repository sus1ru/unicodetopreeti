import requests
from bs4 import BeautifulSoup
import html


class UnicodeToPreeti:
    URL = "https://unicode.shresthasushil.com.np/"

    def __init__(self, timeout=10):
        self.timeout = timeout

    def _fetch(self, text: str) -> str:
        """
        Send request to converter and return raw HTML
        """
        payload = {
            "userInput": text
        }

        response = requests.post(self.URL, data=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def _parse_output(self, html_content: str) -> str:
        """
        Extract text from <textarea class="out preeti">
        """
        soup = BeautifulSoup(html_content, "html.parser")

        textarea = soup.find("textarea", {"class": "out preeti"})
        if not textarea:
            raise ValueError("Output textarea not found")

        # decode HTML entities
        return html.unescape(textarea.text.strip())

    def convert_text(self, text: str) -> str:
        """
        Convert Unicode string → Preeti
        """
        html_content = self._fetch(text)
        return self._parse_output(html_content)

    def convert_file(self, file_path: str) -> str:
        """
        Convert text file → Preeti
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return self.convert_text(content)

    def convert(self, input_data):
        """
        Smart handler:
        - string → convert directly
        - file path → detect and convert
        """
        try:
            # Try treating as file
            with open(input_data, "r", encoding="utf-8"):
                return self.convert_file(input_data)
        except (FileNotFoundError, OSError):
            return self.convert_text(input_data)
