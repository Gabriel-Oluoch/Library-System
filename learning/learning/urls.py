
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from base import views

urlpatterns = [
    path('login/',views.Custom_login,name='login'),
    path('sign_up/',views.sign_up,name='sign_up'),
    path('home/',views.home, name = 'home-view'),
    path('contact',views.contact_view, name='contact'),
    path('room/<str:pk>/',views.room, name = 'room-view'),
    path('create-room/', views.createRoom, name= "create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name= "update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name= "delete-room"),
    
    
    path('admin/', admin.site.urls),
    path('base/',include('base.urls')),
    path('accounts/', include('registration.backends.default.urls')),
    # Root URL redirects to sign_in
    path('',lambda request: redirect('login/',permanent=False)),
]

