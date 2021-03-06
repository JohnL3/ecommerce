from django.conf.urls import url, include
from accounts.views import index, logout, login, registration, user_profile, add_avatar
from accounts import url_reset

urlpatterns = [
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', registration, name='register'),
    url(r'^profile/$', user_profile, name='profile'),
    url(r'^password-reset/', include(url_reset)),
    url(r'^avatar/$', add_avatar, name='add_avatar'),
]