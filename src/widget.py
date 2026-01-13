import re


def mask_account_card(account_card: str) -> str:
    """Функция, которая принимает строку, содержащую тип и номер карты или счета, и
    возвращает строку с замаскированным номером"""
    if not isinstance(account_card, str):
        raise TypeError("Некорректный формат данных")
    elif account_card[-20:].isdigit() and account_card[-21] == " ":
        return "Счет **" + account_card[-4:]
    elif account_card[-16:].isdigit() and account_card[-17] == " ":
        return account_card[:-12] + " " + account_card[-12:-10] + "** **** " + account_card[-4:]
    else:
        raise ValueError("Некорректный формат данных")


def get_date(date_info: str) -> str:
    """Функция, которая принимает строку с информацией об операции и
    возвращает строку с датой в формате ДД.ММ.ГГГГ"""
    if not isinstance(date_info, str):
        raise TypeError("Некорректный формат данных")

    pattern = re.compile(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}:\d{2}:\d{2}.\d{6})')
    match = pattern.fullmatch(date_info)
    if match:
        return f'{match.group(3)}.{match.group(2)}.{match.group(1)}'
    else:
        raise ValueError("Некорректный формат данных")
