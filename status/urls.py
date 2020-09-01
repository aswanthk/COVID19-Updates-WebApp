from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='status-home'),
    path('country-cases/', views.cases, name='status-cases'),
    path('country-cases/india', views.cases_india, name='status-cases-india'),
    path('country-cases/world', views.cases_world, name='status-cases-world')
]
