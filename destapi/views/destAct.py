from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from destapi.models import DestAct, Destination, Activity

class DestActView(ViewSet):
    """Level up destAct view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single destination activitys

        Returns:
            Response -- JSON serialized destination activity
        """
        try:
            destAct = DestAct.objects.get(pk=pk)
            serializer = DestActSerializer(destAct, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DestAct.DoesNotExist as ex:
            return Response({'DestAct Join Table does not exist': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)



    def list(self, request):
        """Handle GET requests to get all destination activitys

        Returns:
            Response -- JSON serialized list of destination activitys
        """
        destAct = DestAct.objects.all()
        serializer = DestActSerializer(destAct, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def create(self, request):
        """Handle POST operations

        Returns
          Response -- JSON serialized destination activity instance
        """
        destination = Destination.objects.get(pk=request.data['destination'])
        activity = Activity.objects.get(pk=request.data['activity'])
        destAct = DestAct.objects.create(
            destination = destination,
            activity = activity
        )

        serializer = DestActSerializer(destAct, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a destination activity

        Returns:
          Response -- Empty body with 204 status code
        """
        try:
            destAct = DestAct.objects.get(pk=pk)
        
            destination = Destination.objects.get(pk=request.data['destination'])
            activity = Activity.objects.get(pk=request.data['activity'])
      
            destAct.destination = destination
            destAct.activity = activity

            destAct.save()
        except DestAct.DoesNotExist as ex:
            return Response({'DestAct join table does not exist': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DestActSerializer(destAct, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, response, pk):
        """Deletes Data

        Returns:
            Response: Empty body with 204 code
        """
        destAct = DestAct.objects.get(pk=pk)
        destAct.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class DestActSerializer(serializers.ModelSerializer):
    """JSON serializer for destination activitys

    """
    class Meta:
        model = DestAct
        fields = ('id', 'destination', 'activity')
        depth = 1