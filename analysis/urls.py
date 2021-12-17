from django.urls import path

from . import views

urlpatterns = [
    path('compare', views.compareTwo, name='compareTwo'),
    path('total', views.total, name='total'),
    path('two-company', views.twoCompany, name='twoCompany'),
    path('compare-genre', views.compareGenre, name='compareGenre'),
]