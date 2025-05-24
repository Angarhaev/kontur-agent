from dataclasses import dataclass

@dataclass(frozen=True)
class Bank:
    """Банковские реквизиты заказчика"""
    name: str
    bic: str
    inn: str | None
    address: str
    correspondent_account: str


@dataclass(frozen=True)
class Organization:
    org_type: str
    name: str
    slug: str
    full_name: str
    address: str
    inn: str
    kpp: str | None
    ogrn: str | None
    okpo: str | None
    okato: str | None
    okogu: str | None
    okved: str | None
    signatory: str #руководитель / предприниматель
    accountant: str | None #бухгалтер

    account: str
    work_phone: str
    mobile_phone: str | None
    email: str

    bank: Bank


@dataclass(frozen=True)
class Customer:
    """Заказчик"""
    name: str
    slug: str
    inn: str
    ogrn: str = ""
    address: str = ""
    signatory: str = ""
    phone: str = ""
    kpp: str = ""
    bank: Bank | None = None


@dataclass
class WorkItem:
    """Наименование услуги, цена, кол-во"""
    task: str
    price: int
    quantity: int = 1