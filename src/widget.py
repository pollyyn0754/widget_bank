def mask_account_card(account_card: str) -> str:
    """Функция, которая принимает строку, содержащую тип и номер карты или счета, и
    возвращает строку с замаскированным номером"""
    if not isinstance(account_card, str):
        raise TypeError('Некорректный формат данных')
    elif account_card[-20:].isdigit() and account_card[-21] == ' ':
        return "Счет **" + account_card[-4:]
    elif account_card[-16:].isdigit() and account_card[-17] == ' ':
        return account_card[:-12] + " " + account_card[-12:-10] + "** **** " + account_card[-4:]
    else:
        raise ValueError("Некорректный формат данных")


def get_date(date_info: str) -> str:
    """Функция, которая принимает строку с информацией об операции и
    возвращает строку с датой в формате ДД.ММ.ГГГГ"""
    if (
        len(date_info) == 26 and date_info[4] == '-' and date_info[7] == '-'
        and date_info[10] == 'T' and date_info[19] == '.'
        and date_info[13] == ':' and date_info[16] == ':'):
                return ".".join([date_info[8:10], date_info[5:7], date_info[:4]])
    elif not isinstance(date_info, str):
        raise TypeError('Некорректный формат данных')
    else:
        raise ValueError("Некорректный формат данных")
