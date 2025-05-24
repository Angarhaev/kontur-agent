from pathlib import Path


def check_required_typst_files(path):
    """Проверяет наличие всех необходимых файлов"""
    required_files = [
        f"{path}/ru-numbers.typ",
        f"{path}/act.typ",
        f"{path}/invoice.typ",
        f"{path}/org_card.typ"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        raise FileNotFoundError(f"Отсутствуют обязательные файлы: {', '.join(missing_files)}")