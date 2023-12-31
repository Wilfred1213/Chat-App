from django.utils import timezone

def format_timestamp(timestamp):
    now = timezone.now()
    
    if timestamp.date() == now.date():
        # If the timestamp is from today, format it as "8:55 AM, Today"
        formatted_time = timestamp.strftime("%I:%M %p")
        return f"{formatted_time}, Today"
    else:
        # Otherwise, format it as "8:55 AM, [Date]"
        formatted_datetime = timestamp.strftime("%I:%M %p, %b %d, %Y")
        return formatted_datetime
