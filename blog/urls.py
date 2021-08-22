from django.contrib import admin
from django.urls import path,include
from . import views 
from django.conf import settings
from django.conf.urls.static import static

app_name="blog"

urlpatterns = [
    path('dashboard/', views.home),
    path('addblog/',views.addblog),
    path('draft/',views.draft),
    path('published/',views.published),
    path('allblog/',views.allblog),
    path('showblog/<int:id>',views.showblog,name='showblog'),
    path('drafttopub/<int:id>',views.drafttopub,name='drafttopub'),
    
    path('drafttodel/<int:id>',views.drafttodel,name='drafttodel'),
    path('publishtodel/<int:id>',views.publishtodel,name='publishtodel')
]

