from django.conf.urls import url

from .views.jogs import JogDetail, JogList
from .views.users import UserList, UserDetail

urlpatterns = [
    url(r'^jogs/$', JogList.as_view()),
    url(r'^jogs/(?P<jog_id>[0-9]+)/$', JogDetail.as_view()),
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<user_id>[0-9]+)/$', UserDetail.as_view())
]
