from rest_framework import serializers
from .models import Client, Bike, Rental

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ['id', 'bike_id_number', 'producer', 'model', 'created', 'available']

class RentalSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='name')
    bike_id_number = serializers.SlugRelatedField(queryset=Bike.objects.all(), slug_field='bike_id_number', many=True)
    
    class Meta:
        model = Rental
        fields = ['id', 'client', 'bike_id_number', 'created', 'returned']
