def convert_to_int(number, default=None):
    try:
        return int(number)
    except Exception:
        return default


def suffixes_for_positional_number(number: int):
    if number == 1:
        return 'st'
    elif number == 2:
        return 'nd'
    elif number == 3:
        return 'rd'
    else:
        return 'th'
