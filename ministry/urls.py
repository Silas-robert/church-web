from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name ='home'),
    path('aboutUs/', views.aboutUs, name ='aboutUs'),
    path('contact/', views.contact, name ='contact'),
    path('visit/', views.visit, name ='visit'),
    path('sermons/', views.sermons, name ='sermons'),
    path('events/', views.events, name ='events'),
    path('donate/', views.donate, name ='donate'),
    path('blog/', views.blog, name='blog'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('join/', views.join, name='join'),
    path('live-stream/', views.live_stream, name='live-stream'),
    path('testimony/', views.testimony, name='testimony'),
    path('prayer_list/', views.prayer_list, name='prayer_list'),
    path('ministor/', views.ministries, name='ministries'),
    path('search_event/', views.search_event, name='search_event'),
    path('download/<int:pk>/', views.download_pdf, name='download_pdf'),
]
