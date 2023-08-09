from django.urls import path, include
from watchlist_app.api.views import *

urlpatterns = [
    path('list/', WatchListList.as_view(), name = 'movie-list'),
    path('<int:pk>', WatchListDetails.as_view(), name = 'movie-detail'),


    path('stream/', StreamPlatFormList.as_view(), name = 'stream-platform'),
    path('stream/<int:pk>/review', StreamPlatFormDetails.as_view(), name = 'stream-details'),


    path('reviews/', ReviewList.as_view(), name = 'reviews'),
    path('reviews/details/<int:pk>', ReviewCreate.as_view(), name = 'review-details')
]