
from django.urls import path
from z_home.views import HomePage

app_name = 'home'

urlpatterns = [
    path('', HomePage.as_view(), name='wellcome-page'),
]
