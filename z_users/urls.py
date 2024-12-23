
from django.urls import path
from z_users.views import *

app_name = 'users'

urlpatterns = [
    path('profile/', UserProfile.as_view(), name='profile'),
    path('profile/<username>', UserProfile.as_view(), name='profile'),
    path('profile/edit/' , UserProfileEdit.as_view(), name="profile-edit"),
    path('profile/email-edit/' , UserProfileEditEmail.as_view(), name="profile-email-edit"),
    path('profile/<user_id>/clear-notifications/', ClearNotifications.as_view(), name='profile-clear-notifications' ),
    path('profile/<user_id>/notification/<notification_id>',ClearCurrentNotification.as_view(), name='profile-clear-current-notification')
]
