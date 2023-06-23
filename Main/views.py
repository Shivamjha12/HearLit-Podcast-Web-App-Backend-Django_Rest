from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from .models import *
import jwt,datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class podcastView(generics.ListCreateAPIView):
    queryset = podcast_data.objects.all()
    serializer_class = PopularPodcastSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PopularPodcastSerializer(queryset, many=True)
        return Response(serializer.data)
    
class podcastList(generics.ListCreateAPIView):
    search_fields = ['title','description','speaker']
    filter_backends = (filters.SearchFilter,)
    queryset = podcast_data.objects.all()
    serializer_class = PopularPodcastSerializer
    
class podcast(APIView):
    
    def get(self,request,postid):
        queryset = podcast_data.objects.filter(postid=postid).first()
        serializer = PopularPodcastSerializer(queryset)
        return Response(serializer.data)
    
class FavouritePodcast(APIView):
    def get(self,request,postid,username):
        user = User.objects.get(email=username)
        podcast_item = podcast_data.objects.filter(postid=postid).first()
        try:
            podcastq = Favorite_podcast.objects.get(user=user,podcast=podcast_item)
            
            is_favorite = podcastq.is_favorite
            print("Hereeeeeeeeeeeeeeeeeeeeeeeee---------eeee",is_favorite)
            serializer = FavouritePodcastSerializer({'is_favorite': is_favorite})
            return Response(serializer.data)
        except Favorite_podcast.DoesNotExist:
            return Response("NO favourite Podcast")
    
    def post(self,request,*args,**kwargs):
        username = request.data.get('username')
        postid = request.data.get('postid')
        print(username,postid, "impooooooooooooorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrnttttttttttttt")
        user = User.objects.filter(email=username).first()
        print(user)
        podcast = podcast_data.objects.filguter(postid=postid).first()
    
        print(podcast,"here------------------xxxxxxxxxxx--------------xxxxxxxxxxxxx-------xx-x-x-xxxxxxxxxxxxxx")
        try:
            fav = Favorite_podcast.objects.filter(user=user, podcast=podcast).first()
            if fav.is_favorite==True:
                fav.is_favorite = False
                fav.save()
                return Response({'message': 'Podcast removed from favorite'})
            else:
                fav.is_favorite = True
                fav.save()
                return Response({'message': 'Podcast Marked as Favorite'})
            
        except Favorite_podcast.DoesNotExist:
            fav = Favorite_podcast.objects.create(user=user, podcast=podcast)
            fav.is_favorite = True
            fav.save()
            return Response({'message': 'Podcast marked as favorite'})
            
    
    def put(self, request,*args,**kwargs):
        username = request.GET.get('username')
        postid = request.GET.get('postid')
        user = User.objects.filter(email=username).first()
        try:
            post = podcast_data.objects.filter(postid=postid).first()
            favorite = Favorite_podcast.objects.get(podcast=post)
            print(favorite,"------dx-x--x-xxxxxxxxxxxxxxxx---------xxxxxxxxxxxxxxxx----------xxxxxxxx")
            favorite_podcast = None
            print(favorite_podcast,"------dx-x--x-xxxxxxxxxxxxxxxx---------xxxxxxxx")
            if favorite_podcast.is_favorite == False:
                favorite_podcast.is_favorite = True
                favorite_podcast.save()
            else:
                favorite_podcast.is_favorite = False
                favorite_podcast.save()
            print(favorite_podcast)
            return Response({'message': 'Podcast marked as favorite'})
        except Favorite_podcast.DoesNotExist:
            return Response({'message': 'Podcast Not found'})