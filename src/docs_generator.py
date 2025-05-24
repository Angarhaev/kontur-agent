from langchain_core.tools import tool


class DocsGenerator:

    def save_file(self, filename: str, json_data: dict):
        output_dir = Path(__file__).parent.parent / "typst/templates_json"
        output_dir.mkdir(exist_ok=True)

        path = output_dir / filename

        with open(path, "w", encoding='utf-8') as f:
            json.dump(act_json, f, ensure_ascii=False, indent=2)

        return str(path)

    @tool
    def generate_pdf_act(self, customer: Customer, jobs: list[WorkItem]) -> str:
        """Генерирует PDF-акт"""

        act_json = {
            "customer": asdict(customer),
            "jobs": list(map(lambda j: asdict(j), jobs))
        }

        self.save_file("act_temp.json", act_json)

        command = ["typst", "compile", "--root", "./typst", "typst/act.typ"]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return "✅ PDF акт успешно создан: typst/act.pdf"

    @tool
    def generate_pdf_invoice(self, customer: Customer, jobs: list[WorkItem]) -> str:
        """Генерирует PDF-счёт"""

        invoice_json = {
            "customer": asdict(customer),
            "jobs": list(map(lambda j: asdict(j), jobs))
        }

        self.save_file("invoice_temp.json", invoice_json)

        command = ["typst", "compile", "--root", "./typst", "typst/invoice.typ"]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return "✅ PDF счёт успешно создан: typst/invoice.pdf"

    @tool
    def generate_pdf_org_card(self) -> str:
        """Генерирует PDF-карточку организации"""
        org_data = {}

        self.save_file("org_card.json", org_data)

        command = ["typst", "compile", "--root", "./typst", "typst/org_card.typ"]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return "✅ PDF карточка организации создана: typst/org_card.pdf"
