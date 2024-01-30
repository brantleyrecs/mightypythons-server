from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from destapi.models import Climate

class ClimateView(ViewSet):
    """Level up climate view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single climates

        Returns:
            Response -- JSON serialized climate
        """
        climate = Climate.objects.get(pk=pk)
        serializer = ClimateSerializer(climate, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        """Handle GET requests to get all climates

        Returns:
            Response -- JSON serialized list of climates
        """
        climate = Climate.objects.all()
        serializer = ClimateSerializer(climate, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def create(self, request):
        """Handle POST operations

        Returns
          Response -- JSON serialized climate instance
        """
        climate = Climate.objects.create(
            name = request.data["name"],
        )

        serializer = ClimateSerializer(climate, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a climate

        Returns:
          Response -- Empty body with 204 status code
        """

        climate = Climate.objects.get(pk=pk)
      
        climate.name = request.data["name"]

        climate.save()
        
        serializer = ClimateSerializer(climate, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, response, pk):
        """Deletes Data

        Returns:
            Response: Empty body with 204 code
        """
        climate = Climate.objects.get(pk=pk)
        climate.delete()
        return response(None, status=status.HTTP_204_NO_CONTENT)
        

class ClimateSerializer(serializers.ModelSerializer):
    """JSON serializer for activities

    """
    class Meta:
        model = Climate
        fields = ('id', 'name')
        depth = 1