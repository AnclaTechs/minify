from django import template
register = template.Library()

from ..models import Notification

@register.simple_tag
def unread_notification(user):
    no = Notification.objects.filter(user=user, read=False).count()
    if no >= 1:
        return True
    else:
        return False