from flask import jsonify


def generate_success_response(data=None, offset=None, limit=None, total=None):
    result = {'success': True, 'data': data}
    if offset is not None:
        result['offset'] = offset
    if limit is not None:
        result['limit'] = limit
    if total is not None:
        result['total'] = total
    return jsonify(result)
