from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [

    path(
        'users/<slug:user_slug>/',
        views.UserProductsListView.as_view(),
        name='users',
    ),

    path('users/<slug:user_slug>/products/<slug:product_slug>/',
         views.UserProductsDetailView.as_view(),
         name='users',
         ),

    path(
        'main-statistics/',
        views.MainStatisticsView.as_view(),
        name='main-statistics',
    ),
]
