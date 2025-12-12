import logging


logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер банковской карты"""
    logger.info(f"Начало маскирования карты: {card_number}")
    if not isinstance(card_number, str):
        logger.error(f"Некорректный формат номера карты: {card_number}")
        raise TypeError("Некорректный формат данных")
    elif len(card_number) == 16 and card_number.isdigit():
        mask_card = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
        logger.info(f"Результат маскирования: {mask_card}")
        return mask_card
    else:
        logger.warning(f"Некорректный формат номера карты: {card_number}")
        raise ValueError("Некорректный номер карты")


def get_mask_account(account: str) -> str:
    """Функция, которая маскирует номер банковского счета"""
    logger.info(f"Начало маскирования счета: {account}")
    if not isinstance(account, str):
        logger.error(f"Некорректный формат номера счета: {account}")
        raise TypeError("Некорректный формат данных")
    elif len(account) == 20 and account.isdigit():
        mask_account = "**" + account[-4:]
        logger.debug(f"Результат маскирования: {mask_account}")
        return mask_account
    else:
        logger.warning(f"Некорректный формат номера счета: {account}")
        raise ValueError("Некорректный номер счета")
