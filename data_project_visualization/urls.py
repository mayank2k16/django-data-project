from django.urls import path

from . import views

app_name = 'data_project_visualization'
urlpatterns = [
    path('data1', views.data_project_1, name = 'data_project_1'),
    path('data2', views.data_project_2, name = 'data_project_2'),
    path('data3', views.data_project_3, name = 'data_project_3'),
    path('data4', views.data_project_4, name = 'data_project_4'),
    path('data5', views.data_project_5, name = 'data_project_5')
]