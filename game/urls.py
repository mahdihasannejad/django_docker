from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('top-platform', views.topplatform, name='topPlatform'),
    path('rank', views.ir_rank, name='rank'),
    path('name', views.ir_name, name='name'),
    path('top-year', views.topYear, name='topYear'),
    path('top-category', views.topCategory, name='topCategory'),
    path('top-year-plarform', views.topYear_platform, name='topYear_platform'),
    path('top-eu-nam', views.topEU_NAm, name='rank'),

]