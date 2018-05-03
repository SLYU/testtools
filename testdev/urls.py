from django.conf.urls import url
from . import  views
urlpatterns = [
    #homepage
    url(r'^upload_file/$',views.upload_file,name='upload_file' ),
    url(r'^stressTesting/$',views.stressTesting,name='stressTesting' ),
    url(r'^$',views.index,name='index' ),
    url(r'^test/$',views.test,name='test')
]