from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    #url(r'^success/(?P<number>\d+)$', views.success),
    url(r'^success/?$', views.success),
    url(r'^process_registration/?$', views.processRegistration),
    url(r'^process_login/?$', views.processLogin),
    url(r'^logout/?$', views.logout),
]
