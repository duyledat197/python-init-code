from itertools import groupby

from sqlalchemy.engine.result import RowProxy


def nested_get(input_data, nested_keys, default_value=None):
    internal_value = input_data
    for k in nested_keys:
        if isinstance(internal_value, dict):
            internal_value = internal_value.get(k, default_value)
        elif isinstance(internal_value, list) and len(internal_value) > int(k):
            internal_value = internal_value[int(k)]
        elif isinstance(internal_value, RowProxy):
            internal_value = internal_value[int(k)]
        else:
            try:
                internal_value = getattr(internal_value, k)
            except AttributeError:
                return default_value
        if internal_value is None:
            return default_value
    return internal_value


def destructure_dict(dictionary, *args):
    return [nested_get(dictionary, [arg], None) for arg in args]


def self_serialize_objects_to_dicts(objects_array, serializer_function_name, serializer_params):
    dicts = []
    for obj in objects_array:
        serializer_function = getattr(obj, serializer_function_name)
        if serializer_function is not None:
            dicts.append(serializer_function(**serializer_params))
        else:
            dicts.append(None)

    return dicts


def group_array_of_json(array: list, *keys, end_key):
    keys = list(keys)
    json_grouped = {}
    key = keys.pop(0)
    for new_key, group in groupby(array, key=lambda json: json[key]):
        json_grouped[new_key] = get_only(list(group), end_key) if len(keys) == 0 \
            else group_array_of_json(list(group), *keys, end_key=end_key)
    return json_grouped


def get_only(array: list, key):
    return list(map(lambda item: item[key], array))


def upper(obj):
    if isinstance(obj, (str, int, float)):
        return str(obj).upper()
    elif isinstance(obj, list):
        return [upper(item) for item in obj]
    elif isinstance(obj, dict):
        rv = {}
        for key in obj:
            if key.upper() != key:
                rv[key.upper()] = upper(obj[key])
            else:
                rv[key] = obj[key]
        return rv
    return obj
