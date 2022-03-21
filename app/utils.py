from flask import Response, request
from flask_restful import abort


def url_filter(filters, args, model):
    checked_arg = {
        key: value if key in filters else abort(Response(f'Incorrect filter', 400)) for key, value in args.items()
    }
    filtered_args = {key: value for key, value in checked_arg.items() if value is not None}
    query_filters = [getattr(model, attribute) == value for attribute, value in filtered_args.items()]
    return query_filters


def validate_request_data(schema):
    data = request.get_json()
    errors = schema.validate(data)
    if errors:
        abort(Response(f'Incorrect data {errors}', 400))
    return data
