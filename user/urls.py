from django.urls import path
from . import views
 

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('hikaruPath/', views.hikaruSys, name='hikarusSystem'),
    path('search/', views.search, name='search'),
    path('list/', views.list, name='list'),
    path('willCompleteQ/', views.willComplete, name='willComplete'),
    path('willDeleteQ/', views.willDelete, name='willDelete'),
    path('complete/', views.completeSys, name='complete'),
    path('delete/', views.deleteSys, name='delete'),
    path('list_2/', views.list_2, name="list_2"),
    path('completed/', views.completed, name="completed"),
    path('random/', views.randomshow, name="completed"),
]
