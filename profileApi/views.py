from django.contrib.auth import authenticate
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import serializers
from . import models
from . import permissions


# Create your views here.

class HelloApiview(APIView):
    serializer_class = serializers.HelloSerializers

    def get(self, request, format=None):
        an_apiview = ['uses HTTP methods as function(get, post, patch, put ,delete)',
                      'It is similar to a traditional Django view',
                      'Gives you the most control over your logic'
                      ]
        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        serializer = serializers.HelloSerializers(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HelloViewSet(viewsets.ViewSet):
    serializer_class = serializers.HelloSerializers

    def list(self, request):
        a_view_set = ['Uses actions (list, create, retrieve, update, partial_update)',
                      'Automatically maps to Urls using Routers',
                      'provides more functionlity with less code']
        return Response({'message': 'Hello!', 'a_view_set': a_view_set})

    def create(self, request):
        serializer = serializers.HelloSerializers(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response({'Http_method': 'Get'})

    def update(self, request, pk=None):
        return Response({'Http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        return Response({'Http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        return Response({'Http_method': 'Delete'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handles create, creating and update profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'email',)


class LoginViewSet(viewsets.ViewSet):
    serializer_class = serializers.LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Generate or retrieve the token
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileFeedViewSets(viewsets.ModelViewSet):
    """Handling creating and updating profile feed item."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializers
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus,IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """ sets the user profile to the logged-in user."""
        serializer.save(user_profile=self.request.user)
