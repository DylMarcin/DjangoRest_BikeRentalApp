from django.urls import path, include
from . import views
from .views import ClientView, BikeView, RentalView, ActiveRentalView, AvailableBikeView, RentalList, RentalDetails, BikeList, BikeDetails
from rest_framework import routers

router = routers.DefaultRouter()

#router.register('bikes', BikeView, basename='bikes')
router.register('rentallist', RentalView, basename='rentallist')
router.register('clients', ClientView, basename='clients')
router.register('activerentals', ActiveRentalView, basename='activerentals')
router.register('availablebikes', AvailableBikeView, basename='availablebikes')


urlpatterns = [
    path('', include(router.urls)),
    path('rentals/<int:pk>/', RentalDetails.as_view()),
    path('rentals/', RentalList.as_view()),
    path('bikes/<int:pk>/', BikeDetails.as_view()),
    path('bikes/', BikeList.as_view()),

]
