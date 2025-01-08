def is_2xx(status) -> bool:
    if not isinstance(status, int):
        return False
    
    return status >= 200 and status < 300