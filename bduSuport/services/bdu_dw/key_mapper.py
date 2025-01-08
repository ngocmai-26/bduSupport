def convert_keys(data: dict, key_mapping: dict) -> dict:
    return {key_mapping.get(key, key): value for key, value in data.items()}

def convert_list(data: list, key_mapping: dict) -> list:
    return [convert_keys(item, key_mapping) for item in data]
