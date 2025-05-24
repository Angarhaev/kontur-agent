import json
from json import JSONDecodeError

from anthropic import Anthropic


class ProxyAgent:
    """Прокси агент, который подготовит данные для документа"""
    DOCUMENT_TYPES = ["Счёт", "Акт", "Карточка организации"]

    def __init__(self, client: Anthropic):
        self.client = client

    def detect_document_type(self, user_prompt: str) -> dict[str, str|None]:
        """Функция для определения типа документа"""
        prompt = f"""
        Определи тип документа, который хочет сформировать юзер.
        Пришли ответ в виде json и никак больше.
        Формат ответа: {{"type": "вид документа"}}
        Вместо "вид документа" используй один из: {self.DOCUMENT_TYPES}
        Если не удалось определить — верни "None".
        Промт юзера: {user_prompt}
        """

        try:
            response = self.client.messages.create(
                model="claude-3-5-haiku-latest",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            data = json.loads(response.content[0].text)
            doc_type = data["type"]

            if doc_type == "None":
                data["type"] = None

            return data

        except (JSONDecodeError, KeyError, IndexError, AttributeError) as e:
            return {"type": None, "error": str(e)}
