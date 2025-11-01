def get_date(operation_info: str) -> str:
    return ".".join([operation_info[8:10], operation_info[5:7], operation_info[:4]])
