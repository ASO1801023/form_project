from django.urls import path
from . import views
 

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('hikaruPath/', views.hikaruSys, name='hikarusSystem'),
<<<<<<< HEAD
    path('search/', views.search, name='search'),
]
=======
    path('list/', views.list, name='list'),
    path('willCompleteQ/', views.willComplete, name='willComplete'),
    path('complete/', views.completeSys, name='complete'),
    path('list_2/', views.list_2, name="list_2"),
]
>>>>>>> 35815a498e0145896a18cac74e7e0fc54cb3e014
