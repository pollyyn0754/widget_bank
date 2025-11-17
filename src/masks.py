def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер банковской карты"""
    if not isinstance(card_number, str):
        raise TypeError('Некорректный формат данных')
    elif len(card_number) == 16 and card_number.isdigit():
        mask_card = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
        return mask_card
    else:
        raise ValueError('Некорректный номер карты')


def get_mask_account(account: str) -> str:
    """Функция, которая маскирует номер банковского счета"""
    if not isinstance(account, str):
        raise TypeError('Некорректный формат данных')
    elif len(account) == 20 and account.isdigit():
        mask_account = "**" + account[-4:]
        return mask_account
    else:
        raise ValueError('Некорректный номер счета')
