from rest_framework import serializers
from .models import Movie, Rating
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    #fields = '__all__'
    fields = ('id','username','password')
    #---Passing more args for field password
    #---Setting write only hides it from the api call result
    extra_kwargs = {'password': {'write_only': True, 'required': True}}

  #---overriding create method from framework
  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    #---token creation
    Token.objects.create(user=user)
    #print(token)
    return user

class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields = ('id', 'title', 'description', 'no_of_ratings','avg_rating')

class RatingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Rating
    fields = ('id', 'stars', 'user', 'movie')
