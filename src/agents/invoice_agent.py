
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class InvoiceAgent:
    def __init__(self, client: Anthropic):
        self.client = client

    def generate_document(self, prompt: str) -> str:
        response = self.client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
