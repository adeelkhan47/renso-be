def response_structure(data, total_rows: int = None):
    response = {"objects": data}
    if total_rows is not None:
        response["total_rows"] = total_rows
    return response


def error_message(msg):
    response = {"error": {"msg": msg}}
    return response
