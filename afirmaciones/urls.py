from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('debug-comentarios/', views.debug_comentarios, name='debug_comentarios'),
    path('test/', views.test_comentarios, name='test_comentarios'),
    path('simple/', views.simple_test, name='simple_test'),
] 