from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.decorators import action
from destapi.models import Destination, User

class DestinationView(ViewSet):
  
  def retrieve(self, request, pk):
    """getting single Destination"""
    destination = Destination.objects.get(pk=pk)
    serializer = DestinationSerializer(destination)
    return Response(serializer.data)
  
  def list(self, request):
    """Getting all Destinations"""
    destination = Destination.objects.all()
    serializer = DestinationSerializer(destination, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    """Create Destination"""
    user_id = User.objects.get(pk=request.data["userId"])
    
    destination = Destination.objects.create(
      user=user_id,
      name=request.data["name"],
      bio=request.data["bio"],
      image=request.data["image"],
    )
    
    destination.save()
    serializer = DestinationSerializer(destination)
    return Response(serializer.data)
  
  def update(self, request, pk):
    """Update Destination"""
    destination = Destination.objects.get(pk=pk)
    destination.name=request.data["name"]
    destination.bio=request.data["bio"]
    destination.image=request.data["image"]
    
    user_id=User.objects.get(pk=request.data["userId"])
    destination.user=user_id
    
    destination.save()
    serializer = DestinationSerializer(destination)
    return Response(serializer.data)
  
  def destroy(self, request, pk):
    """Delete Destination"""
    destination = Destination.objects.get(pk=pk)
    destination.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)


class DestinationSerializer(serializers.ModelSerializer):
  """serializer for Order"""
  # items = OrderItemSerializer(many=True, read_only=True)
  class Meta:
    model=Destination
    fields = ('id', 'name', 'bio', 'image', 'user')
    depth = 2
