from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
    path("popular",podcastView.as_view(),name="famous_podcast"),
    path("podcast/",podcastList.as_view(),name="famous_podcast"),
    path("podcast/<str:postid>",podcast.as_view(),name="particular_podcast"),
    path("podcastFav/<uuid:postid>/<str:username>/",FavouritePodcast.as_view(),name="favourite_podcast"),
    
]
