from django.urls import path, include
from watchlist_app.api.views import *

urlpatterns = [
    path('list/', WatchListList.as_view(), name = 'movie-list'),
    path('<int:pk>', WatchListDetails.as_view(), name = 'movie-detail'),
]
