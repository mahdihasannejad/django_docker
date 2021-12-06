from django.urls import path

from . import views

urlpatterns = [
    # path('', views.Index, name='index'),
    path('', views.index, name='index'),
    path('N-platform', views.topPlatform, name='topPlatform'),
    path('N-year', views.topYear, name='topYear'),
    path('N-genre', views.topGenre, name='topGenre'),
    path('rank', views.rank, name='rank'),
    path('name', views.name, name='name'),
    path('top-year-platform', views.topYearPlatform, name='topYearPlatform'),
    path('eu-na', views.naLessThanEU, name='naLessThanEU'),

]