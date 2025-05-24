#let org = json("templates_json/org_card.json")

#set page(paper: "a4", margin: (x: 2cm, y: 2cm))
#set text(font: "Times New Roman", size: 12pt)

#align(center, text(16pt, weight: "bold")[
  КАРТОЧКА ОРГАНИЗАЦИИ
])

#v(2em)

#table(
  columns: (5cm, 1fr),
  stroke: 0.1em,
  inset: (left: 5pt, rest: 10pt),

  [*Полное наименование:*], [#org.full_name],
  [*Юридический адрес:*], [#org.address],
  [*ИНН:*], [#org.inn],
  [*ОГРН:*], [#org.ogrn],
  [*Расчётный счёт:*], [#org.account],
  [*Банк:*], [#org.bank.name],
  [*Адрес банка:*], [#org.bank.address],
  [*БИК:*], [#org.bank.bic],
  [*Корреспондентский счёт:*], [#org.bank.correspondent_account],
  [*ИНН банка:*], [#org.bank.inn],
  [*E-mail:*], [#org.email],
  [*Номер телефона:*], [#org.work_phone],
)

#v(4em)

#align(center)[
  #box(stroke: 1pt, inset: 1em)[
    *Для переводов и платежей*

    Получатель: #org.name

    ИНН: #org.inn

    Счёт: #org.account

    Банк: #org.bank.name

    БИК: #org.bank.bic

    Корр. счёт: #org.bank.correspondent_account
  ]
]

#v(2em)

#align(right)[
  Дата формирования: #datetime.today().display("[day].[month].[year]")
]