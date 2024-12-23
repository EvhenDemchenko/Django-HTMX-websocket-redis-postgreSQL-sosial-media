
from z_users.models import UserNotification
from django import template
from django.db.models import  Q  



register = template.Library()

@register.inclusion_tag('users/notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    notifications = UserNotification.objects.filter(receiver=request_user).exclude(
        Q(has_seen=True)|
        Q(author=request_user)
    ).order_by('-created_at')
    


    return {'notifications':notifications,   'request_user':request_user}
    
