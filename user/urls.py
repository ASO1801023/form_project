from django.urls import path
from . import views
 
urlpatterns = [
    path('new/', views.new, name='new'),
    path('hikaruPath/', views.hikaruSys, name='hikarusSystem'),
    path('search/', views.search, name='search'),
]
