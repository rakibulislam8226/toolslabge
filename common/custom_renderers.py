from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    """
    A global renderer that enforces a consistent response structure across all APIs.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response", None)
        request = renderer_context.get("request", None)

        # Handle errors
        if response and response.exception:
            return super().render(data, accepted_media_type, renderer_context)

        # If already paginated
        if isinstance(data, dict) and "meta" in data and "data" in data:
            final_data = data

        else:
            method_message_map = {
                "POST": "Created successfully",
                "PUT": "Updated successfully",
                "PATCH": "Updated successfully",
                "DELETE": "Deleted successfully",
                "GET": "Data retrieved successfully",
            }

            # fallback if request missing
            message = method_message_map.get(
                request.method if request else "GET", "Success"
            )

            # non-paginated responses
            final_data = {
                "status": True,
                "message": message,
                "data": data,
            }

        return super().render(final_data, accepted_media_type, renderer_context)
