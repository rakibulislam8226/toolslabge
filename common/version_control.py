from django.http import JsonResponse


def version_control(request):
    version_info = {
        "status": True,
        "message": "Version information retrieved successfully",
        "data": {
            "calendar": {
                "today_date": "2025-09-24",
                "today_calendar_info": {"day": "24", "month": "09", "year": "2025"},
            },
            "server_current_time": "2025-09-24T10:30:00.000Z",
            "version_settings": {
                "android": {
                    "latest_version": "1.0.1",
                    "minimum_version": "1.0.0",
                    "force_update": True,
                    "maintenance_mode": False,
                    "maintenance_started_at": None,
                    "maintenance_ended_at": None,
                },
                "ios": {
                    "latest_version": "1.0.1",
                    "minimum_version": "1.0.0",
                    "force_update": True,
                    "maintenance_mode": True,
                    "maintenance_started_at": None,
                    "maintenance_ended_at": None,
                },
            },
        },
    }
    return JsonResponse(version_info)
