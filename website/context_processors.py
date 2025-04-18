from .models import MaintenanceBanner
from django.utils import timezone

def maintenance_banner(request):
    now = timezone.now()
    banner = (
        MaintenanceBanner.objects
        .filter(start_time__isnull=False, end_time__isnull=False)
        .order_by('start_time')
        .first()
    )

    if not banner:
        return {}

    if now < banner.start_time:
        message = f"There is a scheduled maintenance on {banner.start_time.strftime('%Y-%m-%d %H:%M')} to {banner.end_time.strftime('%Y-%m-%d %H:%M')}. Thanks for the understanding."
        return {"maintenance_banner": message}

    elif banner.start_time <= now < banner.end_time:
        message = f"Scheduled maintenance ongoing until {banner.end_time.strftime('%Y-%m-%d %H:%M')}."
        return {"maintenance_banner": message}

    return {}
