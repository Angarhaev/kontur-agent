import os
from dataclasses import dataclass, field, fields

from dotenv import load_dotenv

load_dotenv()


@dataclass
class EnvConfig:
    anthropic_api_key: str = field(init=False)

    def __post_init__(self):
        """Если какую переменную не удалось загрузить - вызывает ошибку"""
        missing = []

        for f in fields(self):
            env_var = f.name.upper()
            value = os.getenv(env_var)

            setattr(self, f.name, value)

            if value is None and f.default is field(default=None).default:
                missing.append(env_var)

        if missing:
            raise ValueError(f"Missing required env vars: {', '.join(missing)}")
