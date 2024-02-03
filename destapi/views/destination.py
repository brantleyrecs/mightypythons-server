from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.decorators import action
from destapi.models import Destination, User, DestAct, Activity, Climate
from destapi.views.activity import ActivitySerializer

class DestinationView(ViewSet):
  
  def retrieve(self, request, pk):
    """getting single Destination"""
    destination = Destination.objects.get(pk=pk)
    serializer = DestinationSerializer(destination)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def list(self, request):
    """Getting all Destinations"""
    destination = Destination.objects.all()
    serializer = DestinationSerializer(destination, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    """Create Destination"""
    user_id = User.objects.get(pk=request.data["userId"])
    climate_id = Climate.objects.get(pk=request.data["climateId"])
    
    destination = Destination.objects.create(
      climate=climate_id,
      user=user_id,
      name=request.data["name"],
      bio=request.data["bio"],
      image=request.data["image"],
    )
    
    destination.save()
    serializer = DestinationSerializer(destination)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    """Update Destination"""
    destination = Destination.objects.get(pk=pk)
    destination.name=request.data["name"]
    destination.bio=request.data["bio"]
    destination.image=request.data["image"]
    
    user_id=User.objects.get(pk=request.data["userId"])
    destination.user=user_id
    
    climate_id=Climate.objects.get(pk=request.data["climateId"])
    destination.climate=climate_id
    
    destination.save()
    serializer = DestinationSerializer(destination)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    """Delete Destination"""
    destination = Destination.objects.get(pk=pk)
    destination.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  @action(methods=['get'], detail=True)
  def activities(self, request, pk):
    """Method to get all the items associated to a single order"""
    activities = Activity.objects.all()
    associated_destination = activities.filter(destination_id=pk)
    
    serializer = ActivitySerializer(associated_destination, many=True)
    return Response(serializer.data)
  
class DestActSerializer(serializers.ModelSerializer):
  name = serializers.ReadOnlyField(source='activity.name')
  bio = serializers.ReadOnlyField(source='activity.bio')

  class Meta:
    model = DestAct
    fields = ('id', 'name', 'bio')


class DestinationSerializer(serializers.ModelSerializer):
  """serializer for Order"""
  dest_activities = DestActSerializer(many=True, read_only=True)
  class Meta:
    model=Destination
    fields = ('id', 'name', 'bio', 'image', 'user', 'dest_activities', 'climate')
    depth = 2
