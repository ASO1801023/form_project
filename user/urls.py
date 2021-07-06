from django.urls import path
from . import views
from django.views.generic import TemplateView
 

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('hikaruPath/', views.hikaruSys, name='hikarusSystem'),
    path('search/', views.search, name='search'),
    path('list/', views.list, name='list'),
    path('willCompleteQ/', views.willComplete, name='willComplete'),
    path('complete/', views.completeSys, name='complete'),
    path('list_2/', views.list_2, name="list_2"),
    path('completed/', views.completed, name="completed"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('delete_confirm', TemplateView.as_view(template_name='registration/delete_confirm.html'), name='delete-confirmation'),
    path('delete_complete', views.DeleteView.as_view(), name='delete-complete'),
]
