from django.conf.urls import url
from accounts import views as accounts_views


urlpatterns = [
    url(
        r"^send_login_email$", accounts_views.send_login_email, name="send_login_email"
    ),
    url(r"^login$", accounts_views.login, name="login"),
]
