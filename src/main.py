from dataclasses import dataclass, asdict
import json
import os
import subprocess
import traceback
from typing import Sequence
import uuid
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from langchain_core.language_models import LanguageModelLike
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, tool
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from debug_tools import DebugGenerator
from models import Bank, Customer, WorkItem

load_dotenv(find_dotenv())


class DocumentTypeDetector:
    DOCUMENT_TYPES = ["Счёт", "Акт", "Карточка организации"]

    def detect_document_type(self, user_input: str) -> str:
        """Определяет тип документа из пользовательского ввода"""
        user_lower = user_input.lower()

        if any(word in user_lower for word in ["акт", "act"]):
            return "Акт"
        elif any(word in user_lower for word in ["счёт", "счет", "invoice"]):
            return "Счёт"
        elif any(word in user_lower for word in ["карточка", "реквизиты", "карт"]):
            return "Карточка организации"
        else:
            return None


class LLMAgent:
    def __init__(self, model: LanguageModelLike, tools: Sequence[BaseTool]):
        self._model = model
        self._agent = create_react_agent(model, tools=tools, checkpointer=InMemorySaver())
        self._config: RunnableConfig = {"configurable": {"thread_id": uuid.uuid4().hex}}

    def invoke(self, content: str, temperature: float = 0.1) -> str:
        """Отправляет сообщение в чат"""
        message = {"role": "user", "content": content}
        return self._agent.invoke(
            {"messages": [message], "temperature": temperature},
            config=self._config
        )["messages"][-1].content


def print_agent_response(llm_response: str) -> None:
    print(f"\033[35m{llm_response}\033[0m")


def get_user_prompt() -> str:
    return input("\nВы: ")


def main():

    model = ChatAnthropic(
        model="claude-3-haiku-20240307",
        temperature=0.1,
        max_tokens=2048,
        anthropic_api_key=os.getenv('ANTHROPIC_API_KEY')
    )

    detector = DocumentTypeDetector()
    agent = LLMAgent(model, tools=[
        DebugGenerator.generate_pdf_act,
        DebugGenerator.generate_pdf_invoice,
        DebugGenerator.generate_pdf_org_card
    ])

    print("🚀 Генератор PDF документов для ИП Ангархаева (РЕЖИМ ОТЛАДКИ)")
    print("=" * 50)

    # ОТЛАДКА: Захардкоженные данные вместо ввода пользователя
    # first_question = "Добрый день! Какой документ хотите сформировать?"
    # print(f"Assistant: {first_question}")
    # user_input = input("Вы: ")
    org_slug = "ip_angarhaeva"
    org_type = "ip"
    user_input = "карточка"  # ОТЛАДКА: захардкожено
    print(f"[ОТЛАДКА] Пользователь ввел: {user_input}")

    document_type = None
    while not document_type:
        document_type = detector.detect_document_type(user_input)
        if not document_type:
            # print("Assistant: Я не смог понять, какой вид документа вы хотите сформировать.")
            # print("Доступные типы: Акт, Счёт, Карточка организации")
            # user_input = input("Пожалуйста, уточните: ")
            user_input = "акт"  # ОТЛАДКА: захардкожено
            print(f"[ОТЛАДКА] Переспрос, пользователь ввел: {user_input}")

    print(f"✅ Определен тип документа: {document_type}")

    if document_type == "Карточка организации":
        print("Создаю карточку организации...")
        result = DebugGenerator.generate_pdf_org_card(org_slug , org_type)
        print(f"Assistant: {result}")
        return


    print("\n[ОТЛАДКА] Создаем тестовые данные...")

    test_customer = Customer(
        name='МАУ "СС"',
        inn="0323347497",
        ogrn="1030300123456",
        kpp="032301001",
        address="670031, Бурятия Респ, Улан-Удэ г, Широких-Полянского ул, дом № 50",
        work_phone="8-983-458-24-95",
        signatory="Иванов И.И."
    )

    test_jobs = [
        WorkItem(
            task='Техническое обслуживание ККТ и оборудования на 1 месяц. Пакет "СЕРВИС Lite"',
            price=600,
            quantity=10
        )
    ]

    print(f"[ОТЛАДКА] Тестовый заказчик: {test_customer.name}")
    print(f"[ОТЛАДКА] Тестовые работы: {len(test_jobs)} шт")


    try:
        if document_type == "Акт":
            print("\n[ОТЛАДКА] Вызываем debug_generate_pdf_act...")
            result = DebugGenerator.generate_pdf_act(
                customer=test_customer,
                jobs=test_jobs,
                org_slug=org_slug,
                org_type=org_type
            )
            print(f"[ОТЛАДКА] Результат: {result}")
        elif document_type == "Счёт":
            print("\n[ОТЛАДКА] Вызываем debug_generate_pdf_invoice...")
            result = DebugGenerator.generate_pdf_invoice(test_customer, test_jobs)
            print(f"[ОТЛАДКА] Результат: {result}")
    except Exception as e:
        print(f"[ОТЛАДКА] ОШИБКА: {type(e).__name__}: {e}")
        import traceback
        print(f"[ОТЛАДКА] Полный трейсбек:")
        traceback.print_exc()


    """
    system_prompt = f'''
    Пользователь хочет сгенерировать: {document_type}

    Твоя задача собрать данные заказчика поэтапно:
    1. Название организации  
    2. ИНН
    3. ОГРН
    4. Адрес
    5. Подписант
    6. Данные о работах (название, количество, цена)

    После получения всех данных используй соответствующий инструмент.
    Начни с первого вопроса.
    '''

    agent_response = agent.invoke(content=system_prompt)

    while True:
        print_agent_response(agent_response)
        user_input = get_user_prompt()

        if user_input.lower() in ['выход', 'quit', 'exit']:
            print("👋 Досвидания!")
            break

        agent_response = agent.invoke(user_input)

        if "✅ PDF" in agent_response:
            print("\n🎉 Документ готов!")
            next_action = input("Хотите создать ещё один документ? (да/нет): ")
            if next_action.lower() in ['да', 'yes', 'y']:
                main()
            break
    """


if __name__ == "__main__":
    main()