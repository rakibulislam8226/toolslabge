from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "limit"  # allow client to override page size
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "status": True,
                "message": "Data retrieved successfully",
                "data": (
                    data["data"] if isinstance(data, dict) and "data" in data else data
                ),
                "meta": {
                    "from": self.page.start_index(),
                    "to": self.page.end_index(),
                    "total": self.page.paginator.count,
                    "num_pages": self.page.paginator.num_pages,
                    "current_page": self.page.number,
                    "has_previous": self.page.has_previous(),
                    "has_next": self.page.has_next(),
                },
            }
        )
