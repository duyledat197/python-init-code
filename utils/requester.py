import hashlib
import hmac

from dateutil.parser import parse
from sqlalchemy import desc, asc

from utils.exceptions import BadRequest, Unauthorized


def get_pagination_params(request):
    r_offset = request.args.get('offset', None, type=int)
    r_limit = request.args.get('limit', None, type=int)
    if r_offset is not None or r_limit is not None:
        offset = r_offset or 0
        limit = r_limit
        return offset, limit

    r_start = request.args.get('_start', None, type=int)
    r_end = request.args.get('_end', None, type=int)
    offset = r_start or 0
    limit = 10
    if r_start is not None and r_end is not None:
        limit = r_end - r_start

    return offset, limit


def get_sort(request, map_sort, default_sort_by):
    request_sort_by = request.args.get("sort_by", None)
    sort_by = map_sort[request_sort_by] if request_sort_by is not None and request_sort_by in map_sort \
        else default_sort_by
    request_sort_type = request.args.get("sort_type", None)
    sort_type = asc if request_sort_type == 'ASC' else desc
    return sort_by, sort_type


def get_list_type_param(request, param_name):
    param = request.args.get(param_name, None)
    if param is not None:
        param = request.args.getlist(param_name)
    return param


def get_datetime_param_from_url(request, param_name, default_value):
    datetime_str = request.args.get(param_name, None)
    if datetime_str is None:
        return default_value

    try:
        return parse(datetime_str)
    except ValueError:
        raise BadRequest(f"'{param_name}' has an invalid format datetime")


def validate_header_x_hub(secret, headers, payload):
    try:
        header_x_hub_signature = headers['X-Hub-Signature'].split('=')[1]
        print(f'header_x_hub_signature: {header_x_hub_signature}')
        print(f'payload: {payload}')
        signature = hmac.new(bytes(secret, 'latin-1'), payload, hashlib.sha1).hexdigest()
        if not hmac.compare_digest(signature, header_x_hub_signature):
            raise Exception()
    except Exception as e:
        print(e)
        raise Unauthorized('Request header X-Hub-Signature not present or invalid')


def get_param_boolean(request, param_name):
    param_value = request.args.get(param_name, None)
    if param_value == 'true':
        param = True
    elif param_value == 'false':
        param = False
    else:
        param = None
    return param
