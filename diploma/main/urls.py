from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login, name="login"),
    path('home', views.index, name="home"),
    path('register', views.register, name="register"),
    path('find', views.find, name="find"),
    path('termlonger', views.termlonger, name="termlonger" ),
    path('changepass', views.changepass, name="changepass"),
    path('history', views.history, name="history"),
    path('logout', views.logout, name="logout"),
    path('ownchangepass', views.change_own_pass, name="ownchangepass")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)