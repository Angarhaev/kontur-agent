from pathlib import Path
import json
from dataclasses import asdict
import subprocess

from src.models import Bank, Customer, WorkItem, Organization
from src.exceptions import DocsGeneratorError
from src.utils import check_required_typst_files

class DebugGenerator:
    @staticmethod
    def save_req_file(organization: Organization, filename: str, json_data: dict):

        output_dir = Path(__file__).parent.parent / f"typst/{organization.org_type}/{organization.slug}/templates_json"
        output_dir.mkdir(exist_ok=True)

        path = output_dir / filename

        with open(path, "w", encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        return str(path)

    @staticmethod
    def load_organization_from_file(org_slug, org_type):
        try:
            path = Path(__file__).parent.parent / "config/org_profiles.json"
            with open(path, "r", encoding="utf-8") as org_file:
                data = json.load(org_file)

            requisites = data[org_type][org_slug]
            return Organization(
                org_type=requisites["org_type"],
                slug=requisites["slug"],
                name=requisites["name"],
                full_name=requisites["full_name"],
                address=requisites["address"],
                inn=requisites["inn"],
                kpp=requisites.get("kpp"),
                ogrn=requisites.get("ogrn"),
                okpo=requisites.get("okpo"),
                okato=requisites.get("okato"),
                okogu=requisites.get("okogu"),
                okved=requisites.get("okved"),
                account=requisites["account"],
                signatory=requisites["signatory"],
                accountant=requisites.get("accountant"),
                work_phone=requisites["work_phone"],
                mobile_phone=requisites.get("mobile_phone"),
                email=requisites["email"],
                bank=Bank(
                    name=requisites["bank"]["name"],
                    bic=requisites["bank"]["bic"],
                    inn=requisites["bank"]["inn"],
                    address=requisites["bank"]["address"],
                    correspondent_account=requisites["bank"]["correspondent_account"]
                )
            )
        except (FileNotFoundError, PermissionError, json.JSONDecodeError, KeyError, TypeError) as e:
            raise DocsGeneratorError(f"Failed get organization {org_name}") from e


    @staticmethod
    def generate_pdf_act(customer: Customer, jobs: list[WorkItem], org_slug: str, org_type: str) -> str:
        """Генерирует PDF-акт (версия для отладки)"""

        act_json = {
            "customer": asdict(customer),
            "jobs": list(map(lambda j: asdict(j), jobs))
        }

        organization = DebugGenerator.load_organization_from_file("ip_angarhaeva")

        print(f"[ОТЛАДКА] Создаем act_temp.json с данными:")
        print(json.dumps(act_json, ensure_ascii=False, indent=2))

        file_name = "act_temp.json"
        DebugGenerator.save_req_file("act_temp.json", act_json)

        print(f"[ОТЛАДКА] Файл act.json сохранен")

        command = [
            "typst",
            "compile",
            "--root", "./typst",
            "--font-path", "typst/fonts",
            "typst/act.typ",
            "output/act.pdf"
        ]
        print(f"[ОТЛАДКА] Выполняем команду: {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True)

        print(f"[ОТЛАДКА] Возвращенный код: {result.returncode}")
        print(f"[ОТЛАДКА] Stdout: {result.stdout}")
        print(f"[ОТЛАДКА] Stderr: {result.stderr}")

        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, command, result.stdout, result.stderr)

        return "✅ PDF акт успешно создан: typst/act.pdf"

    @staticmethod
    def generate_pdf_org_card(org_slug, org_type) -> str:
        """Генерирует PDF-карточку организации (версия для отладки)"""

        organization = DebugGenerator.load_organization_from_file(org_slug, org_type)

        DebugGenerator.save_req_file(organization, f"org_card.json", asdict(organization))

        base_dir = f"typst/{organization.org_type}/{organization.slug}"
        check_required_typst_files(base_dir)

        output_dir = Path(f"output/{organization.org_type}/{organization.slug}")
        output_dir.mkdir(parents=True, exist_ok=True)

        command = [
            "typst",
            "compile",
            "--root", "./typst",
            "--font-path", "typst/fonts",
            f"{base_dir}/org_card.typ",
            f"{output_dir}/org_card.pdf"
        ]

        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return f"✅ PDF карточка организации {organization.name} создана: {output_dir}/org_card.pdf"

    @staticmethod
    def generate_pdf_invoice(customer: Customer, jobs: list[WorkItem]) -> str:
        """Генерирует PDF-счёт (версия для отладки)"""

        invoice_json = {
            "customer": asdict(customer),
            "jobs": list(map(lambda j: asdict(j), jobs))
        }

        DebugGenerator.save_req_file("invoice_temp.json", invoice_json)

        command = [
            "typst",
            "compile",
            "--root", "./typst",
            "--font-path", "typst/fonts",
            "typst/invoice.typ",
            f"output/invoice.pdf"
        ]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return "✅ PDF счёт успешно создан: typst/invoice.pdf"