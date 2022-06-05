from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login, name="login"),
    path('home', views.index, name="home"),
    path('register', views.register, name="register"),
    path('find', views.find, name="find"),
    path('termlonger', views.termlonger, name="termlonger"),
    path('changepass', views.changepass, name="changepass"),
    path('history', views.history, name="history"),
    path('logout', views.logout, name="logout"),
    path('find_stuff', views.findstuff, name="findstuff"),
    path('uhome', views.userhome, name="user_home"),
    path('ownchangepass', views.change_own_pass, name="ownchangepass"),
    path('uownchangepass', views.changeownpassuser, name="uownchangepass"),
    path('remindpass', views.remind_password, name="remindpass"),
    path('update/<int:pk>', views.UserUpdateView, name="user-update"),
    path('checkhistory/<int:pk>', views.HistoryView, name="history_check"),
    path('VPN', views.accesstovpn, name="vpn"),
    path('addtovpn', views.addtovpn, name="addtovpn"),
    path('addtovpn_noc', views.addtovpn_noc, name="addtovpn_noc"),
    path('recovery/<str:code>', views.recoverypass, name="recovery"),
    path('mypage', views.mypage, name="mypage")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
