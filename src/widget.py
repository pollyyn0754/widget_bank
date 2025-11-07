def mask_account_card(account_card: str) -> str:
    """Функция, которая примает строку, содержащую тип и номер карты или счета, и
    возвращает строку с замаскированным номером"""
    if account_card[-20:].isdigit():
        return "Счет **" + account_card[-4:]
    else:
        return account_card[:-12] + " " + account_card[-12:-10] + "** **** " + account_card[-4:]


def get_date(operation_info: str) -> str:
    """Функция, которая принимает строку с информацией об операции и
    возвращает строку с датой в формате ДД.ММ.ГГГГ"""
    return ".".join([operation_info[8:10], operation_info[5:7], operation_info[:4]])
