from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

#Using ModelViewSet to create the basic CRUD operations automatically
class MovieViewSet(viewsets.ModelViewSet):
  queryset = Movie.objects.all()
  serializer_class = MovieSerializer
  #Token usage
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  #custom method
  #Override and using decorators
  @action(detail=True, methods=['POST'])
  def rate_movie(self, request, pk=None):
    if 'stars' in request.data:
      #print(pk)
      movie = Movie.objects.get(id=pk)
      stars = request.data['stars']
      #Uncomment this is you want to use it with the token
      user = request.user
      #Manually using user id for now...
      #user = User.objects.get(id=1)
      #print('user',user.username)

      try:
        rating = Rating.objects.get(user=user.id, movie=movie.id)
        rating.stars = stars
        rating.save()
        serializer = RatingSerializer(rating, many=False)
        response = {'message': 'Rating updated', 'result': serializer.data}
        return Response(response, status=status.HTTP_200_OK)
      except:
        rating = Rating.objects.create(user=user, movie=movie, stars=stars)
        serializer = RatingSerializer(rating, many=False)
        response = {'message': 'Rating created', 'result': serializer.data}
        return Response(response, status=status.HTTP_200_OK)


    else:
      response = {'message': 'You need to provide stars'}
      return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
  queryset = Rating.objects.all()
  serializer_class = RatingSerializer
  #Token usage
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)

  def update(self, request, *args, **kwargs):
    response = {'message': 'You cannot update rating like that'}
    return Response(response, status=status.HTTP_400_BAD_REQUEST)

  def create(self, request, *args, **kwargs):
    response = {'message': 'You cannot create rating like that'}
    return Response(response, status=status.HTTP_400_BAD_REQUEST)