from django.urls import path
from userauths.views import registration_page, login_page, logout_page

app_name = 'userauths'

urlpatterns = [
    path("sign-up/", registration_page, name='registration_page'),  # Make sure to use the view function, not a string
    path("sign-in/", login_page, name='login_page'),
    path("sign-out/", logout_page, name='sign-out'),
]
