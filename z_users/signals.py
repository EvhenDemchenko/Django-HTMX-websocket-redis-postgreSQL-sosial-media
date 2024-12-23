from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from z_users.models import UserNotification

@receiver(post_save , sender = UserNotification)
def send_comment_notification(sender , instance , created , **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = 'notifications'
        event = {
            'type': 'user_notification_handler',
            'notification': instance.id
        }

        async_to_sync(channel_layer.group_send)(
            group_name , event
        )
