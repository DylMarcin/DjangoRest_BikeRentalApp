from django.shortcuts import render
from .models import Client, Bike, Rental
from .serializers import ClientSerializer, BikeSerializer, RentalSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import generics


# Create your views here.

class ClientView(viewsets.ViewSet):

    def list(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Client.objects.all()
        client = get_object_or_404(queryset, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk=None):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        rental = Client.objects.get(pk=pk)
        rental.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BikeView(viewsets.ViewSet):
    
    def list(self, request):
        bikes = Bike.objects.all()
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = BikeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Bike.objects.all()
        bike = get_object_or_404(queryset, pk=pk)
        serializer = BikeSerializer(bike)
        return Response(serializer.data)

    def put(self, request, pk=None):
        bike = Bike.objects.filter(pk=pk)
        serializer = BikeSerializer(bike, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        rental = Bike.objects.filter(pk=pk)
        rental.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RentalView(viewsets.ViewSet):

    def list(self, request):
        rentals = Rental.objects.all()
        serializer = RentalSerializer(rentals, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RentalSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return HttpResponse('', status=200)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Rental.objects.all()
        rental = get_object_or_404(queryset, pk=pk)
        serializer = RentalSerializer(rental)
        return Response(serializer.data)

    def update(self, request, pk=None):
        rental = Rental.objects.filter(pk=pk)
        serializer = RentalSerializer(rental, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        rental = Rental.objects.filter(pk=pk)
        rental.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RentalList(generics.ListCreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer


class RentalDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

class BikeList(generics.ListCreateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer


class BikeDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer

class ActiveRentalView(RentalView, viewsets.ViewSet):

     def list(self, request, pk=None):
        rentals = Rental.objects.all().filter(returned=False)
        serializer = RentalSerializer(rentals, many=True)
        return Response(serializer.data)



class AvailableBikeView(BikeView, viewsets.ViewSet):
    def list(self, request, pk=None):
        bike = Bike.objects.all().filter(available=True)
        serializer = BikeSerializer(bike, many=True)
        return Response(serializer.data)
        

