from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Global handler to return a custom JSON format for all DRF errors.
    Includes a friendly 'message' and full 'data' with error details.
    """
    response = exception_handler(exc, context)

    def flatten_errors(errors, parent_key=""):
        """Recursively flatten nested dict/list validation errors."""
        flattened = []
        if isinstance(errors, dict):
            for field, value in errors.items():
                key = f"{parent_key}.{field}" if parent_key else field
                flattened.extend(flatten_errors(value, key))
        elif isinstance(errors, list):
            for item in errors:
                flattened.extend(flatten_errors(item, parent_key))
        else:
            flattened.append({parent_key: str(errors)})
        return flattened

    if response is not None:
        message = None
        error_data = response.data
        flattened_errors = flatten_errors(error_data)

        if isinstance(response.data, dict):
            if "message" in response.data:
                message = response.data["message"]
            elif "detail" in response.data:
                message = response.data["detail"]
            else:
                message = (
                    next(iter(response.data.values()))[0]
                    if response.data
                    else "Validation error"
                )
        elif isinstance(response.data, list):
            message = response.data[0]
        else:
            message = str(response.data)

        return Response(
            {
                "status": False,
                "message": message,
                "data": {"errors": flattened_errors} if flattened_errors else None,
            },
            status=response.status_code,
        )

    return Response({"status": False, "message": str(exc), "data": None}, status=500)
