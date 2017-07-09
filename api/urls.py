from django.conf.urls import url

from .views.jogs import JogDetail, JogList

urlpatterns = [
    url(r'^jogs/$', JogList.as_view()),
    url(r'^jogs/(?P<jog_id>[0-9]+)/$', JogDetail.as_view())
]
