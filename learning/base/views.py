from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Room,Topic
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print("the form was sent")
            send_mail("mail message","contact","comfortinesiwende@gmail.com",['comsiwende@gmail.com'])
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(
                f'Message from {name}',
                message,
                email,
                ['comsiwende@gmail.com'],  # Enter target email address with your email
            )
            return render(request, 'success.html')  # Redirect to a success page
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
    context = {"form":form}
    return render(request, 'sign_up.html',context)

# login
def Custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home-view')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
# rooms = [
#     {'id':1, 'name':'Python Django!'},
#     {'id':2, 'name':'TypeScript!'},
#     {'id':3, 'name':'TailWind css!'},
# ]
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count
    }
    return render(request,'home.html',context)

def room(request, pk):
    room = Room.objects.get(id=pk)
   
    context = {
        'room':room
    }
    return render(request,'room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home-view')
    context = {
        'form':form
    }
    return render(request, 'room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home-view')
    context = {
        'form':form
    }
    return render(request, 'room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home-view')
    return render(request, 'delete.html',{'obj':room})