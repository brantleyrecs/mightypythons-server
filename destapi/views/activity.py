from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from destapi.models import Activity

class ActivityView(ViewSet):
    """Level up activity view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single activitys

        Returns:
            Response -- JSON serialized activity
        """
        try:
            activity = Activity.objects.get(pk=pk)
            serializer = ActivitySerializer(activity, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Activity.DoesNotExist as ex:
            return Response({'Activity does not exist': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all activitys

        Returns:
            Response -- JSON serialized list of activitys
        """
        activity = Activity.objects.all()
        serializer = ActivitySerializer(activity, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def create(self, request):
        """Handle POST operations

        Returns
          Response -- JSON serialized activity instance
        """
        activity = Activity.objects.create(
            name = request.data["name"],
            bio = request.data["bio"],
        )
        activity.save()

        serializer = ActivitySerializer(activity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a activity

        Returns:
          Response -- Empty body with 204 status code
        """
        try:
            activity = Activity.objects.get(pk=pk)
      
            activity.name = request.data["name"]
            activity.bio = request.data["bio"]

            activity.save()
        
            serializer = ActivitySerializer(activity, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Activity.DoesNotExist as ex:
            return Response({'Activity does not exist': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, response, pk):
        """Deletes Data

        Returns:
            Response: Empty body with 204 code
        """
        
        activity = Activity.objects.get(pk=pk)
        activity.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

        

class ActivitySerializer(serializers.ModelSerializer):
    """JSON serializer for activities

    """
    class Meta:
        model = Activity
        fields = ('id', 'name', 'bio')
        depth = 1
