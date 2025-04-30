from .models import MaintenanceBanner
from django.utils import timezone

def maintenance_banner(request):
    now = timezone.now()
    banners = MaintenanceBanner.objects.filter(
        start_time__isnull=False,
        end_time__isnull=False,
        end_time__gte=now  # Only future and ongoing
    ).order_by('start_time')

    if not banners.exists():
        return {}

    banner_messages = []

    for banner in banners:
        if now < banner.start_time:
            message = f"Upcoming: Scheduled maintenance on {banner.start_time.strftime('%Y-%m-%d %H:%M')} to {banner.end_time.strftime('%Y-%m-%d %H:%M')}."
        elif banner.start_time <= now < banner.end_time:
            message = f"Ongoing: Scheduled maintenance until {banner.end_time.strftime('%Y-%m-%d %H:%M')}."
        else:
            continue
        banner_messages.append(message)

    return {"maintenance_banners": banner_messages}
