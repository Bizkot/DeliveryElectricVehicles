from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('firstheuristic/', views.first_heuristic, name="first_heuristic"),
    path('secondheuristic/', views.second_heuristic, name="second_heuristic")
]
