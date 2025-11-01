def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер банковской карты"""
    mask_card = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
    return mask_card


def get_mask_account(account: str) -> str:
    """Функция, которая маскирует номер банковского счета"""
    mask_account = "**" + account[-4:]
    return mask_account
