from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from destapi.models import User

class UserView(ViewSet):
    """Level up user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single users

        Returns:
            Response -- JSON serialized user
        """
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        """Handle GET requests to get all users

        Returns:
            Response -- JSON serialized list of users
        """
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def create(self, request):
        """Handle POST operations

        Returns
          Response -- JSON serialized user instance
        """
        user = User.objects.create(
            name = request.data["name"],
            uid = request.data["uid"],
        )

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a user

        Returns:
          Response -- Empty body with 204 status code
        """

        user = User.objects.get(pk=pk)
      
        user.name = request.data["name"]
        user.uid = request.data["uid"]

        user.save()
        
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, response, pk):
        """Deletes Data

        Returns:
            Response: Empty body with 204 code
        """
        user = User.objects.get(pk=pk)
        user.delete()
        return response(None, status=status.HTTP_204_NO_CONTENT)
        

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for activities

    """
    class Meta:
        model = User
        fields = ('id', 'name', 'uid')
        depth = 1