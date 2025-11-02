def get_date(operation_info: str) -> str:
    """Функция, которая принимает строку с информацией об операции и возвращает строку с датой в формате ДД.ММ.ГГГГ"""
    return ".".join([operation_info[8:10], operation_info[5:7], operation_info[:4]])
