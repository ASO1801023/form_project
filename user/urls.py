from django.urls import path
from . import views
 

urlpatterns = [
    path('new/', views.new, name='new'),
    path('hikaruPath/', views.hikaruSys, name='hikarusSystem'),
    path('list/', views.list, name='list'),
    path('willCompleteQ/', views.willComplete, name='willComplete'),
    path('complete/', views.completeSys, name='complete'),
]